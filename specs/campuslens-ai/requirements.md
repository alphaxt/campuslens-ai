# Requirements Document

## Introduction

CampusLens AI is an AI-powered campus issue intelligence and resolution platform that allows students to submit campus problems using natural language. The AI analyzes each report and transforms unstructured complaints into structured information for university administration. This platform streamlines the reporting and resolution process for campus issues while providing administrators with actionable insights through analytics and AI-generated summaries.

The platform serves two primary user groups: students who submit and track issues, and administrators who manage and resolve them. The system uses Gemini API for AI analysis, Supabase PostgreSQL with pgvector for data storage and semantic duplicate detection, and provides secure authentication through Supabase Auth.

## Glossary

- **CampusLens AI**: The AI-powered campus issue intelligence and resolution platform
- **Student**: A registered user who can submit campus issues and track their status
- **Administrator**: A registered user with administrative privileges who can view, filter, and manage all reports
- **Issue**: A reported campus problem submitted by a student, containing natural language description
- **Category**: A classification of the issue type (Network, Facilities, Security, Cleanliness, Transport, Accessibility, Academic Facilities)
- **Severity**: The impact level of an issue (Low, Medium, High, Critical)
- **Priority Score**: A numeric score (0-100) calculated based on severity, duplicates, duration, safety impact, and accessibility impact
- **Department**: The university department responsible for resolving a specific category of issues
- **Location**: A physical location on campus where the issue is reported
- **Report**: A complete issue submission with all metadata and analysis results
- **Campus Pulse**: An AI-generated summary of campus issue trends and priorities for administrators

## Requirements

### Requirement 1: Student Authentication

**User Story:** As a student, I want to register and log in to CampusLens AI, so that my identity is verified and I can submit and track issues.

#### Acceptance Criteria

1. WHEN a new user accesses the platform, THE Student Portal SHALL present registration options
2. WHEN a user registers, THE System SHALL create an authentication record in Supabase Auth
3. WHEN login credentials are submitted, THE System SHALL authenticate the user with Supabase Auth
4. IF authentication fails, THEN THE System SHALL return a clear error message
5. WHERE a user is not authenticated, THE System SHALL redirect to the login page

### Requirement 2: Administrator Authentication

**User Story:** As an administrator, I want to log in to the administrative dashboard, so that only authorized personnel can access sensitive information.

#### Acceptance Criteria

1. WHEN an administrator accesses the dashboard, THE System SHALL require authentication
2. WHEN invalid credentials are provided, THE System SHALL return a clear error message
3. WHERE a non-administrator attempts to access the dashboard, THE System SHALL deny access
4. THE System SHALL maintain administrator session state securely

### Requirement 3: Issue Submission by Students

**User Story:** As a student, I want to submit a campus issue using natural language, so that I do not need to know the correct category beforehand.

#### Acceptance Criteria

1. WHEN a student submits an issue description, THE System SHALL accept natural language text input
2. WHERE a student is authenticated, THE Student Portal SHALL allow issue submission
3. WHEN an issue is submitted, THE System SHALL store the student's user ID with the issue
4. IF issue submission fails, THEN THE System SHALL return an error message with details

### Requirement 4: AI Issue Analysis

**User Story:** As a student, I want the AI to analyze my issue, so that I can see how the system understands my complaint before final submission.

#### Acceptance Criteria

1. WHEN a valid issue description is submitted, THE System SHALL analyze the description with Gemini API
2. THE AI Analysis SHALL determine the category from predefined options
3. THE AI Analysis SHALL determine the severity level (Low, Medium, High, Critical)
4. THE AI Analysis SHALL extract location information when present in the description
5. THE AI Analysis SHALL identify the most likely responsible department
6. THE AI Analysis SHALL generate a concise summary of the issue
7. WHERE Gemini API is unavailable, THE System SHALL use fallback analysis with warning to the user
8. IF analysis fails after retry, THEN THE System SHALL return an error with option to submit without AI analysis

