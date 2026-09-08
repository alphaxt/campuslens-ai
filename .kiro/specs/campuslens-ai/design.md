# CampusLens AI - Complete System Design

## 1. System Overview

CampusLens AI is an AI-powered campus issue intelligence and resolution platform that transforms unstructured student complaints into actionable intelligence for university administration. Students submit campus problems using natural language, the system analyzes each report with AI and semantic analysis to extract structured information, detect duplicates, and calculate priority scores. Administrators access a comprehensive dashboard to manage issues, view analytics, track status changes, and understand campus trends through AI-generated insights.

The platform serves two primary user groups: students who submit and track issues without needing to know correct categories or departments, and administrators who efficiently triage, prioritize, and resolve problems at scale. By combining generative AI for intelligent analysis with semantic embeddings for duplicate detection, CampusLens ensures no issue is missed and resources are allocated to the highest-impact problems.

**Core Value Proposition:**
- Students: Simple natural language issue submission with AI-powered analysis and transparent tracking
- Administrators: Complete visibility into campus problems, automatic duplicate detection, intelligent prioritization, and data-driven insights for resource allocation

**Architecture at 50,000 feet:**
Frontend (React SPA on Vercel) → Backend API (FastAPI on Render) → Database (Supabase PostgreSQL) ↔ AI Services (Google Gemini API)

---

## 2. Architecture Components

### 2.1 Frontend Layer (React/Vite/Tailwind)

**Technology Stack:**
- Framework: React 19
- Build Tool: Vite 8 (optimized development and production builds)
- Styling: Tailwind CSS 4 (utility-first, responsive design)
- Routing: React Router 7 (client-side navigation)
- Charts: Recharts 3 (data visualization)
- Database Client: Supabase JS SDK (real-time updates via RLS)
- Deployment: Vercel (automatic deployments on Git push)

**Architecture:**

The frontend is a Single Page Application hosted on Vercel that serves both student and administrator interfaces. Routes are protected via `ProtectedRoute` component which checks authentication via Supabase Auth and role claims. Global authentication state is managed through `AuthContext`, providing user identity and admin status to all components.

**Student Portal Pages:**
- **ReportIssue.jsx** - Issue submission form with real-time AI analysis preview
  - Text input for natural language description
  - AI analysis display (category, severity, location, department)
  - Confidence and fallback indicators
  - Submit confirmation with issue ID
  
- **MyReports.jsx** - Personal issue tracking dashboard
  - Paginated list of student's submitted issues
  - Filtering by status and category
  - Quick access to issue details, status history
  - Real-time status updates when admin changes status

- **Login.jsx** - Supabase Auth integration
  - Email/password login
  - Error messaging
  - Redirect to dashboard on success

- **Register.jsx** - New user account creation
  - Email/password registration
  - Student role assignment
  - Automatic login on success

**Administrator Dashboard Pages:**
- **AdminDashboard.jsx** - Main administrative interface
  - Overview statistics (total issues, open count, critical count)
  - Advanced filtering panel (category, severity, status, location, date range)
  - Issues table with sortable columns and inline status updates
  - Analytics section with charts

- **Supporting Components:**
  - **AnalyticsCharts.jsx** - Category distribution, severity distribution, status breakdown
  - **CampusPulse.jsx** - AI-generated campus health summary with trends and recommendations
  - **StatusHistory.jsx** - Timeline of status changes for specific report

**UI Components:**
- **Navbar.jsx** - Navigation with auth state, logout button
- **ProtectedRoute.jsx** - Route guard checking authentication and admin status
- **AuthContext.jsx** - Global state provider for user info, admin flag, session management

**Key Features:**
- All routes require Supabase authentication
- Admin routes additionally require `admin_flag` claim in JWT
- Error boundaries prevent UI crashes from API failures
- Responsive design adapts to mobile, tablet, desktop
- Fallback UI when Gemini API unavailable (shows basic data without AI analysis)

### 2.2 Backend Layer (FastAPI)

**Technology Stack:**
- Framework: FastAPI (modern, async, high-performance)
- Server: Uvicorn (ASGI server)
- Validation: Pydantic (request/response validation)
- Authentication: Supabase Auth (JWT tokens, RLS integration)
- Database: Supabase Python SDK (PostgreSQL client)
- AI: Google Gemini API (issue analysis, embeddings, campus pulse)
- Deployment: Render (automatic deployments, auto-scaling)

**Architecture:**

FastAPI backend provides 7 REST API endpoints with role-based access control. All endpoints verify Supabase JWT tokens and apply RLS policies. The backend is organized into modular services: `ai_service.py` for Gemini calls with fallback handling, `duplicate.py` for embedding-based duplicate detection, `priority.py` for priority scoring logic, `database.py` for Supabase queries, and `auth.py` for token verification.

**7 API Endpoints:**

1. **POST /reports** - Submit new issue
   - Authentication: Student (any authenticated user)
   - Input: `{ description: string }`
   - Processing Flow:
     - `analyze_issue(description)` - Get AI analysis (with fallback if Gemini unavailable)
     - `find_best_duplicate(description, category, location, active_reports)` - Check for duplicates using embeddings
     - `calculate_priority_score(severity, safety_flag, accessibility_flag, duplicate_count)` - Score issue
     - `save_report(report_data, token)` - Store in database with RLS
     - `save_duplicate_relationship(new_report_id, original_id, similarity_score)` - Log duplicate if found
     - `update_report_priority(original_report_id, new_priority, token)` - Boost priority of original report
   - Output: `{ success: bool, report: Report, analysis: Analysis, duplicate: DuplicateResult }`
   - Side Effects: Report stored, embedding computed, duplicate relationship created (if applicable), original report's priority updated

2. **GET /reports** - List all reports
   - Authentication: Authenticated (any logged-in user)
   - Query Parameters: None
   - RLS: Students see own reports only; Admins see all
   - Output: `{ success: bool, count: int, reports: Report[] }`
   - Processing: Queries database, computes duplicate_count for each report

3. **GET /reports/{report_id}** - Get specific report
   - Authentication: Authenticated
   - RLS: Students can access only own reports; Admins can access any
   - Output: `{ success: bool, report: Report }`
   - 404 if report not found or access denied

4. **PUT /reports/{report_id}/status** - Update report status (admin only)
   - Authentication: Admin required
   - Input: `{ status: string }`
   - Valid Statuses: Submitted, Under Review, In Progress, Resolved, Closed
   - Processing:
     - Validate new status
     - Get current report and its old status
     - Update status in database
     - Log status change in status_history table
   - Output: `{ success: bool, report: Report, history: StatusHistory }`
   - Side Effects: Audit trail created, student sees update in real-time via RLS

