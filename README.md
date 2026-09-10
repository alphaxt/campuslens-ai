# CampusLens AI

**AI-powered campus issue intelligence and resolution platform**

Transform how campus communities identify, analyze, and resolve campus issues through intelligent AI analysis, duplicate detection, and automated priority scoring.

---

## Table of Contents

1. [Overview](#overview)
2. [Problem Being Solved](#problem-being-solved)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [User Workflows](#user-workflows)
6. [Technology Stack](#technology-stack)
7. [Local Development Setup](#local-development-setup)
8. [Environment Variables](#environment-variables)
9. [Production Deployment](#production-deployment)
10. [API Reference](#api-reference)
11. [Technical Deep Dives](#technical-deep-dives)
12. [Screenshots](#screenshots)
13. [Live Demo](#live-demo)
14. [Repository](#repository)
15. [License](#license)
16. [Built With](#built-with)

---

## Overview

CampusLens AI is a full-stack application that empowers university communities to report, analyze, and resolve campus issues collaboratively. Students submit issues through an intuitive interface, while Gemini AI analyzes each report in real-time, categorizes it, assesses severity, and identifies duplicates using advanced embedding-based similarity detection.

### Value Proposition

- **Intelligent Triage**: Gemini AI automatically analyzes reports and extracts structured data
- **Duplicate Prevention**: Embedding-based matching prevents redundant submissions with 0.80+ similarity threshold
- **Smart Prioritization**: Dynamic priority scoring considers severity, safety, accessibility, duration, and community engagement
- **Admin Transparency**: Campus leadership gains real-time visibility into campus health through analytics and AI-generated insights
- **Accountability**: Complete audit trail with status history and admin tracking

---

## Problem Being Solved

University campuses face fragmented issue reporting:
- Students lack a unified platform to report problems
- Campus teams cannot quickly identify high-impact issues or prevent duplicate reports
- No intelligent triage means critical issues may be deprioritized
- No visibility into campus-wide trends or emerging problems

CampusLens AI solves this by creating a centralized, AI-powered issue intelligence system that benefits both students and campus administration.

---

## Key Features

### For Students
✓ **Easy Issue Reporting** - Intuitive web form for submitting campus problems  
✓ **AI Analysis** - Automatic issue categorization, severity assessment, location extraction  
✓ **Duplicate Detection** - Notified when similar issues already exist  
✓ **Personal Dashboard** - Track submitted reports and their status in real-time  
✓ **Authentication** - Secure login via Supabase Auth  

### For Campus Administrators
✓ **Admin Dashboard** - Comprehensive view of all campus reports  
✓ **Advanced Filtering** - Sort by category, severity, status, date, priority score  
✓ **Analytics & Charts** - Visualize issue distribution and trends  
✓ **Campus Pulse AI** - AI-generated insights about overall campus health  
✓ **Status Management** - Update issue status (Submitted → Under Review → In Progress → Resolved → Closed)  
✓ **Status History** - Complete audit trail with timestamps and admin tracking  
✓ **Priority Recalculation** - Scheduled daily recalculation based on duration and engagement  
✓ **Role-Based Access** - Student vs. admin permissions enforced via Supabase RLS  

### Issue Categories
- **Network** - Wi-Fi, internet, connectivity problems
- **Facilities** - Electricity, AC, plumbing, furniture, building infrastructure
- **Security** - Theft, unsafe situations, security concerns
- **Cleanliness** - Trash, sanitation, cleaning problems
- **Transport** - Buses, parking, campus transportation
- **Accessibility** - Barriers affecting disabled or mobility-impaired people
- **Academic Facilities** - Projectors, computers, labs, classroom equipment

### Severity Levels
- **Low** - Cosmetic inconvenience (e.g., broken clock, minor furniture issue)
- **Medium** - Noticeable disruption but alternatives exist (e.g., one lab projector unavailable)
- **High** - Significant disruption affecting classes/services (e.g., network outage in lab)
- **Critical** - Immediate safety risk or emergency (e.g., exposed electrical wiring, fire hazard)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Vercel)                        │
│  React 19 + Vite 8 + Tailwind CSS 4 + React Router 7           │
│  ├── Student Portal (Report Form, My Reports)                  │
│  ├── Admin Dashboard (Analytics, Status Management)            │
│  └── Authentication (Supabase Auth)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
                    (CORS-protected HTTPS)
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (Render)                         │
│  FastAPI 0.112+ + Uvicorn + Python 3.10+                       │
│  ├── POST /reports (Analysis + Duplicate Detection)            │
│  ├── GET /reports (List all reports)                           │
│  ├── GET /reports/{id} (Specific report)                       │
│  ├── PUT /reports/{id}/status (Admin status update)            │
│  ├── GET /reports/{id}/history (Status audit trail)            │
│  ├── GET /analytics/campus-pulse (AI insights)                 │
│  └── POST /priority/recalculate (Daily priority update)        │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
                   (Authenticated Requests)
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (Supabase PostgreSQL)                │
│  ├── reports (All student submissions)                         │
│  ├── report_status_history (Audit trail)                       │
│  ├── duplicate_reports (Relationship tracking)                 │
│  └── RLS Policies (Student/Admin role enforcement)             │
│                                                                 │
│  pgvector Extension for AI Embeddings                          │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
                   (Authenticated Requests)
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│                    AI SERVICES (Google Cloud)                   │
│  ├── Gemini 3.6 Flash (Issue analysis, Campus Pulse)           │
│  └── Gemini Embeddings 2 (Duplicate detection)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow: Creating a Report

```
1. Student submits issue → Frontend validates input
2. Frontend sends to Backend API (authenticated)
3. Backend calls Gemini 3.6 Flash for analysis (with 429/timeout fallback)
4. Backend retrieves active reports from Supabase
5. Backend generates embeddings for all reports using Gemini Embeddings 2
6. Backend compares similarity scores (0.80+ threshold = duplicate)
7. Backend calculates priority score (severity + flags + duration + duplicates)
8. Backend saves report to Supabase with RLS enforcement
9. If duplicate: saves duplicate_reports relationship and updates original priority
10. Backend returns analysis to Frontend
11. Frontend displays results to student
```

---

## User Workflows

### Student Workflow

```
1. Student visits CampusLens AI
2. Clicks "Register" if first-time user
3. Provides email and password (Supabase Auth)
4. Logs in to student dashboard
5. Clicks "Report Issue"
6. Fills out form:
   - Issue description (required, free text)
   - Category (optional - AI will auto-detect)
   - Location (optional - AI will extract)
7. Submits form
8. AI analysis runs (category, severity, department, flags)
9. Duplicate detection runs (compares to active reports)
10. Results shown to student:
    - AI analysis (category, severity, location, department)
    - If duplicate: link to original report + similarity score
    - Priority score explanation
11. Report saved to "My Reports" dashboard
12. Student can track status changes in real-time
```

### Admin Workflow

```
1. Admin logs in with admin-marked Supabase account
2. Accessed Admin Dashboard (RLS enforces admin-only access)
3. Views default: all reports with filters
   - Filter by category, severity, status, date range
   - Sort by priority score (highest first)
4. Clicks on report to view details:
   - Original student description
   - AI analysis (summary, category, severity, location, department)
   - Safety/accessibility flags
   - Duplicate count and relationships
   - Full status history with timestamps
   - Recommended department for routing
5. Updates status if needed (Submitted → Under Review → In Progress → Resolved → Closed)
   - System logs status change with admin ID and timestamp
6. Views analytics:
   - Charts showing issues by category, severity, status
   - Trend analysis over time
   - Most critical issues highlighted
7. Generates Campus Pulse:
   - Clicks "Campus Pulse" to view AI-generated insights
   - Reads headline, executive summary, major concern, trends
   - Reviews AI-recommended actions
   - Uses data to prioritize campus maintenance efforts
8. Runs priority recalculation:
   - Triggered via POST /priority/recalculate (typically via cron job)
   - Reports open for 7+ days automatically increase priority
   - Updated priorities reflect in admin dashboard
```

---

## Technology Stack

### Frontend
| Layer | Technology | Version |
|-------|-----------|---------|
| Runtime | Node.js | 18+ |
| Build Tool | Vite | 8.2.2 |
| UI Framework | React | 19.2.8 |
| Styling | Tailwind CSS | 4.3.3 |
| Routing | React Router | 7.18.2 |
| Charts | Recharts | 3.10.1 |
| Backend Client | Supabase JS | 2.112.4 |
| Package Manager | npm | Latest |

### Backend
| Layer | Technology | Version |
|-------|-----------|---------|
| Runtime | Python | 3.10+ |
| Web Framework | FastAPI | Latest |
| Server | Uvicorn | Latest |
| Validation | Pydantic | Latest |
| Config | python-dotenv | Latest |
| Database Client | Supabase | Latest |
| AI | google-genai | Latest |

### Database & Infrastructure
| Service | Technology | Purpose |
|---------|-----------|---------|
| Database | Supabase PostgreSQL | Central data storage with RLS |
| Vector DB | pgvector (PostgreSQL extension) | Embedding storage for duplicate detection |
| Auth | Supabase Auth (JWT) | User authentication and role management |
| Frontend Deployment | Vercel | Zero-config React/Node.js hosting |
| Backend Deployment | Render | Python/FastAPI hosting with auto-scaling |
| AI Models | Google Gemini 3.6 Flash | Issue analysis and Campus Pulse generation |
| AI Embeddings | Google Gemini Embeddings 2 | Text embeddings for duplicate detection |

---

## Local Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Supabase account (free tier available)
- Google Cloud account with Gemini API enabled
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/campuslens-ai.git
cd campuslens-ai
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env template and add your credentials
cp .env.example .env
# Edit .env with your API keys (see Environment Variables section)
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
npm install

# Copy .env template and add your credentials
cp .env.example .env
# Edit .env with your configuration (see Environment Variables section)
```

### Step 4: Supabase Configuration

1. Create a new Supabase project at https://supabase.com
2. Create tables (SQL below):

```sql
-- Create reports table
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL,
  original_description TEXT NOT NULL,
  ai_summary TEXT,
  category VARCHAR(50),
  severity VARCHAR(20),
  extracted_location TEXT,
  recommended_department TEXT,
  priority_score INTEGER DEFAULT 50,
  status VARCHAR(20) DEFAULT 'Submitted',
  is_safety_flag BOOLEAN DEFAULT FALSE,
  is_accessibility_flag BOOLEAN DEFAULT FALSE,
  confidence NUMERIC(3,2),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create status history table
CREATE TABLE report_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES reports(id),
  old_status VARCHAR(20),
  new_status VARCHAR(20),
  changed_by UUID NOT NULL,
  changed_at TIMESTAMP DEFAULT NOW()
);

-- Create duplicate relationships table
CREATE TABLE duplicate_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES reports(id),
  duplicate_of_report_id UUID NOT NULL REFERENCES reports(id),
  similarity_score NUMERIC(4,4),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_status_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE duplicate_reports ENABLE ROW LEVEL SECURITY;

-- RLS Policies (see Security & RLS section for details)
```

3. Set up authentication roles in Supabase Auth
4. Copy credentials to `.env` files

### Step 5: Run Development Servers

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload

# Backend will run on http://localhost:8000
# API docs available at http://localhost:8000/docs

# Terminal 2: Frontend
cd frontend
npm run dev

# Frontend will run on http://localhost:5173
```

### Verify Installation

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Environment Variables

### Backend (.env)

```bash
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Optional: Server Configuration
# PORT=8000
# WORKERS=4
```

**Getting Your API Keys:**

1. **Gemini API Key**: https://ai.google.dev/
   - Create a Google Cloud project
   - Enable Gemini API
   - Generate an API key

2. **Supabase URL & Key**: https://supabase.com/
   - Create a new project
   - Navigate to Settings → API
   - Copy project URL and `anon` key

### Frontend (.env)

```bash
# Backend API Endpoint
VITE_API_URL=http://localhost:8000

# Supabase Configuration (must match backend)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

---

## Production Deployment

### Deployment Architecture

```
Frontend (Vercel)
  ↓
Backend (Render)
  ↓
Database (Supabase)
```

### Deploy Frontend to Vercel

1. Push code to GitHub
2. Connect GitHub repo to Vercel: https://vercel.com/new
3. Configure environment variables in Vercel settings
4. Deploy (automatic on git push to main)

**Vercel Environment Variables:**
```
VITE_API_URL=https://campuslens-backend.onrender.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### Deploy Backend to Render

1. Push code to GitHub
2. Create new Web Service on Render: https://render.com/dashboard
3. Connect GitHub repo and select repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.10
5. Add environment variables in Render dashboard

**Render Environment Variables:**
```
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

### Configure Supabase for Production

1. Update CORS in Supabase settings to allow Vercel domain
2. Verify RLS policies are properly configured
3. Set up daily cron job to call `/priority/recalculate`

**Daily Priority Recalculation (Recommended Setup):**
- Use Render's cron or external service (e.g., EasyCron)
- Call: `POST https://campuslens-backend.onrender.com/priority/recalculate`
- Include admin authentication token

---

## API Reference

All endpoints require authentication via JWT token (from Supabase Auth) passed in `Authorization: Bearer {token}` header.

### 1. Create Report (Submit Issue)

**Endpoint:** `POST /reports`  
**Auth Required:** Yes (Student role)  
**Rate Limit:** None currently

**Request:**
```json
{
  "description": "The Wi-Fi in Building A has been down for 3 hours and students cannot access online learning resources"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "report": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "student_id": "user-uuid",
      "original_description": "The Wi-Fi in Building A...",
      "ai_summary": "Network connectivity issue affecting student access",
      "category": "Network",
      "severity": "High",
      "extracted_location": "building a",
      "recommended_department": "IT Support",
      "priority_score": 85,
      "status": "Submitted",
      "is_safety_flag": false,
      "is_accessibility_flag": false,
      "confidence": 0.95,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "analysis": {
    "summary": "Network connectivity issue affecting student access",
    "category": "Network",
    "severity": "High",
    "recommended_department": "IT Support",
    "extracted_location": "building a",
    "safety_flag": false,
    "accessibility_flag": false,
    "confidence": 0.95
  },
  "duplicate": {
    "is_duplicate": false,
    "duplicate_report_id": null,
    "similarity_score": 0.0,
    "duplicate_priority": null
  }
}
```

**Example with Duplicate Detection:**
```json
{
  "success": true,
  "report": [...],
  "analysis": {...},
  "duplicate": {
    "is_duplicate": true,
    "duplicate_report_id": "550e8400-e29b-41d4-a716-446655440001",
    "similarity_score": 0.87,
    "duplicate_priority": 85
  }
}
```

---

### 2. List All Reports

**Endpoint:** `GET /reports`  
**Auth Required:** Yes (Student or Admin)  
**Auth Note:** Students see only their own reports; Admins see all

**Response (200 OK):**
```json
{
  "success": true,
  "count": 42,
  "reports": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "student_id": "user-uuid",
      "original_description": "...",
      "ai_summary": "...",
      "category": "Network",
      "severity": "High",
      "extracted_location": "building a",
      "recommended_department": "IT Support",
      "priority_score": 85,
      "status": "Under Review",
      "is_safety_flag": false,
      "is_accessibility_flag": false,
      "confidence": 0.95,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

---

### 3. Get Specific Report

**Endpoint:** `GET /reports/{report_id}`  
**Auth Required:** Yes (Student or Admin)  
**Auth Note:** Students can view only their own reports; Admins can view all

**Response (200 OK):**
```json
{
  "success": true,
  "report": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "student_id": "user-uuid",
    "original_description": "...",
    "ai_summary": "...",
    "category": "Network",
    "severity": "High",
    "extracted_location": "building a",
    "recommended_department": "IT Support",
    "priority_score": 85,
    "status": "Under Review",
    "is_safety_flag": false,
    "is_accessibility_flag": false,
    "confidence": 0.95,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  }
}
```

**Errors:**
- 404 Not Found: Report does not exist
- 403 Forbidden: Student trying to access another student's report

---

### 4. Update Report Status (Admin)

**Endpoint:** `PUT /reports/{report_id}/status`  
**Auth Required:** Yes (Admin only)

**Request:**
```json
{
  "status": "In Progress"
}
```

**Valid Status Values:**
- Submitted
- Under Review
- In Progress
- Resolved
- Closed

**Response (200 OK):**
```json
{
  "success": true,
  "report": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "In Progress",
    "updated_at": "2024-01-15T11:00:00Z"
  },
  "history": {
    "id": "550e8400-e29b-41d4-a716-446655440999",
    "report_id": "550e8400-e29b-41d4-a716-446655440000",
    "old_status": "Under Review",
    "new_status": "In Progress",
    "changed_by": "admin-user-id",
    "changed_at": "2024-01-15T11:00:00Z"
  }
}
```

---

### 5. Get Report Status History (Admin)

**Endpoint:** `GET /reports/{report_id}/history`  
**Auth Required:** Yes (Admin only)

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "history": [
    {
      "id": "history-uuid-1",
      "report_id": "550e8400-e29b-41d4-a716-446655440000",
      "old_status": null,
      "new_status": "Submitted",
      "changed_by": "system",
      "changed_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "history-uuid-2",
      "report_id": "550e8400-e29b-41d4-a716-446655440000",
      "old_status": "Submitted",
      "new_status": "Under Review",
      "changed_by": "admin-uuid-123",
      "changed_at": "2024-01-15T10:45:00Z"
    },
    {
      "id": "history-uuid-3",
      "report_id": "550e8400-e29b-41d4-a716-446655440000",
      "old_status": "Under Review",
      "new_status": "In Progress",
      "changed_by": "admin-uuid-456",
      "changed_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

### 6. Campus Pulse (AI Insights)

**Endpoint:** `GET /analytics/campus-pulse`  
**Auth Required:** Yes (Admin only)

**Response (200 OK):**
```json
{
  "success": true,
  "pulse": {
    "headline": "Network Issues Emerging as Major Concern",
    "summary": "42 total campus reports processed. Network infrastructure shows 8 related issues concentrated in academic buildings. Critical Wi-Fi outage in Building A has been escalated.",
    "major_concern": "Network infrastructure reliability affecting academic delivery",
    "emerging_trend": "8 reports in the 'Network' category suggest recurring connectivity issues",
    "critical_issue": "Wi-Fi outage in Building A - students cannot access learning resources",
    "improvement": "Facilities maintenance has resolved 3 cleanliness issues in the past week",
    "recommended_actions": [
      "Address critical Wi-Fi outage in Building A immediately",
      "Review network infrastructure for common points of failure",
      "Schedule IT department meeting to discuss redundancy options"
    ]
  }
}
```

**Fallback Response (when Gemini API unavailable):**
```json
{
  "success": true,
  "pulse": {
    "headline": "Campus Status: 8 Open Issues",
    "summary": "Total of 42 campus reports. 8 remain unresolved. Network infrastructure reliability affecting academic delivery.",
    "major_concern": "Network infrastructure reliability affecting academic delivery",
    "emerging_trend": "8 reports in the 'Network' category suggest a recurring issue.",
    "critical_issue": "Wi-Fi outage in Building A",
    "improvement": "No critical issues currently reported, which is a positive sign.",
    "recommended_actions": [
      "Address 1 critical issue(s) immediately.",
      "Review network infrastructure for common issues.",
      "Continue monitoring campus issues."
    ]
  }
}
```

---

### 7. Recalculate Priorities (Admin)

**Endpoint:** `POST /priority/recalculate`  
**Auth Required:** Yes (Admin only)  
**Recommended:** Call daily via cron job

**Request:**
```
(No request body required)
```

**Response (200 OK):**
```json
{
  "success": true,
  "recalculated": 5,
  "unchanged": 12,
  "total_active": 17
}
```

**What This Does:**
- Reviews all active (non-Resolved/Closed) reports
- Increases priority +15 for reports open 7+ days
- Updates priority scores that increased
- Returns count of updated and unchanged reports

---

### 8. Health Check

**Endpoint:** `GET /health`  
**Auth Required:** No

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## Technical Deep Dives

### AI Issue Analysis (Gemini 3.6 Flash)

#### How It Works

When a student submits an issue:

1. **Backend receives description** and sends to Gemini 3.6 Flash
2. **Gemini analyzes** using detailed prompt with:
   - Category definitions
   - Severity guidelines
   - Output format specification
3. **Returns structured JSON** with category, severity, location, department, flags
4. **Fallback mechanism** on 429 (rate limit) or timeout errors

#### Analysis Output

```json
{
  "summary": "Network connectivity issue affecting student access",
  "category": "Network",
  "severity": "High",
  "recommended_department": "IT Support",
  "extracted_location": "building a",
  "safety_flag": false,
  "accessibility_flag": true,
  "confidence": 0.95
}
```

#### Fallback Behavior

If Gemini API fails (429 rate limit, timeout, etc.), backend returns safe fallback:
- Uses keyword matching for category and department
- Extracts location using regex patterns
- Returns confidence: 0.0 to indicate uncertain analysis
- Never exposes raw error messages to frontend
- **System continues functioning** rather than failing

```json
{
  "summary": "Issue reported: [first 100 chars]",
  "category": "Uncategorized",
  "severity": "Medium",
  "recommended_department": "General Maintenance",
  "extracted_location": null,
  "safety_flag": false,
  "accessibility_flag": false,
  "confidence": 0.0
}
```

#### Severity Guidelines

| Level | Definition | Examples |
|-------|-----------|----------|
| Low | Cosmetic inconvenience, non-essential equipment | Broken classroom clock, minor furniture issue |
| Medium | Noticeable disruption but alternatives exist | One lab projector unavailable, slow Wi-Fi in small area |
| High | Significant disruption affecting classes/services | Network outage in lab, major AC failure, important facility unavailable |
| Critical | Immediate safety risk or emergency | Exposed electrical wiring, fire hazard, blocked emergency exit |

---

### Duplicate Detection (Gemini Embeddings 2)

#### How It Works

When creating a report:

1. **Get new report embedding** via Gemini Embeddings 2 API
2. **Get embeddings for all active reports** from database
3. **Calculate cosine similarity** between new report and each existing report
4. **Apply metadata matching** (category, location) to boost/confirm duplicates
5. **Return best match** if similarity >= 0.80 threshold

#### Similarity Scoring Formula

```
final_score = semantic_similarity

if same_category:
    final_score += 0.05

if same_location:
    final_score += 0.10

final_score = min(final_score, 1.0)

is_duplicate = (
    final_score >= 0.80
    OR (final_score >= 0.72 AND (category_match OR location_match))
)
```

#### Duplicate Detection Examples

**Example 1: Strong Semantic Match**
```
New:      "Wi-Fi down in Building A"
Existing: "No internet in Building A"
Semantic: 0.88
Category: Network = Network ✓
Location: building a = building a ✓

final_score = 0.88 + 0.05 + 0.10 = 1.0 (capped)
→ DUPLICATE (0.88 >= 0.80)
```

**Example 2: Semantic Match with Metadata**
```
New:      "Roof leaking in Library"
Existing: "Water dripping from ceiling"
Semantic: 0.75
Category: Facilities = Facilities ✓
Location: library = library ✓

final_score = 0.75 + 0.05 + 0.10 = 0.90
→ DUPLICATE (0.75 >= 0.72 AND category_match)
```

**Example 3: Not a Duplicate**
```
New:      "Building too cold"
Existing: "Parking lot floods in rain"
Semantic: 0.45
Category: Facilities = Facilities (same)
Location: null = null (no help)

final_score = 0.45 + 0.05 = 0.50
→ NOT DUPLICATE (0.50 < 0.80)
```

#### Duplicate Relationship Tracking

When duplicate detected:
- **New report** is linked to **original report** via `duplicate_reports` table
- **Original report priority increases** based on duplicate count
- **Duplicate count visible** on both reports in UI
- **Status updates propagate** - resolving original affects understanding of duplicates

---

### Priority Scoring

#### Scoring Algorithm

```
Base Score (Severity):
  Low     = 25
  Medium  = 50
  High    = 70
  Critical = 90

Modifiers:
  + 20 if Safety Flag
  + 15 if Accessibility Flag
  + 10 if 1 duplicate
  + 15 if 2 duplicates
  + 20 if 3+ duplicates
  + 15 if open 7+ days

Final Score: Capped at 100
```

#### Priority Scoring Examples

| Scenario | Severity | Safety | Access | Duration | Duplicates | Score |
|----------|----------|--------|--------|----------|-----------|-------|
| New electrical hazard (safety) | Critical (90) | Yes (+20) | No | 1 day | 0 | **100** |
| Classroom projector down | Low (25) | No | No | 3 days | 0 | **25** |
| Campus Wi-Fi outage (widespread) | High (70) | No | Yes (+15) | 5 days | 5 dupes (+20) | **100** |
| Broken elevator | Medium (50) | No | Yes (+15) | 8 days (+15) | 2 dupes (+15) | **100** |
| Minor cleanliness issue | Low (25) | No | No | 2 days | 1 dup (+10) | **35** |

#### Dynamic Priority Recalculation

Backend includes `/priority/recalculate` endpoint that:
- Runs daily (recommend via cron)
- Reviews all active reports
- Adds +15 for reports open 7+ days
- Updates reports that increased in priority
- Does not decrease priorities
- Provides count of updated reports

```bash
# Example: Call daily at 2 AM
# Via EasyCron or similar service
POST https://api.campuslens.com/priority/recalculate
Authorization: Bearer {admin_token}
```

---

### Security & Row-Level Security (RLS)

#### Authentication Flow

```
1. Student registers with Supabase Auth
   → Supabase returns JWT token
   
2. Frontend stores JWT in localStorage
   
3. All API requests include Authorization header:
   Authorization: Bearer {jwt_token}
   
4. Backend validates JWT signature
   → Extracts user_id and role from claims
   
5. Backend enforces authorization:
   → Students can only access their own data
   → Admins can access all data
```

#### RLS Policies

**Reports Table:**
```sql
-- Students can see only their own reports
CREATE POLICY student_read_own
  ON reports FOR SELECT
  USING (
    auth.uid() = student_id
    OR auth.jwt() ->> 'role' = 'admin'
  );

-- Students can insert only their own reports
CREATE POLICY student_insert_own
  ON reports FOR INSERT
  WITH CHECK (
    auth.uid() = student_id
  );

-- Only admins can update reports
CREATE POLICY admin_update
  ON reports FOR UPDATE
  USING (auth.jwt() ->> 'role' = 'admin');

-- Only admins can delete reports
CREATE POLICY admin_delete
  ON reports FOR DELETE
  USING (auth.jwt() ->> 'role' = 'admin');
```

**Status History Table:**
```sql
-- Authenticated users can read history
CREATE POLICY auth_read_history
  ON report_status_history FOR SELECT
  USING (
    auth.jwt() ->> 'role' IN ('admin', 'student')
  );

-- Only backend can insert (via authenticated admin requests)
CREATE POLICY admin_insert_history
  ON report_status_history FOR INSERT
  WITH CHECK (
    auth.jwt() ->> 'role' = 'admin'
  );
```

#### API-Level Authorization

Backend uses `get_admin_user()` and `get_student_user()` dependency functions:

```python
@app.get("/reports/{report_id}/history")
def report_status_history(
    report_id: str,
    current_user: dict = Depends(get_admin_user)  # Only admins
):
    # Implementation
    pass
```

#### Security Considerations

- **JWT expiration**: Supabase tokens expire after 1 hour
- **No secrets in frontend**: All API keys stored only in backend `.env`
- **CORS restricted**: Frontend can only call authenticated backend
- **Role-based access**: Enforced at DB level (RLS) and API level
- **Audit trail**: All status changes logged with admin ID
- **No hardcoded credentials**: All config via environment variables

---

## Screenshots

### Student Dashboard - Report Issue
```
[Screenshot showing the report submission form]
- Title: "Report a Campus Issue"
- Description input field (required)
- Category selector (optional - AI detects)
- Location input (optional - AI extracts)
- Submit button
```

### Student Dashboard - My Reports
```
[Screenshot showing list of student's submitted reports]
- Filter controls (status, category)
- Report cards with:
  - Issue title/summary
  - Category tag
  - Severity badge (color-coded)
  - Priority score
  - Status
  - Date submitted
  - Duplicate badge (if applicable)
```

### Admin Dashboard - All Reports
```
[Screenshot showing admin report management interface]
- Advanced filter panel (category, severity, status, date range)
- Sortable table with columns:
  - Priority Score (sortable)
  - Category
  - Severity
  - Status
  - Location
  - Department
  - Date
  - Duplicate Count
- Clickable rows for detail view
```

### Admin Dashboard - Report Detail
```
[Screenshot showing detailed report view]
- Original student description
- AI analysis (category, severity, location, department)
- Safety/Accessibility flags highlighted
- Duplicate information (if applicable)
- Status history timeline
- Status update dropdown
- Recommended actions
```

### Admin Dashboard - Analytics
```
[Screenshot showing analytics charts]
- Issues by Category (pie chart)
- Issues by Severity (bar chart)
- Issues by Status (donut chart)
- Issues over Time (line chart)
- Priority Score distribution (histogram)
```

### Admin Dashboard - Campus Pulse
```
[Screenshot showing AI insights]
- Headline (large, prominent)
- Executive summary (2-3 sentences)
- Major concern section
- Emerging trend section
- Critical issue highlighted
- Recommended actions (bulleted list)
```

---

## Live Demo

**Frontend:** https://campuslens-ai.vercel.app  
**Backend API:** https://campuslens-backend.onrender.com  
**API Documentation:** https://campuslens-backend.onrender.com/docs  

**Demo Credentials:**
- Email: `demo@campus.edu`
- Password: `DemoPassword123!`

(Credentials reset daily; all demo data cleared)

---

## Repository

**GitHub:** https://github.com/yourusername/campuslens-ai  

### Project Structure

```
campuslens-ai/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   ├── AnalyticsCharts.jsx
│   │   │   │   └── CampusPulse.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── StatusHistory.jsx
│   │   ├── pages/
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── MyReports.jsx
│   │   │   ├── Register.jsx
│   │   │   └── ReportIssue.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── supabase.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── backend/
│   ├── services/
│   │   ├── ai_service.py (Gemini analysis)
│   │   ├── duplicate.py (Duplicate detection)
│   │   ├── priority.py (Priority scoring)
│   │   ├── auth.py (JWT validation)
│   │   ├── database.py (Supabase queries)
│   │   └── __init__.py
│   ├── models/
│   │   ├── report.py (Pydantic schemas)
│   │   └── __init__.py
│   ├── tests/
│   │   └── test_ai_service_error_handling.py
│   ├── main.py (FastAPI app)
│   ├── requirements.txt
│   └── .env.example
├── README.md (this file)
└── package.json (monorepo root)
```

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## Built With

### Frontend Technologies
- **React 19** - UI framework
- **Vite 8** - Lightning-fast build tool
- **Tailwind CSS 4** - Utility-first CSS framework
- **Recharts 3** - React chart components
- **React Router 7** - Client-side routing
- **Supabase JS Client** - Auth and database client

### Backend Technologies
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Supabase Python** - Database client
- **Google GenAI** - Gemini API integration

### Infrastructure
- **Supabase** - PostgreSQL database, authentication, real-time
- **pgvector** - Vector similarity search (Postgres extension)
- **Google Gemini API** - AI models for analysis and embeddings
- **Vercel** - Frontend deployment
- **Render** - Backend deployment

### Development Tools
- **ESLint** - JavaScript linter
- **Python** - Backend language

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Support

For questions or issues:
- 📧 Email: support@campuslens.ai
- 🐙 GitHub Issues: https://github.com/alphaxt/campuslens-ai/issues
- 💬 Discussions: https://github.com/alphaxt/campuslens-ai/discussions

---

## Acknowledgments

Built with [Kiro](https://kiro.dev) - the AI development environment.

---

**Last Updated:** January 2024  
**Version:** 1.0.0