### Requirement 5: Issue Preview and Confirmation

**User Story:** As a student, I want to review AI analysis before final submission, so that I can verify the system understood my issue correctly.

#### Acceptance Criteria

1. WHEN AI analysis is complete, THE System SHALL display the analysis to the student
2. WHERE the student confirms the issue, THE System SHALL save the issue to the database
3. WHERE the student requests changes, THE System SHALL allow editing of the original description
4. WHEN an issue is saved, THE System SHALL return a unique issue ID

### Requirement 6: Issue Persistence

**User Story:** As a student, I want my issue to be saved, so that I can track its status and history.

#### Acceptance Criteria

1. WHEN an issue is confirmed, THE System SHALL store it in Supabase PostgreSQL
2. THE System SHALL store the issue with all metadata: category, severity, location, department, summary, priority score, and status
3. THE System SHALL assign a unique ID to each issue
4. WHEN an issue is stored, THE System SHALL generate a unique tracking link
5. IF database storage fails, THEN THE System SHALL return an error and roll back the transaction

### Requirement 7: Student Issue Tracking

**User Story:** As a student, I want to view my submitted reports, so that I can track their status.

#### Acceptance Criteria

1. WHERE a student is authenticated, THE System SHALL display a list of their submitted issues
2. FOR EACH issue in the list, THE System SHALL display: issue ID, category, severity, status, submission date, and last update
3. WHEN a student selects an issue, THE System SHALL display detailed information including AI analysis and status history
4. THE System SHALL update the status display in real-time when changes occur
5. IF no issues are found, THE System SHALL display an empty state message

### Requirement 8: Report Status Management

**User Story:** As a student, I want to view the status of my report, so that I know when it's being addressed.

#### Acceptance Criteria

1. THE System SHALL maintain status for each report: Submitted, Under Review, In Progress, Resolved, Closed
2. WHEN an administrator updates a report status, THE Student Portal SHALL reflect the change
3. WHEN a report status changes, THE System SHALL record the timestamp and administrator who made the change
4. THE System SHALL display status history for each report

### Requirement 9: Administrator Dashboard Access

**User Story:** As an administrator, I want to access the dashboard, so that I can manage all campus issues.

#### Acceptance Criteria

1. WHEN authenticated administrators access the dashboard, THE System SHALL display the main dashboard view
2. WHERE authentication fails or user is not an administrator, THE System SHALL deny access
3. THE System SHALL maintain dashboard session state securely

### Requirement 10: Issue Filtering by Administrator

**User Story:** As an administrator, I want to filter issues by multiple criteria, so that I can focus on specific problems.

#### Acceptance Criteria

1. THE Dashboard SHALL provide filters for: category, location, severity, status, department, and date range
2. WHERE multiple filters are applied, THE System SHALL apply all filters with AND logic
3. WHEN a filter is changed, THE System SHALL update the displayed issues within 2 seconds
4. THE System SHALL reset to show all issues when all filters are cleared
5. WHEN filtering by date range, THE System SHALL include issues submitted between the start and end dates inclusive

### Requirement 11: Issue List Display

**User Story:** As an administrator, I want to view all issues with filtering, so that I can see the full scope of campus problems.

#### Acceptance Criteria

1. THE System SHALL display issues in a sortable table or card view
2. FOR EACH issue, THE System SHALL display: issue ID, description summary, category, severity, priority score, status, location, submitter, and submission date
3. WHEN a priority score is displayed, THE System SHALL show it with visual indicators (color-coded)
4. THE System SHALL support pagination or infinite scroll for large result sets
5. WHEN issues are loaded, THE System SHALL display the total count and number of filtered results

### Requirement 12: AI Priority Scoring

**User Story:** As an administrator, I want to view AI-generated priority recommendations, so that urgent problems can be addressed first.

#### Acceptance Criteria