5. **GET /reports/{report_id}/history** - Get status history
   - Authentication: Authenticated
   - RLS: Students see history for own reports; Admins see any
   - Output: `{ success: bool, count: int, history: StatusHistory[] }`
   - Ordered chronologically

6. **GET /analytics/campus-pulse** - AI-generated campus insights (admin only)
   - Authentication: Admin required
   - Query Parameters: Optional date_range
   - Processing:
     - Fetch all reports within date range
     - Call `generate_campus_pulse(reports)` with fallback handling
     - Campus Pulse returns: { headline, summary, major_concern, emerging_trend, critical_issue, improvement, recommended_actions }
   - Output: `{ success: bool, pulse: CampusPulse }`
   - Caching: Results cached for 30 minutes to reduce API calls
   - Fallback: Returns basic statistics if Gemini unavailable

7. **POST /priority/recalculate** - Recalculate priorities (admin only)
   - Authentication: Admin required
   - Purpose: Called daily via scheduled job to update priorities based on duration
   - Processing:
     - Get all active reports (not Resolved/Closed)
     - For each report, recalculate priority including duration bonus
     - Update database if priority changed
   - Output: `{ success: bool, recalculated: int, unchanged: int, total_active: int }`
   - Side Effects: Priority scores updated for reports open > 7 days

**Error Handling:**
- All endpoints catch exceptions and return user-friendly error messages
- Actual error details logged for admin debugging
- Gemini API failures handled with fallback analysis (no exception exposed to user)
- Database errors return appropriate HTTP status codes (400, 404, 403, 500)
- Rate limiting enforced at infrastructure level (Render, CORS)

**CORS Configuration:**
- Allowed Origins: http://localhost:5173, http://127.0.0.1:5173, https://campuslens-ai.vercel.app
- Credentials: Enabled (for JWT in cookies or Authorization headers)
- Methods: All (*), Headers: All (*)

### 2.3 Data Layer (Supabase PostgreSQL)

**Database Architecture:**

Supabase provides managed PostgreSQL with pgvector extension (for embeddings), built-in authentication (Supabase Auth), Row-Level Security (RLS) policies, and real-time subscriptions. The database enforces data access policies at the row level, ensuring students see only their own reports while admins see all data.

**3 Core Tables:**

1. **reports** (Issue Storage)
   - Columns:
     - `id` (UUID, primary key)
     - `student_id` (UUID, foreign key to auth.users)
     - `original_description` (text) - Raw student input
     - `ai_summary` (text) - AI-generated concise summary
     - `category` (text enum) - Network, Facilities, Security, Cleanliness, Transport, Accessibility, Academic Facilities, Uncategorized
     - `severity` (text enum) - Low, Medium, High, Critical
     - `extracted_location` (text, nullable) - Location parsed from description or map selection
     - `recommended_department` (text) - AI-determined responsible department
     - `priority_score` (integer, 0-100) - Dynamic ranking
     - `status` (text enum) - Submitted, Under Review, In Progress, Resolved, Closed
     - `is_safety_flag` (boolean) - Safety concern detected
     - `is_accessibility_flag` (boolean) - Accessibility impact detected
     - `confidence` (decimal, 0-1) - AI analysis confidence
     - `created_at` (timestamp with timezone)
     - `updated_at` (timestamp with timezone, auto-updated)
   - Indexes: student_id, category, status, priority_score, created_at
   - RLS Policy: Students SELECT/INSERT own records; Admins SELECT all; UPDATE requires admin role

2. **status_history** (Audit Trail)
   - Columns:
     - `id` (UUID, primary key)
     - `report_id` (UUID, foreign key to reports)
     - `old_status` (text) - Previous status value
     - `new_status` (text) - New status value
     - `changed_by` (UUID, foreign key to auth.users) - Admin who made change
     - `changed_at` (timestamp with timezone, auto-generated)
   - Purpose: Complete audit trail of all status transitions for compliance and transparency
   - RLS Policy: Students see history for own reports; Admins see all

3. **duplicate_relationships** (Duplicate Tracking)
   - Columns:
     - `id` (UUID, primary key)
     - `report_id` (UUID, foreign key to reports) - The duplicate report
     - `duplicate_of_report_id` (UUID, foreign key to reports) - The original report
     - `similarity_score` (decimal, 0-1) - Embedding cosine similarity
     - `created_at` (timestamp with timezone)
   - Purpose: Tracks which reports are duplicates of which, supports priority boosting and aggregation
   - RLS Policy: Implicit (students can only see through reports they can access; admins see all)
   - Note: Multiple reports can point to single original report

**Row-Level Security (RLS) Policies:**

Reports Table:
- SELECT: `(auth.uid() = student_id) OR (auth.jwt() ->> 'admin_flag' = 'true')`
  - Students see own reports; Admins see all
- INSERT: `auth.uid() = student_id`
  - Only the student can create their own report
- UPDATE: `auth.jwt() ->> 'admin_flag' = 'true'`
  - Only admins can update reports (status changes)

Status History Table:
- SELECT: `(SELECT student_id FROM reports WHERE id = report_id) = auth.uid() OR (auth.jwt() ->> 'admin_flag' = 'true')`
  - Students see history for their reports; Admins see all

**Duplicate Relationships Table:**
- Implicit RLS via reports table (accessed only through reports)

**Database Design Patterns:**

- Immutable audit trail: status_history records never updated/deleted
- Denormalized duplicate_count: Computed on-the-fly from duplicate_relationships but cached in reports for performance
- Timestamps: All records use `created_at` with default `now()` and `updated_at` with default `now()` + trigger for auto-update
- UUIDs: All primary keys are UUIDs for security and scalability

### 2.4 AI Services (Google Gemini)

**Integration Points:**

The system uses Google Gemini API in two ways: Gemini 3.6 Flash for issue analysis and Campus Pulse generation, and Gemini Embeddings 2 for semantic duplicate detection.

**Gemini 3.6 Flash - Issue Analysis (`analyze_issue()`):**

Purpose: Transform student's natural language description into structured analysis.

Prompt Instructions:
- Analyze university campus issue
- Determine category from predefined list
- Determine severity level (Low, Medium, High, Critical)
- Extract location information
- Identify responsible department
- Generate concise summary
- Flag safety concerns (exposed electrical, fire hazard, emergency situation)
- Flag accessibility concerns (blocked exits, barriers for disabled students)
- Provide confidence score (0-1)

Severity Guidelines:
- Low: Cosmetic inconvenience, non-essential equipment, doesn't disrupt learning/safety
- Medium: Noticeable disruption but alternatives exist (one broken projector, slow Wi-Fi in one area)
- High: Significant disruption affecting classes/many students (lab network down, major cooling failure)
- Critical: Immediate safety risk, serious accessibility issue, emergency, or campus-wide outage

Error Handling:
- All Gemini API calls wrapped in try/except
- Catches: ResourceExhausted (429), DeadlineExceeded (timeout), GoogleAPIError, generic Exception
- On error: Returns fallback analysis with confidence 0.5
- Fallback: { summary: "AI analysis unavailable", category: "Uncategorized", severity: "Medium", recommended_department: "Campus Facilities", extracted_location: null, safety_flag: false, accessibility_flag: false, confidence: 0.5 }
- Actual error logged with logging.error() for admin debugging
- Report submission continues with fallback data (never blocked by API failure)

**Gemini Embeddings 2 - Duplicate Detection (`get_embedding()`):**

Purpose: Generate semantic embeddings for issue descriptions to detect duplicates.

Process:
- Issue description embedded using `client.models.embed_content(model="gemini-embedding-2", contents=text)`
- Embedding is vector of ~768 dimensions
- Stored implicitly (not in database, computed on demand during duplicate check)

**Campus Pulse Generation (`generate_campus_pulse()`):**

Purpose: Generate AI insights about campus issue trends for administrators.

Processing:
- Fetches all reports from last 7 days (configurable)
- Sends summary of reports to Gemini with instructions to identify patterns
- Asks for: headline, summary, major concern, emerging trend, critical issue, improvement area, recommended actions
- Returns structured JSON with insights

Error Handling:
- Try/except wraps the API call
- On error: Returns basic statistics (category counts, severity distribution, top locations)
- Actual error logged for debugging
- Never crashes analytics endpoint

Response Structure:
```json
{
  "headline": "string (key insight in 1-2 words)",
  "summary": "string (2-3 sentence overview of campus state)",
  "major_concern": "string (biggest issue category)",
  "emerging_trend": "string (new pattern detected)",
  "critical_issue": "string (most urgent problem)",
  "improvement": "string (area showing progress)",
  "recommended_actions": ["action1", "action2", "action3"]
}
```

---

## 3. Data Models

### 3.1 Issue/Report Model

```
{
  id: UUID,
  student_id: UUID (auth.users.id),
  original_description: string (raw student input),
  ai_summary: string (AI-generated concise summary),
  category: string (
    Network | Facilities | Security | Cleanliness | 
    Transport | Accessibility | Academic Facilities | Uncategorized
  ),
  severity: string (Low | Medium | High | Critical),
  extracted_location: string | null (parsed from description or map),
  recommended_department: string (AI-determined responsible department),
  priority_score: int (0-100, calculated and recalculated daily),
  status: string (Submitted | Under Review | In Progress | Resolved | Closed),
  is_safety_flag: boolean (safety concern detected by AI),
  is_accessibility_flag: boolean (accessibility concern detected by AI),
  confidence: decimal (0-1, AI analysis confidence),
  created_at: timestamp with timezone (ISO 8601, set at creation),
  updated_at: timestamp with timezone (ISO 8601, auto-updated),
  duplicate_count: int (calculated from duplicate_relationships table)
}
```

### 3.2 Status History Model

```
{
  id: UUID,
  report_id: UUID (foreign key to reports),
  old_status: string (previous status value),
  new_status: string (new status value),
  changed_by: UUID (admin_id who made the change),
  changed_at: timestamp with timezone (auto-generated at creation)
}
```

### 3.3 Duplicate Relationship Model

```
{
  id: UUID,
  report_id: UUID (foreign key to reports - the duplicate report),
  duplicate_of_report_id: UUID (foreign key to reports - the original report),
  similarity_score: decimal (0-1, cosine similarity from embeddings),
  created_at: timestamp with timezone (auto-generated at creation)
}
```

---

## 4. API Design

### 4.1 POST /reports - Submit New Issue

**Purpose:** Students submit a new issue with natural language description.

**Authentication:** Requires valid Supabase JWT token with student role

**Request Body:**
```json
{
  "description": "string (required, natural language issue description)"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "report": [{
    "id": "uuid",
    "student_id": "uuid",
    "original_description": "...",
    "ai_summary": "...",
    "category": "Network",
    "severity": "High",
    "extracted_location": "Building A, Room 101",
    "recommended_department": "IT Department",
    "priority_score": 75,
    "status": "Submitted",
    "is_safety_flag": false,
    "is_accessibility_flag": false,
    "confidence": 0.92,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "duplicate_count": 2
  }],
  "analysis": {
    "summary": "...",
    "category": "Network",
    "severity": "High",
    "recommended_department": "IT Department",
    "extracted_location": "Building A, Room 101",
    "safety_flag": false,
    "accessibility_flag": false,
    "confidence": 0.92
  },
  "duplicate": {
    "is_duplicate": true,
    "duplicate_report_id": "uuid",
    "similarity_score": 0.87,
    "duplicate_priority": 70
  }
}
```

**Error Responses:**
- 400 Bad Request: Invalid input (empty description)
- 401 Unauthorized: Invalid or missing token
- 500 Internal Server Error: Database error (with generic message)

**Processing Flow:**
```
1. analyze_issue(description) → AI analysis or fallback
2. get_active_reports(token) → Active reports for duplicate check
3. find_best_duplicate(description, category, location, active_reports) → Duplicate result
4. calculate_priority_score(severity, safety, accessibility, 0) → Initial priority
5. If duplicate: add 10 to priority score
6. save_report(report_data, token) → Create report in database
7. If duplicate:
   - save_duplicate_relationship(...) → Log relationship
   - get_duplicate_count(original_id, token) → Count of duplicates
   - calculate_priority_score(...) → Recalculate original report priority
   - update_report_priority(original_id, new_priority, token) → Boost original
8. Return success with report and analysis
```

### 4.2 GET /reports - List All Reports

**Purpose:** Retrieve all reports (students see own, admins see all).

**Authentication:** Requires valid JWT token

**Query Parameters:** None (filtering done on frontend)

**Response (200 OK):**
```json
{
  "success": true,
  "count": 42,
  "reports": [
    { "id": "uuid", "category": "Network", "severity": "High", ... },
    { "id": "uuid", "category": "Facilities", "severity": "Low", ... }
  ]
}
```

**RLS Applied:** Supabase automatically filters based on user role

**Error Responses:**
- 401 Unauthorized: Invalid or missing token
- 500 Internal Server Error: Database error

### 4.3 GET /reports/{report_id} - Get Specific Report

**Purpose:** Retrieve detailed information about a single report.