1. WHEN a new issue is created, THE System SHALL calculate a priority score between 0 and 100
2. THE priority score SHALL be based on: severity (40%), duplicate count (20%), duration since submission (20%), safety impact (10%), accessibility impact (10%)
3. WHERE severity is Critical, THE priority score SHALL increase by at least 30 points
4. WHERE an issue has duplicates, THE priority score SHALL increase by 10 points per duplicate (maximum 20 points)
5. WHERE an issue has been open for more than 7 days, THE priority score SHALL increase by 15 points
6. WHERE an issue impacts safety, THE priority score SHALL increase by at least 20 points
7. WHERE an issue impacts accessibility, THE priority score SHALL increase by at least 15 points
8. THE System SHALL recalculate priority scores daily based on duration

### Requirement 13: Semantic Duplicate Detection

**User Story:** As an administrator, I want duplicate issues identified, so that I can address the most common problems first.

#### Acceptance Criteria

1. WHEN a new issue is created, THE System SHALL compare it with existing issues using Gemini embeddings
2. WHERE a similar issue exists with embedding similarity above 0.85, THE System SHALL flag it as a potential duplicate
3. THE System SHALL store duplicate relationships and count duplicates for each issue
4. WHEN duplicate issues are detected, THE System SHALL notify administrators in the dashboard
5. IF embedding computation fails, THE System SHALL log the error and continue with basic text matching

### Requirement 14: Report Status Changes

**User Story:** As an administrator, I want to change report status, so that students are informed about progress.

#### Acceptance Criteria

1. WHEN an administrator changes a report status, THE System SHALL update the status in the database
2. THE System SHALL record the administrator who made the change and the timestamp
3. WHEN status changes, THE System SHALL update the student's view in real-time
4. WHERE status is changed to Resolved or Closed, THE System SHALL require optional resolution notes
5. IF status update fails, THEN THE System SHALL return an error and maintain the original status

### Requirement 15: Issue Details View

**User Story:** As an administrator, I want to view detailed information about an issue, so that I can understand the full context before taking action.

#### Acceptance Criteria

1. WHEN an administrator selects an issue, THE System SHALL display a detailed view with all information
2. THE detailed view SHALL include: full description, AI analysis (category, severity, location, department, summary), priority score, status history, duplicate count, and submission date
3. WHERE location information is available, THE System SHALL display it in a map component
4. THE System SHALL show the student who submitted the issue with option to contact them
5. WHEN duplicate issues exist, THE System SHALL display a list of related issues with links

### Requirement 16: Campus Pulse Generation

**User Story:** As an administrator, I want to view AI-generated Campus Pulse summaries, so that I can understand campus trends at a glance.

#### Acceptance Criteria

1. WHEN the Campus Pulse feature is accessed, THE System SHALL generate a summary using Gemini API
2. THE Campus Pulse SHALL include: top 5 categories by issue count, top 5 locations with most issues, severity distribution, priority score summary, and emerging trends
3. THE Campus Pulse SHALL cover the last 7 days by default with option to change date range
4. WHERE data is insufficient, THE System SHALL indicate limited data rather than generating incomplete insights
5. THE System SHALL cache Campus Pulse results for 30 minutes to improve performance
6. IF Gemini API is unavailable, THE System SHALL display basic statistics from the database

### Requirement 17: Category Management

**User Story:** As an administrator, I want to view the defined issue categories, so that I understand how issues are classified.

#### Acceptance Criteria

1. THE System SHALL define the following categories: Network, Facilities, Security, Cleanliness, Transport, Accessibility, Academic Facilities
2. WHEN an issue is analyzed, THE System SHALL classify it into one of these categories
3. WHERE a category is not clearly identified, THE System SHALL assign "Uncategorized" as a temporary category
4. THE System SHALL allow administrators to view category statistics

### Requirement 18: Location Handling

**User Story:** As a student, I want to specify location for my issue, so that maintenance teams can find the problem quickly.

#### Acceptance Criteria