**Authentication:** Requires valid JWT token

**Path Parameters:**
- `report_id` (string, required, UUID format)

**Response (200 OK):**
```json
{
  "success": true,
  "report": {
    "id": "uuid",
    "student_id": "uuid",
    "original_description": "...",
    "ai_summary": "...",
    "category": "Network",
    "severity": "High",
    "extracted_location": "Building A",
    "recommended_department": "IT",
    "priority_score": 75,
    "status": "Under Review",
    "is_safety_flag": false,
    "is_accessibility_flag": true,
    "confidence": 0.92,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-16T14:20:00Z",
    "duplicate_count": 2
  }
}
```

**Error Responses:**
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Report not found or access denied
- 500 Internal Server Error: Database error

**RLS Applied:** Students can only access own reports

### 4.4 PUT /reports/{report_id}/status - Update Report Status

**Purpose:** Admin changes report status and creates audit trail.

**Authentication:** Requires admin JWT token

**Path Parameters:**
- `report_id` (string, required, UUID format)

**Request Body:**
```json
{
  "status": "string (required, one of: Submitted, Under Review, In Progress, Resolved, Closed)"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "report": {
    "id": "uuid",
    "status": "In Progress",
    "updated_at": "2024-01-16T15:45:00Z",
    ...
  },
  "history": {
    "id": "uuid",
    "report_id": "uuid",
    "old_status": "Under Review",
    "new_status": "In Progress",
    "changed_by": "admin_uuid",
    "changed_at": "2024-01-16T15:45:00Z"
  }
}
```

**Error Responses:**
- 400 Bad Request: Invalid status value
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User is not admin
- 404 Not Found: Report not found
- 500 Internal Server Error: Database error

**Processing Flow:**
```
1. Validate status is in allowed list
2. Get current report to retrieve old_status
3. Check if status is changing (avoid duplicate history entries)
4. update_report_status(report_id, new_status, token) → Update database
5. add_status_history(report_id, old_status, new_status, admin_id, token) → Create audit entry
6. Return updated report and history entry
7. Frontend receives update via RLS subscription
```

### 4.5 GET /reports/{report_id}/history - Get Status History

**Purpose:** Retrieve complete status change timeline for a report.

**Authentication:** Requires valid JWT token

**Path Parameters:**
- `report_id` (string, required, UUID format)

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "history": [
    {
      "id": "uuid",
      "report_id": "uuid",
      "old_status": "Submitted",
      "new_status": "Under Review",
      "changed_by": "admin_uuid",
      "changed_at": "2024-01-15T11:00:00Z"
    },
    {
      "id": "uuid",
      "report_id": "uuid",
      "old_status": "Under Review",
      "new_status": "In Progress",
      "changed_by": "admin_uuid",
      "changed_at": "2024-01-16T15:45:00Z"
    }
  ]
}
```

**Error Responses:**
- 401 Unauthorized: Invalid or missing token
- 404 Not Found: Report not found or access denied
- 500 Internal Server Error: Database error

**RLS Applied:** Students see history for own reports; Admins see any

### 4.6 GET /analytics/campus-pulse - Campus Insights (Admin Only)

**Purpose:** Generate AI-powered summary of campus trends and priorities.

**Authentication:** Requires admin JWT token

**Query Parameters:**
- `date_range` (optional, string) - "7d", "30d", "90d" (default: "7d")

**Response (200 OK):**
```json
{
  "success": true,
  "pulse": {
    "headline": "Network Crisis Growing",
    "summary": "Campus experiencing surge in connectivity issues, particularly in Library and Lab Building. 34% of reports in past week related to network problems.",
    "major_concern": "Network (34 issues)",
    "emerging_trend": "Morning peak hours show 60% of network issues",
    "critical_issue": "Lab Building Wi-Fi completely down",
    "improvement": "Facilities response time improved 25% week-over-week",
    "recommended_actions": [
      "Deploy IT team to Lab Building immediately",
      "Increase network monitoring during 8-11 AM peak",
      "Schedule infrastructure upgrade for Library backup power"
    ]
  }
}
```

**Error Responses:**
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User is not admin
- 500 Internal Server Error: Database or Gemini error (returns fallback stats)

**Processing Flow:**
```
1. Authenticate as admin
2. get_all_reports(token) → Fetch all reports
3. Filter by date_range (if provided)
4. generate_campus_pulse(reports) → Call Gemini with fallback handling
5. Return pulse with AI insights or basic statistics if Gemini unavailable
```

**Caching:** Results cached for 30 minutes per date_range to reduce API calls

**Fallback (if Gemini unavailable):** Basic statistics structure instead of AI insights

### 4.7 POST /priority/recalculate - Recalculate Priorities (Admin Only)

**Purpose:** Scheduled job to update priority scores based on duration.

**Authentication:** Requires admin JWT token

**Request Body:** None

**Response (200 OK):**
```json
{
  "success": true,
  "recalculated": 12,
  "unchanged": 28,
  "total_active": 40
}
```

**Error Responses:**
- 401 Unauthorized: Invalid or missing token
- 403 Forbidden: User is not admin
- 500 Internal Server Error: Database error

**Processing Flow:**
```
1. Authenticate as admin
2. get_reports_for_priority_update(token) → Get all active (non-resolved) reports
3. For each report:
   a. Calculate should_recalculate_priority(...) → Check if duration bonus applies
   b. If priority would increase: update_report_priority(report_id, new_priority, token)
4. Return count of recalculated vs unchanged
```

**Purpose:** Called daily (e.g., 2 AM) via Render scheduled jobs to boost priority of reports open > 7 days

---

## 5. Component Architecture

### 5.1 Frontend Components

**Page Components:**
- **ReportIssue.jsx**
  - Student form for submitting issues
  - Real-time AI analysis preview as user types
  - Submit button with loading state
  - Success state with issue ID and tracking link
  - Error handling with retry option

- **MyReports.jsx**
  - Table of student's submitted issues
  - Columns: ID, category, severity, status, submitted date, last update
  - Filtering by status and category
  - Click to view details including status history
  - Real-time updates when admin changes status

- **AdminDashboard.jsx**
  - Overview cards: total issues, open count, critical count, this week's count
  - Advanced filter panel: category, severity, status, location, date range
  - Issues table with sortable columns
  - Inline status update dropdown
  - Pagination or infinite scroll
  - Link to CampusPulse and analytics

- **Login.jsx** / **Register.jsx**
  - Supabase Auth UI integration
  - Email/password forms
  - Error messages
  - Redirect on success

**Dashboard Components:**
- **AnalyticsCharts.jsx**
  - Bar chart: issues by category
  - Pie chart: severity distribution
  - Line chart: issues over time
  - Responsive layout, mobile-friendly

- **CampusPulse.jsx**
  - Display AI-generated insights
  - Headline, summary, key findings
  - Recommended actions list
  - Fallback display if Gemini unavailable

- **StatusHistory.jsx**
  - Timeline view of status changes
  - Shows timestamp, old status, new status, admin who made change
  - Can be embedded in report detail view

**Shared Components:**
- **Navbar.jsx**
  - Logo/branding
  - Navigation links (filtered by role)
  - User profile / logout
  - Theme toggle (if applicable)

- **ProtectedRoute.jsx**
  - Route guard checking authentication
  - Optional admin role check
  - Redirect to login if unauthenticated
  - Redirect to student portal if admin route accessed by student

- **AuthContext.jsx**
  - Global state provider
  - Manages user info, admin flag, session
  - Provides useAuth() hook for components
  - Handles session refresh

### 5.2 Backend Services

**ai_service.py - Gemini Integration with Fallback**
- `analyze_issue(description: str) → dict`
  - Wraps Gemini API call in try/except
  - Returns full analysis on success (summary, category, severity, location, department, flags, confidence)
  - Returns fallback analysis on any error (API unavailable, timeout, rate limit)
  - Logs actual errors for debugging
  
- `get_fallback_analysis(description: str) → dict`
  - Predefined fallback structure
  - Category: Uncategorized
  - Severity: Medium
  - Confidence: 0.5
  - Used when Gemini unavailable

- `generate_campus_pulse(reports: list) → dict`
  - Calls Gemini to analyze trends in reports
  - Returns insights: headline, summary, major_concern, emerging_trend, critical_issue, improvement, recommended_actions
  - Falls back to basic statistics if Gemini unavailable
  - Logs errors for debugging

- `get_fallback_campus_pulse(reports: list) → dict`
  - Computes basic statistics: category counts, severity distribution, top locations, resolution times
  - Returns as structured JSON matching expected format
  - Used when Gemini unavailable

**duplicate.py - Semantic Duplicate Detection**
- `get_embedding(text: str) → list[float]`
  - Calls Gemini Embeddings 2 model
  - Returns vector representation of text
  - Used for semantic similarity comparison

- `cosine_similarity(vector_a: list, vector_b: list) → float`
  - Computes cosine similarity between two embedding vectors
  - Returns score 0-1
  - Used to measure semantic similarity

- `find_best_duplicate(description: str, category: str, location: str, reports: list) → dict`
  - Compares new description against all active reports
  - Computes semantic similarity via embeddings
  - Boosts score for category and location matches (+0.05 for category, +0.10 for location)
  - Returns best match if similarity >= 0.80 OR (>= 0.72 with metadata support)
  - Result dict: { is_duplicate, duplicate_report_id, similarity_score, duplicate_priority }

**priority.py - Priority Score Calculation**
- `calculate_priority_score(severity, safety_flag, accessibility_flag, duplicate_count, created_at, current_status) → int`
  - Base severity scores: Low=25, Medium=50, High=70, Critical=90
  - Safety flag: +20 points
  - Accessibility flag: +15 points
  - Duplicates: 1=+10, 2=+15, 3+=+20 points
  - Duration > 7 days: +15 points (only for active reports)
  - Capped at 100
  
- `calculate_duration_days(created_at, current_status) → int`
  - Returns days open for active reports
  - Returns 0 for resolved/closed

- `should_recalculate_priority(...) → tuple(bool, int)`
  - Determines if priority should be recalculated based on duration
  - Returns (should_recalc, new_priority)
  - Only applies to active reports

**database.py - Supabase Query Interface**
- `save_report(report_data: dict, access_token: str) → list`
  - Inserts report into reports table
  - Respects RLS (only student can insert own)

- `get_all_reports(access_token: str) → list`
  - Fetches all reports (filtered by RLS)
  - Computes duplicate_count for each report

- `get_report_by_id(report_id: str, access_token: str) → list`
  - Fetches specific report
  - RLS applies

- `update_report_status(report_id: str, new_status: str, access_token: str) → list`
  - Updates status column
  - Admin-only via RLS

- `add_status_history(report_id, old_status, new_status, changed_by, access_token) → list`
  - Inserts status change record

- `get_status_history(report_id, access_token) → list`
  - Fetches status history ordered by time

- `get_active_reports(access_token: str) → list`
  - Returns reports where status != Resolved and != Closed
  - Used for duplicate detection

- `save_duplicate_relationship(report_id, duplicate_of_report_id, similarity_score, access_token) → list`
  - Records duplicate relationship

- `get_duplicate_count(report_id, access_token) → int`
  - Counts how many reports are marked as duplicates of this report

- `update_report_priority(report_id, new_priority, access_token) → list`
  - Updates priority_score column

- `get_reports_for_priority_update(access_token: str) → list`
  - Gets active reports for daily recalculation

**auth.py - Authentication & Authorization**
- `get_authenticated_user(current_user: dict = Depends(...)) → dict`
  - FastAPI dependency that verifies JWT token
  - Returns user dict with id, admin_flag

- `get_student_user(...) → dict`
  - Dependency for student endpoints
  - Same as authenticated_user (any logged-in user)

- `get_admin_user(...) → dict`
  - Dependency for admin endpoints
  - Verifies admin_flag in JWT is true
  - Raises 403 if not admin

---

## 6. Key Algorithms

### 6.1 AI Issue Analysis Algorithm

**Input:** Natural language description (e.g., "Wi-Fi in Library not working for past 3 days")

**Process:**
```
1. Send description + detailed prompt to Gemini 3.6 Flash
   Prompt includes:
   - Category definitions (Network, Facilities, Security, etc.)
   - Severity guidelines (Low/Medium/High/Critical with examples)
   - Instructions to return JSON only
   
2. Gemini analyzes and returns JSON:
   {
     "summary": "...",
     "category": "Network",
     "severity": "High",
     "extracted_location": "Library",
     "recommended_department": "IT Department",
     "safety_flag": false,
     "accessibility_flag": false,
     "confidence": 0.92
   }
   
3. If API error (429, timeout, etc.):
   Return fallback: { category: "Uncategorized", severity: "Medium", confidence: 0.5, ... }