1. WHEN submitting an issue, THE Student Portal SHALL provide location selection options
2. LOCATION options SHALL include: building names, campus zones, and free-text input
3. WHERE Gemini API extracts location from text, THE System SHALL suggest it to the student
4. IF location is not specified, THE System SHALL allow submission with "General Campus" as default
5. THE System SHALL store location coordinates when available from map selection

### Requirement 19: Performance Requirements

**User Story:** As a user, I want the system to respond quickly, so that I can complete tasks efficiently.

#### Acceptance Criteria

1. WHEN submitting an issue, THE System SHALL complete within 5 seconds for 95% of requests
2. WHEN loading the dashboard, THE System SHALL display initial results within 3 seconds
3. WHEN filtering issues, THE System SHALL update results within 2 seconds
4. WHEN generating Campus Pulse, THE System SHALL complete within 15 seconds
5. THE System SHALL handle up to 100 concurrent users without degradation

### Requirement 20: Security Requirements

**User Story:** As a user, I want my data to be secure, so that my personal information and campus issues are protected.

#### Acceptance Criteria

1. THE System SHALL use Supabase Auth for all user authentication
2. WHEN API keys are stored, THE System SHALL use environment variables and never expose them in client code
3. ALL data transmitted between client and server SHALL use HTTPS
4. WHEN a session expires, THE System SHALL require re-authentication
5. THE System SHALL implement rate limiting to prevent API abuse
6. WHEN authentication fails repeatedly, THE System SHALL temporarily block the IP address

### Requirement 21: Availability Requirements

**User Story:** As a user, I want the system to be available when I need it, so that I can report issues without disruption.

#### Acceptance Criteria

1. THE System SHALL be available 99% of business hours (6 AM to 11 PM)
2. WHEN a service fails, THE System SHALL display a user-friendly error message
3. THE System SHALL log all errors for administrator review
4. WHERE AI services are unavailable, THE System SHALL continue to function with limited capabilities

### Requirement 22: Error Handling

**User Story:** As a user, I want clear error messages, so that I can resolve issues or try again.

#### Acceptance Criteria

1. WHEN a network error occurs, THE System SHALL display a message and retry option
2. WHEN API limits are reached, THE System SHALL inform the user and suggest trying later
3. IF validation fails, THE System SHALL highlight problematic fields with specific error messages
4. WHEN an unexpected error occurs, THE System SHALL return a generic error message to the user and log detailed information
5. THE System SHALL maintain error logs for administrator review

### Requirement 23: Responsive Design

**User Story:** As a student, I want to use CampusLens AI on mobile devices, so that I can submit issues from anywhere.

#### Acceptance Criteria

1. THE Student Portal SHALL be fully responsive for mobile, tablet, and desktop screens
2. WHEN accessed on mobile, THE System SHALL optimize touch targets and layout
3. WHEN the screen size changes, THE System SHALL adapt the UI without layout issues
4. THE System SHALL maintain consistent functionality across all device types

### Requirement 24: Data Privacy

**User Story:** As a student, I want my data to be private, so that only authorized personnel can access my issues.

#### Acceptance Criteria

1. WHERE a student submits an issue, ONLY the student and administrators SHALL view it
2. THE System SHALL not share student information with unauthorized personnel
3. WHEN an issue is resolved, THE System SHALL maintain audit logs but anonymize student data after 12 months
4. THE System SHALL comply with data protection regulations for student information

### Requirement 25: Admin Analytics

**User Story:** As an administrator, I want to view analytics and trends, so that I can identify patterns and allocate resources effectively.

#### Acceptance Criteria

1. THE Dashboard SHALL display charts for issue categories, severity distribution, and resolution times
2. WHEN date ranges are selected, THE System SHALL update analytics in real-time
3. THE System SHALL export analytics data in CSV format on request
4. WHERE data is insufficient, THE System SHALL indicate limited data rather than showing misleading charts
5. THE System SHALL display trending topics compared to previous periods