```

**Output:** Dictionary with analysis fields or fallback

**Error Handling:** Try/except catches all Gemini exceptions, logs them, returns fallback

**Confidence Scoring:** Gemini provides confidence 0-1; fallback uses 0.5

---

### 6.2 Duplicate Detection Algorithm

**Input:** 
- New description: "Lab building Wi-Fi down"
- Category: "Network"
- Location: "Lab Building"
- Existing active reports: [Report1, Report2, Report3, ...]

**Process:**
```
FOR EACH existing_report IN active_reports:
  1. Get embedding for existing_report description/summary
     existing_embedding = get_embedding(existing_report.description)
  
  2. Get embedding for new description
     new_embedding = get_embedding(new_description)
  
  3. Compute semantic similarity
     semantic_score = cosine_similarity(new_embedding, existing_embedding)
     // Range: 0-1, where 1 = identical meaning
  
  4. Check metadata matches
     category_match = (new_category == existing_category)
     location_match = (new_location IN existing_location OR vice versa)
  
  5. Compute final score with metadata boosts
     final_score = semantic_score
     IF category_match: final_score += 0.05
     IF location_match: final_score += 0.10
     final_score = min(final_score, 1.0)
  
  6. Track best match
     IF final_score > best_score:
        best_score = final_score
        best_report = existing_report

AFTER loop:
  Determine if duplicate:
  is_duplicate = (best_score >= 0.80)
              OR (best_score >= 0.72 AND (category_match OR location_match))
  
  RETURN {
    "is_duplicate": is_duplicate,
    "duplicate_report_id": best_report.id IF is_duplicate ELSE null,
    "similarity_score": best_score,
    "duplicate_priority": best_report.priority_score IF is_duplicate ELSE null
  }
```

**Example:**
- New: "Library Wi-Fi not working", category "Network", location "Library"
- Existing1: "Internet down in Library", category "Network", location "Library", priority 65
  - semantic_score: 0.88
  - category_match: true (+0.05)
  - location_match: true (+0.10)
  - final: 0.88 + 0.05 + 0.10 = 1.03 → capped at 1.0
  - **is_duplicate: YES** (>= 0.80)

- Existing2: "Lab building AC broken", category "Facilities", location "Lab Building"
  - semantic_score: 0.42
  - category_match: false
  - location_match: false
  - final: 0.42
  - is_duplicate: NO

**Best Match:** Existing1 with score 1.0 and priority 65

---

### 6.3 Priority Scoring Algorithm

**Input:**
- severity: "High"
- safety_flag: false
- accessibility_flag: true
- duplicate_count: 2
- created_at: "2024-01-08T10:00:00Z" (8 days ago)
- current_status: "Under Review"

**Process:**
```
1. Base severity score
   score = severity_scores.get("High", default=25)
   // Low=25, Medium=50, High=70, Critical=90
   score = 70

2. Safety impact
   IF safety_flag: score += 20
   // Current: 70 (no change)

3. Accessibility impact
   IF accessibility_flag: score += 15
   score = 70 + 15 = 85

4. Duplicate impact
   IF duplicate_count >= 3: score += 20
   ELIF duplicate_count == 2: score += 15
   ELIF duplicate_count == 1: score += 10
   // duplicate_count == 2
   score = 85 + 15 = 100

5. Duration impact (only for active reports)
   IF created_at AND current_status NOT IN ["Resolved", "Closed"]:
     days_open = NOW - created_at
     IF days_open > 7: score += 15
   // 8 days open, but already at 100 (capped)
   score = min(100, 100 + 15) = 100

6. Cap at 100
   final_score = min(score, 100)
   final_score = 100
```

**Output:** 100 (maximum priority)

**Example 2 - New Report:**
- severity: "Medium"
- safety_flag: false
- accessibility_flag: false
- duplicate_count: 0
- created_at: "2024-01-16T14:00:00Z" (just created)
- current_status: "Submitted"

```
Base: 50
Safety: 0
Accessibility: 0
Duplicates: 0
Duration: 0
Final: 50
```

---

### 6.4 Priority Recalculation Algorithm (Daily Job)

**Purpose:** Boost priority scores based on duration for reports open > 7 days

**Input:** Called once daily (e.g., 2 AM)

**Process:**
```
1. get_reports_for_priority_update() → All reports where status NOT IN ["Resolved", "Closed"]

2. FOR EACH report:
   a. should_recalculate_priority(
        severity, safety_flag, accessibility_flag, duplicate_count,
        created_at, current_status, current_priority
      ) → Returns (should_recalc, new_priority)
   
   b. The function recalculates as if duration >= 7 days
      This adds 15 points if duration check passes
   
   c. IF new_priority > current_priority:
        update_report_priority(report_id, new_priority)
        recalc_count += 1
      ELSE:
        no_change_count += 1

3. RETURN { recalculated: recalc_count, unchanged: no_change_count, total: len(reports) }
```

**Example:**
- Report created 10 days ago with priority 70
- Recalculation adds 15 for duration > 7 days
- New priority: 70 + 15 = 85
- Database updated, recalc_count += 1

---

## 7. Security Design

### 7.1 Authentication

**Token Source:** Supabase Auth provides JWT tokens

**Token Structure (JWT):**
```
{
  "sub": "user_uuid",
  "aud": "authenticated",
  "iat": 1234567890,
  "exp": 1234571490,
  "admin_flag": "true" OR absent
}
```

**Token Usage:**
- Frontend stores token in secure context (Supabase SDK handles this)
- Frontend sends token in Authorization header: `Authorization: Bearer <token>`
- Backend verifies token signature and expiry with Supabase public key

**Session Expiry:**
- Default: 1 hour
- Refresh token handled by Supabase SDK on frontend
- Expired tokens trigger redirect to login

**Multi-Device Security:**
- Each device gets separate token
- Logout on one device doesn't affect others
- Typical for SPA apps

### 7.2 Authorization

**Role-Based Access Control (RBAC):**

Admin flag in JWT determines access:
- **Student endpoints** (ReportIssue, MyReports):
  - `GET_AUTHENTICATED_USER` dependency
  - Any logged-in user can access
  - RLS filters own data automatically

- **Admin endpoints** (AdminDashboard, CampusPulse, StatusUpdate):
  - `GET_ADMIN_USER` dependency
  - Checks `admin_flag == "true"` in JWT
  - Raises 403 Forbidden if not admin
  - RLS allows access to all data

**Frontend Authorization:**
- `ProtectedRoute` component checks auth state and admin flag
- Shows student pages only to students
- Shows admin dashboard only to admins
- Redirects unauthenticated to login

### 7.3 Row-Level Security (RLS)

**Database-Level Access Control:**

RLS policies enforce data access at database level, preventing even compromised tokens from accessing unauthorized data.

**Reports Table Policies:**
1. SELECT: `(auth.uid() = student_id) OR (admin_flag = 'true')`
   - Students see only own reports
   - Admins see all reports
   
2. INSERT: `auth.uid() = student_id`
   - Only the student can create their own report
   - Prevents one user impersonating another

3. UPDATE: `admin_flag = 'true'`
   - Only admins can update reports (status, priority)
   - Prevents students modifying their own data

**Status History Table Policies:**
1. SELECT: `(SELECT student_id FROM reports WHERE id = report_id) = auth.uid() OR (admin_flag = 'true')`
   - Students see history for their reports
   - Admins see any history

**Duplicate Relationships Table:**
- Implicit RLS via reports table
- Accessible only through reports a user can already access

**Key Principle:** RLS is enforced by PostgreSQL, not application logic. A token that somehow bypassed application auth would still be blocked by RLS.

### 7.4 API Security

**CORS Configuration:**
- Allowed origins: http://localhost:5173, http://127.0.0.1:5173, https://campuslens-ai.vercel.app
- Credentials enabled (for Bearer token support)
- Methods: All, Headers: All
- Prevents unauthorized cross-site requests

**API Key Management:**
- GEMINI_API_KEY stored only in backend .env (never in frontend)
- Backend uses Supabase service role key (never exposed to frontend)
- Frontend uses Supabase anon key with RLS to limit scope

**HTTPS Enforcement:**
- All communication encrypted
- Frontend on Vercel: HTTPS enforced
- Backend on Render: HTTPS enforced
- Database connections: TLS/SSL required

**Rate Limiting:**
- Implemented at infrastructure level (Render, CDN)
- Prevents API abuse
- Gemini API has built-in rate limits

**Input Validation:**
- Pydantic models validate request bodies
- Invalid input returns 400 Bad Request with clear error
- Description length limits (to prevent abuse)

**Error Messages:**
- User-friendly messages shown to clients
- Actual error details logged server-side for debugging
- No technical details exposed (SQL errors, file paths, etc.)

---

## 8. Error Handling Strategy

### 8.1 Gemini API Failures

**Scenario:** Gemini API returns 429, times out, or has connection error

**Handling:**
```
TRY:
  response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
  // Parse and return analysis
CATCH ResourceExhausted (429):
  logger.error("Gemini API 429 Resource Exhausted: ...")
  RETURN fallback_analysis()
CATCH DeadlineExceeded (timeout):
  logger.error("Gemini API Deadline Exceeded: ...")
  RETURN fallback_analysis()
CATCH GoogleAPIError:
  logger.error("Gemini API error: ...")
  RETURN fallback_analysis()
CATCH Exception:
  logger.error("Unexpected error during AI analysis: ...")
  RETURN fallback_analysis()
```

**User Experience:**
- Report submission succeeds with fallback analysis
- Frontend shows indication that AI was unavailable
- Student receives issue ID and can track submission

**Admin Debugging:**
- Actual error logged with full stack trace
- Admins can review logs to identify issues
- No raw errors exposed to students

**Fallback Structure:**
```json
{
  "summary": "AI analysis unavailable",
  "category": "Uncategorized",
  "severity": "Medium",
  "recommended_department": "Campus Facilities",
  "extracted_location": null,
  "safety_flag": false,
  "accessibility_flag": false,
  "confidence": 0.5
}
```

### 8.2 Database Errors

**Common Errors:**
- Validation error (invalid category): 400 Bad Request
- Record not found: 404 Not Found
- Permission denied (RLS block): 403 Forbidden
- Connection error: 500 Internal Server Error (logged)

**Handling:**
```
TRY:
  result = supabase.table("reports").insert(data).execute()
CATCH HTTPException:
  // Re-raise HTTP exceptions (404, 400, etc.)
  RAISE
CATCH Exception as error:
  logger.error(f"Database error: {error}")
  RAISE HTTPException(status_code=500, detail="Database operation failed")
```

**User Message:**
- Specific: "Report not found" (404)
- Specific: "Invalid status value" (400)
- Generic: "Database operation failed" (500)

---

### 8.3 Frontend Error Handling

**Network Errors:**
```
TRY:
  response = await fetch('/api/reports', { headers: { Authorization: `Bearer ${token}` } })
  data = await response.json()
CATCH NetworkError:
  showError("Failed to connect. Please check your internet and try again.")
  showRetryButton()
CATCH:
  IF response.status === 401:
    redirectToLogin()
  ELSE IF response.status === 403:
    showError("You don't have permission to view this.")
  ELSE IF response.status === 404:
    showError("Report not found.")
  ELSE IF response.status === 500:
    showError("Server error. Please try again later.")
```

**Gemini Unavailable Detection:**
```
IF response.analysis.confidence === 0.5 AND response.analysis.category === "Uncategorized":
  showWarning("AI analysis temporarily unavailable. Results generated using basic analysis.")
```

**Validation Error Display:**
```
IF response.error.field === "description":
  highlightField("description")
  showFieldError("Description is required and must be at least 10 characters")
```

---

## 9. Performance Considerations

### 9.1 Frontend Performance

**Build Optimization:**
- Vite tree-shaking removes unused code
- React code splitting via React Router (lazy loading pages)
- Production build: minified, optimized, ~150KB gzipped

**Runtime Optimization:**
- React.memo on chart components to prevent unnecessary re-renders
- useMemo for expensive computations (duplicate detection scoring)
- Recharts optimized for large datasets

**CSS Performance:**
- Tailwind CSS purges unused styles
- CSS-in-JS minimized via CSS modules
- No render-blocking CSS

**API Call Optimization:**
- Frontend caching of reports list (1 minute TTL)
- Pagination for large datasets
- Lazy load analytics/Campus Pulse on request

### 9.2 Backend Performance

**FastAPI Optimizations:**
- Async request handling with Uvicorn (concurrent requests)
- No blocking I/O operations
- Connection pooling to Supabase
- Dependency injection caches services

**Database Optimization:**
- Indexes on frequently queried columns: student_id, category, status, priority_score, created_at
- Supabase connection pooling
- Partitioning for large tables (future enhancement)

**Gemini API Optimization:**
- No caching of embeddings (would require storage)
- Campus Pulse cached for 30 minutes per date_range
- No retries by default (fail fast)

**Query Optimization:**
```
-- Efficient queries with indexes
SELECT * FROM reports WHERE student_id = ? AND status != 'Resolved' -- Uses indexes
SELECT * FROM reports WHERE created_at > NOW() - INTERVAL '7 days' -- Indexed by created_at
```

### 9.3 Performance Targets

**API Response Times:**
- POST /reports (issue submission): < 5 seconds (95th percentile)
  - Includes Gemini API call + embedding + duplicate check + database insert
- GET /reports (list): < 2 seconds (95th percentile)
- GET /analytics/campus-pulse: < 15 seconds (includes Gemini call, cached after)
- PUT /reports/{id}/status: < 1 second

**Concurrent Users:**
- Designed to handle 100 concurrent users without degradation
- Render auto-scaling handles traffic spikes
- Supabase managed database auto-scales

---

## 10. Deployment Architecture

### 10.1 Frontend Deployment (Vercel)

**Deployment Process:**
1. Push to main branch on GitHub
2. Vercel webhook triggers build
3. npm run build → dist/ directory
4. Vercel serves from global CDN
5. HTTPS enforced

**Environment Variables:**
- `VITE_API_URL` - Backend API URL (https://campuslens-ai.onrender.com)
- `VITE_SUPABASE_URL` - Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Supabase anonymous API key (limited via RLS)

**Build Configuration:**
```javascript
// vite.config.js
import react from '@vitejs/plugin-react'

export default {
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'terser',
    sourcemap: false // Disable for production
  }
}
```

**Serving:**
- Static asset serving from CDN
- Automatic gzip compression
- 404 handling for SPA routing (rewrite to index.html)

### 10.2 Backend Deployment (Render)

**Deployment Process:**
1. Push to main branch on GitHub
2. Render webhook triggers build
3. pip install -r backend/requirements.txt
4. Start: uvicorn main:app --host 0.0.0.0 --port $PORT
5. Auto-scaled based on CPU/memory usage

**Environment Variables:**
- `GEMINI_API_KEY` - Google Gemini API key (sensitive)
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase service role key (sensitive)

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
```

**Auto-Scaling:**
- Render monitors CPU and memory
- Scales horizontally (more instances) under load
- Scales down during low traffic

**Health Check:**
- GET /health endpoint returns { "status": "healthy" }
- Render pings endpoint periodically

### 10.3 Database Deployment (Supabase)

**Database Service:**
- Managed PostgreSQL with automated backups
- Automatic failover
- Point-in-time restore available

**pgvector Extension:**
- Enabled for embedding storage (if needed in future)
- Currently embeddings computed on-demand

**Backups:**
- Automatic daily backups
- 30-day retention
- Point-in-time restore available

**Monitoring:**
- Supabase dashboard shows query performance
- Slow query logs available for optimization

---

## 11. Testing Strategy

### 11.1 Frontend Testing

**Unit Tests (React Testing Library):**
- ProtectedRoute component blocks unauthenticated access
- ReportIssue form validates description input
- AdminDashboard filters update issue list correctly
- StatusHistory displays status changes chronologically

**Integration Tests (MSW mocking):**
- Full report submission flow with mocked API
- Login → Submit Issue → See Report in MyReports
- Admin filters and status updates
- Error scenarios (network error, API error)

**E2E Tests (Cypress/Playwright, optional):**
- Complete student workflow: register → submit → track
- Complete admin workflow: login → filter → update → view pulse
- Cross-browser testing

### 11.2 Backend Testing

**Unit Tests (pytest):**
- analyze_issue() returns fallback on 429 error
- find_best_duplicate() correctly scores similarity
- calculate_priority_score() applies all bonuses correctly
- duplicate detection with embedding similarity

**Integration Tests (FastAPI TestClient):**
- POST /reports full flow
- GET /reports with RLS filtering
- PUT /reports/{id}/status audit trail creation
- GET /analytics/campus-pulse with fallback

**Mocking Strategy:**
- Mock Gemini API responses (simulate success, 429, timeout)
- Mock Supabase with in-memory database (optional)
- Mock embeddings for deterministic duplicate detection

### 11.3 AI Services Testing

**Fallback Handling:**
- Gemini 429 → fallback analysis returned
- Gemini timeout → fallback analysis returned
- Gemini connection error → fallback analysis returned

**Duplicate Detection:**
- Random descriptions → correct semantic scoring
- Same category/location → bonus applied
- Edge cases: empty description, very long description

---

## 12. Known Limitations & Future Improvements

### 12.1 Current Limitations

**Fallback Analysis Quality:**
- Fallback uses basic keyword extraction, not true AI analysis
- Always returns "Uncategorized" and "Medium" severity
- Confidence score fixed at 0.5 (vs. 0.9+ for AI)
- Impacts priority scoring when Gemini unavailable

**Stateless Analysis:**
- Each issue analyzed independently
- No context from student's previous issues
- Can't learn from campus-wide patterns in individual analysis

**No Multi-Language Support:**
- All prompts and categories in English
- Students speaking other languages must describe in English

**Campus Pulse Real-Time:**
- Cached for 30 minutes, not real-time
- Manual refresh required or scheduled job (not yet implemented)

**No Mobile App:**
- Only web-based access
- Could benefit from native iOS/Android apps

**Limited Location Data:**
- Locations extracted as text, not structured coordinates
- No map visualization or geographic clustering

### 12.2 Future Improvements

**Machine Learning Fallback:**
- Train custom ML model for category/severity classification
- Use campus-wide historical data to improve accuracy
- Gradually improve as more data collected

**Persistent Conversation:**
- Multi-turn dialogue for clarification ("Which building?")
- Reduce back-and-forth between student and admin

**Multi-Language Support:**
- Translate descriptions to English internally
- Support prompts in multiple languages
- Serve diverse campus population

**Real-Time Campus Pulse:**
- Schedule background job to regenerate Campus Pulse hourly
- Update admin dashboard in real-time
- Push notifications for critical issues

**Mobile Apps:**
- React Native app for iOS/Android
- Offline submission with sync when online
- Push notifications for status updates

**Advanced Location Handling:**
- Map-based location picker
- GPS coordinates in mobile app
- Geographic heatmaps in analytics

**Predictive Analytics:**
- Predict resolution time based on category/severity
- Recommend resource allocation
- Identify systemic issues requiring infrastructure investment

**Workflow Automation:**
- Automatic email notifications for status changes
- Escalation rules (auto-flag if unresolved > 14 days)
- Department integration (forward to maintenance system)

**Multi-Campus Support:**
- Support multiple university campuses
- Cross-campus trend analysis
- Campus-specific category customization

---

## Conclusion

CampusLens AI provides a comprehensive, intelligent, and scalable solution for campus issue management. By combining modern technologies (React, FastAPI, Supabase, Gemini) with proven architectural patterns (RLS for security, embeddings for intelligence, priority algorithms for triage), the system delivers value to both students (simple submission and tracking) and administrators (complete visibility and data-driven insights).

The system gracefully handles AI service failures through fallback analysis, ensuring students can always submit issues and administrators can always triage and respond. Production deployment on Vercel, Render, and Supabase provides reliability, performance, and scalability to support growing campus populations.