# Implementation Plan: CampusLens AI

## Overview

This implementation plan covers the complete CampusLens AI platform - an AI-powered campus issue intelligence system. The platform enables students to submit campus problems using natural language, uses Gemini API for AI analysis and categorization, provides administrators with a dashboard for issue management, and implements duplicate detection using semantic embeddings.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "2.1", "3.1", "4.1", "4.2", "5.1"] },
    { "id": 1, "tasks": ["1.4", "1.5", "1.6", "2.2", "2.3", "3.2", "3.3", "4.3", "4.4", "5.2", "5.3"] },
    { "id": 2, "tasks": ["1.7", "2.4", "3.4", "4.5", "4.6", "5.4"] },
    { "id": 3, "tasks": ["2.5", "3.5", "4.7", "4.8", "5.5", "6.1", "6.2"] },
    { "id": 4, "tasks": ["2.6", "3.6", "4.9", "4.10", "5.6", "5.7", "6.3", "6.4"] },
    { "id": 5, "tasks": ["2.7", "3.7", "5.8", "6.5", "6.6"] },
    { "id": 6, "tasks": ["2.8", "3.8", "5.9", "6.7"] },
    { "id": 7, "tasks": ["2.9", "3.9", "5.10", "6.8", "6.9"] },
    { "id": 8, "tasks": ["2.10", "3.10", "6.10", "6.11"] },
    { "id": 9, "tasks": ["3.11", "6.12", "7.1", "7.2", "7.3", "7.4", "7.5"] },
    { "id": 10, "tasks": ["3.12", "6.13", "7.6", "8.1", "8.2", "8.3"] },
    { "id": 11, "tasks": ["7.7", "8.4", "8.5", "9.1"] },
    { "id": 12, "tasks": ["7.8", "8.6", "8.7", "9.2"] },
    { "id": 13, "tasks": ["7.9", "8.8", "9.3"] },
    { "id": 14, "tasks": ["7.10", "8.9", "9.4"] },
    { "id": 15, "tasks": ["7.11", "8.10", "9.5"] },
    { "id": 16, "tasks": ["7.12", "8.11", "9.6"] },
    { "id": 17, "tasks": ["7.13", "8.12", "9.7"] },
    { "id": 18, "tasks": ["7.14", "8.13", "9.8"] },
    { "id": 19, "tasks": ["8.14", "9.9"] },
    { "id": 20, "tasks": ["9.10", "10.1", "10.2"] },
    { "id": 21, "tasks": ["9.11", "10.3", "10.4"] },
    { "id": 22, "tasks": ["9.12", "10.5", "10.6"] },
    { "id": 23, "tasks": ["9.13", "10.7", "10.8"] },
    { "id": 24, "tasks": ["10.9", "10.10", "10.11"] },
    { "id": 25, "tasks": ["10.12", "10.13", "11.1"] },
    { "id": 26, "tasks": ["11.2", "11.3"] },
    { "id": 27, "tasks": ["11.4", "11.5"] },
    { "id": 28, "tasks": ["11.6", "11.7"] },
    { "id": 29, "tasks": ["11.8", "11.9", "11.10"] }
  ]
}
```

## Tasks

### Phase 1: Backend Infrastructure Setup

- [ ] 1. Set up project structure and dependencies
  - [ ] 1.1 Create backend directory structure
    - Create main.py with FastAPI app initialization
    - Create routes/, services/, models/ directories
    - Set up __init__.py files for modules
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour
  
  - [ ] 1.2 Configure environment variables
    - Create .env.example with all required variables
    - Set up Supabase configuration (URL, anon key)
    - Configure Gemini API key
    - Add database connection string
    - _Requirements: 1, 2, 4, 13_
    - Estimated: 0.5 hours
  
  - [ ] 1.3 Set up requirements.txt
    - Add FastAPI, uvicorn, python-multipart
    - Add supabase, pgvector
    - Add google-generativeai
    - Add pydantic with validation extras
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 0.5 hours
  
  - [ ] 1.4 Create database connection module
    - Implement database.py with Supabase client initialization
    - Add connection pooling configuration
    - Add error handling for connection failures
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour
  
  - [ ] 1.5 Set up AI service base configuration
    - Create ai_service.py with Gemini API client
    - Add retry logic with exponential backoff
    - Implement error handling for API failures
    - _Requirements: 4, 13_
    - Estimated: 1 hour
  
  - [ ] 1.6 Create Pydantic models for data validation
    - Implement all models from design document
    - Add Category, Severity, ReportStatus enums
    - Create request/response models for all endpoints
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 1.7 Implement error handling utilities
    - Create AppError base class
    - Implement AuthenticationError, AuthorizationError, ValidationError
    - Add custom exception handlers for FastAPI
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour

### Phase 2: Authentication and User Management

- [ ] 2. Implement authentication system
  - [ ] 2.1 Create Supabase Auth integration
    - Implement user registration endpoint
    - Implement login/logout endpoints
    - Add session validation middleware
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_
    - Estimated: 3 hours
  
  - [ ] 2.2 Create user profile management
    - Implement profile creation on registration
    - Add role-based access control (student/admin)
    - Create profile update endpoint
    - _Requirements: 1.2, 2.1, 2.3, 2.4_
    - Estimated: 1.5 hours
  
  - [ ] 2.3 Implement protected route decorators
    - Create admin_required decorator
    - Create student_required decorator
    - Implement current_user dependency
    - _Requirements: 1.5, 2.4, 3.2, 9.2, 15.2_
    - Estimated: 1 hour
  
  - [ ] 2.4 Create authentication endpoints
    - POST /api/auth/register
    - POST /api/auth/login
    - POST /api/auth/logout
    - GET /api/auth/session
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_
    - Estimated: 2 hours
  
  - [ ] 2.5 Add authentication middleware
    - Implement token validation middleware
    - Add rate limiting for auth endpoints
    - Create auth logging system
    - _Requirements: 1.4, 1.5, 2.3, 2.4_
    - Estimated: 1.5 hours
  
  - [ ] 2.6 Implement session management
    - Add session token refresh
    - Implement session cleanup
    - Add session timeout handling
    - _Requirements: 1.5, 2.4_
    - Estimated: 1 hour
  
  - [ ] 2.7 Add authentication error responses
    - Create standardized error responses for auth errors
    - Implement 401/403 error formatting
    - Add user-friendly error messages
    - _Requirements: 1.4, 2.4_
    - Estimated: 1 hour
  
  - [ ] 2.8 Implement role-based authorization
    - Create role checking utility
    - Add admin endpoint protection
    - Implement student-only endpoint protection
    - _Requirements: 2.3, 2.4, 9.2, 15.2_
    - Estimated: 1.5 hours
  
  - [ ] 2.9 Add authentication tests
    - [ ]* 2.9.1 Write unit tests for auth functions
      - Test token validation
      - Test role checking
      - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_
    
    - [ ]* 2.9.2 Write integration tests for auth endpoints
      - Test registration flow
      - Test login flow
      - Test unauthorized access
      - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_
    - Estimated: 2 hours
  
  - [ ] 2.10 Add authentication documentation
    - Create API documentation for auth endpoints
    - Add example requests/responses
    - Document error responses
    - Estimated: 1 hour

### Phase 3: Issue Management System

- [ ] 3. Implement issue management endpoints
  - [ ] 3.1 Create issue submission endpoint
    - Implement POST /api/reports
    - Validate authentication and authorization
    - Process issue submission with AI analysis
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 6.5_
    - Estimated: 3 hours
  
  - [ ] 3.2 Create issue retrieval endpoints
    - Implement GET /api/reports (admin list)
    - Implement GET /api/reports/:id (admin detail)
    - Implement GET /api/reports/student/:id (student list)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 9.1, 10.1, 10.2, 10.3, 10.4, 10.5, 11.1, 11.2, 11.3, 11.4, 11.5, 15.1, 15.2_
    - Estimated: 2 hours
  
  - [ ] 3.3 Implement issue update endpoint
    - Implement PUT /api/reports/:id (admin update)
    - Validate status transitions
    - Update status history
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_
    - Estimated: 2 hours
  
  - [ ] 3.4 Create AI analysis endpoint
    - Implement POST /api/analysis/analyze
    - Call Gemini API for analysis
    - Return structured analysis
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    - Estimated: 1.5 hours
  
  - [ ] 3.5 Implement duplicate detection endpoint
    - Implement POST /api/duplicates/check
    - Calculate embeddings similarity
    - Return duplicate candidates
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
    - Estimated: 2 hours
  
  - [ ] 3.6 Create analytics endpoints
    - Implement GET /api/analytics/campus-pulse
    - Implement GET /api/analytics/summary
    - Implement GET /api/analytics/export
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
    - Estimated: 2 hours
  
  - [ ] 3.7 Add filtering logic for issue list
    - Implement category filter
    - Implement location filter
    - Implement severity filter
    - Implement status filter
    - Implement date range filter
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
    - Estimated: 2 hours
  
  - [ ] 3.8 Add pagination support
    - Implement page parameter handling
    - Add limit parameter
    - Create pagination metadata
    - _Requirements: 11.4_
    - Estimated: 1 hour
  
  - [ ] 3.9 Add sorting functionality
    - Implement priority score sorting
    - Implement date sorting
    - Implement category sorting
    - _Requirements: 11.1_
    - Estimated: 1 hour
  
  - [ ] 3.10 Implement reporting functionality
    - [ ]* 3.10.1 Write unit tests for issue endpoints
      - Test issue creation
      - Test issue retrieval
      - Test issue updates
      - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 14.1, 14.2, 14.3, 14.4, 14.5_
    
    - [ ]* 3.10.2 Write integration tests for issue workflows
      - Test complete issue submission flow
      - Test admin dashboard filtering
      - Test status update flow
      - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 14.1, 14.2, 14.3, 14.4, 14.5, 15.1, 15.2, 15.3, 15.4, 15.5_
    - Estimated: 3 hours
  
  - [ ] 3.11 Add endpoint documentation
    - Document all issue management endpoints
    - Add example requests and responses
    - Document authentication requirements
    - Estimated: 1.5 hours
  
  - [ ] 3.12 Add error handling for endpoints
    - Implement consistent error responses
    - Add validation error formatting
    - Create custom exception handlers
    - Estimated: 1.5 hours

### Phase 4: AI Services Implementation

- [ ] 4. Implement AI analysis services
  - [ ] 4.1 Create Gemini API integration module
    - Initialize Gemini client with API key
    - Implement text analysis function
    - Add error handling for API failures
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    - Estimated: 2 hours
  
  - [ ] 4.2 Implement issue analysis logic
    - Parse issue description with Gemini
    - Extract category, severity, location
    - Generate summary and department recommendation
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    - Estimated: 2 hours
  
  - [ ] 4.3 Create keyword-based fallback system
    - Implement keyword matching for categories
    - Create severity estimation rules
    - Add fallback category mapping
    - _Requirements: 4.7, 4.8_
    - Estimated: 1.5 hours
  
  - [ ] 4.4 Add embedding generation service
    - Implement Gemini embeddings API call
    - Handle embedding vector formatting
    - Add error handling for embedding failures
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
    - Estimated: 1.5 hours
  
  - [ ] 4.5 Implement semantic similarity search
    - Use pgvector for cosine similarity
    - Implement 0.85 threshold check
    - Return duplicate candidates with scores
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
    - Estimated: 2 hours
  
  - [ ] 4.6 Create duplicate detection logic
    - Combine embedding similarity with text matching
    - Implement fallback text matching
    - Store duplicate relationships
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
    - Estimated: 2 hours
  
  - [ ] 4.7 Add confidence scoring
    - Calculate analysis confidence based on Gemini output
    - Implement low-confidence warnings
    - Add confidence thresholds for auto-approval
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    - Estimated: 1 hour
  
  - [ ] 4.8 Implement analysis caching
    - Cache Gemini API responses
    - Implement cache invalidation
    - Add cache expiry configuration
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    - Estimated: 1 hour
  
  - [ ] 4.9 Add AI service unit tests
    - [ ]* 4.9.1 Write unit tests for Gemini integration
      - Test successful API calls
      - Test error handling
      - Test fallback scenarios
      - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    
    - [ ]* 4.9.2 Write property test for analysis consistency (Property 1)
      - **Property 1: Issue Analysis Consistency**
      - **Validates: Requirements 4.1, 4.2, 4.3**
      - Test semantic similarity categorization
      - Test severity consistency
      - _Requirements: 4.1, 4.2, 4.3_
    - Estimated: 2 hours
  
  - [ ] 4.10 Add AI service integration tests
    - [ ]* 4.10.1 Test end-to-end analysis flow
      - Submit issue description
      - Verify AI analysis output
      - Test fallback scenarios
      - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
    
    - [ ]* 4.10.2 Test embedding generation
      - Generate embeddings for sample texts
      - Verify vector dimensions
      - Test error handling
      - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
    - Estimated: 2 hours

### Phase 5: Priority Scoring System

- [ ] 5. Implement priority scoring logic
  - [ ] 5.1 Create priority scoring function
    - Implement base score calculation (Low=25, Medium=50, High=75, Critical=100)
    - Add duplicate bonus (up to 20 points)
    - Add duration bonus (15 points if >7 days)
    - Add safety flag bonus (20 points)
    - Add accessibility flag bonus (15 points)
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8_
    - Estimated: 2 hours
  
  - [ ] 5.2 Implement daily priority recalculation
    - Create scheduled task for daily recalculation
    - Update all open issues
    - Log recalculation statistics
    - _Requirements: 12.8_
    - Estimated: 1.5 hours
  
  - [ ] 5.3 Add priority scoring tests
    - [ ]* 5.3.1 Write unit tests for priority calculation
      - Test base scores
      - Test duplicate bonuses
      - Test duration bonuses
      - Test flag bonuses
      - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8_
    
    - [ ]* 5.3.2 Write property test for priority calculation (Property 2)
      - **Property 2: Priority Score Calculation**
      - **Validates: Requirements 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7**
      - Test all combinations of inputs
      - Verify score bounds (0-100)
      - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_
    - Estimated: 2 hours
  
  - [ ] 5.4 Add priority visualization
    - [ ]* 5.4.1 Implement color-coded priority indicators
      - Define priority ranges and colors
      - Create visual components
      - _Requirements: 11.3_
    - Estimated: 1 hour
  
  - [ ] 5.5 Implement priority filtering
    - [ ]* 5.5.1 Add priority filter to admin dashboard
      - Filter by priority range
      - Sort by priority score
      - _Requirements: 10.1_
    - Estimated: 1 hour

### Phase 6: Database Implementation

- [ ] 6. Implement database schema and operations
  - [ ] 6.1 Create database migration scripts
    - Implement reports table
    - Implement status_history table
    - Implement duplicate_relationships table
    - Implement campus_pulse_cache table
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 6.2 Implement data models
    - Create SQLAlchemy models for all tables
    - Add relationship definitions
    - Implement validation
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 6.3 Add row-level security policies
    - Implement student policy for own reports
    - Implement admin policy for all reports
    - Implement insert policy for students
    - _Requirements: 1.5, 2.4, 3.2, 9.2, 15.2_
    - Estimated: 1.5 hours
  
  - [ ] 6.4 Create database index
    - Implement vector index for embeddings
    - Add indexes for common query patterns
    - Optimize query performance
    - _Requirements: 10.3_
    - Estimated: 1 hour
  
  - [ ] 6.5 Implement duplicate detection tests
    - [ ]* 6.5.1 Write property test for duplicate detection (Property 3)
      - **Property 3: Duplicate Detection Threshold**
      - **Validates: Requirements 13.1, 13.2, 13.3**
      - Test similarity score calculations
      - Verify 0.85 threshold behavior
      - _Requirements: 13.1, 13.2, 13.3_
    
    - [ ]* 6.5.2 Write property test for duplicate count accuracy (Property 5)
      - **Property 5: Duplicate Count Accuracy**
      - **Validates: Requirements 13.3**
      - Test duplicate count increments
      - Test duplicate count decrements
      - _Requirements: 13.3_
    - Estimated: 2 hours
  
  - [ ] 6.6 Add database utility functions
    - Create connection utility
    - Add transaction handling
    - Implement query helpers
    - Estimated: 1 hour
  
  - [ ] 6.7 Add database error handling
    - Implement connection retry logic
    - Add deadlock handling
    - Create error reporting
    - Estimated: 1 hour
  
  - [ ] 6.8 Implement status transition tests
    - [ ]* 6.8.1 Write property test for status transitions (Property 4)
      - **Property 4: Report Status Transition Validity**
      - **Validates: Requirements 8.1**
      - Test valid transitions
      - Test invalid transitions
      - _Requirements: 8.1_
    - Estimated: 1.5 hours
  
  - [ ] 6.9 Add authorization tests
    - [ ]* 6.9.1 Write property test for authorization (Property 7)
      - **Property 7: User Authorization Enforcement**
      - **Validates: Requirements 1.5, 3.2, 9.2**
      - Test student access restrictions
      - Test admin access
      - _Requirements: 1.5, 3.2, 9.2, 15.2_
    - Estimated: 1.5 hours
  
  - [ ] 6.10 Add database integration tests
    - [ ]* 6.10.1 Test report creation
    - [ ]* 6.10.2 Test report retrieval
    - [ ]* 6.10.3 Test status history tracking
    - [ ]* 6.10.4 Test duplicate relationship storage
    - Estimated: 2 hours
  
  - [ ] 6.11 Add database cleanup utilities
    - Create cleanup functions for test data
    - Add migration rollback scripts
    - Estimated: 0.5 hours
  
  - [ ] 6.12 Implement Campus Pulse caching
    - [ ]* 6.12.1 Write property test for Campus Pulse caching (Property 6)
      - **Property 6: Campus Pulse Caching**
      - **Validates: Requirements 16.5**
      - Test cache hit scenarios
      - Test cache invalidation
      - _Requirements: 16.5_
    - Estimated: 1.5 hours
  
  - [ ] 6.13 Add database migration documentation
    - Document all schema changes
    - Add migration instructions
    - Estimated: 0.5 hours

### Phase 7: Frontend Setup

- [ ] 7. Set up frontend project structure
  - [ ] 7.1 Initialize React + Vite + Tailwind project
    - Create new Vite React project
    - Install and configure Tailwind CSS
    - Set up basic project structure
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 7.2 Configure TypeScript
    - Set up tsconfig.json
    - Add type definitions
    - Configure strict mode
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour
  
  - [ ] 7.3 Set up routing with React Router
    - Configure main routes
    - Set up ProtectedRoute component
    - Create route guards for admin routes
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 7.4 Create state management structure
    - Set up React Context for authentication
    - Create issue context for global state
    - Implement reducer patterns
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 7.5 Create API client service
    - Implement axios instance
    - Add authentication headers
    - Create API error handling
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 7.6 Add layout components
    - [ ]* 7.6.1 Create Header component
      - Navigation links
      - User status display
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    
    - [ ]* 7.6.2 Create Footer component
      - Copyright information
      - Links
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 7.7 Implement authentication pages
    - [ ]* 7.7.1 Create Login page
      - Email/password inputs
      - Submit button
      - Error display
      - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_
    
    - [ ]* 7.7.2 Create Register page
      - User registration form
      - Role selection
      - Validation
      - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
    - Estimated: 2 hours
  
  - [ ] 7.8 Add loading states and error boundaries
    - Create Loading component
    - Add ErrorBoundary component
    - Implement global loading state
    - Estimated: 1 hour
  
  - [ ] 7.9 Create responsive design utilities
    - [ ]* 7.9.1 Test mobile responsiveness
    - [ ]* 7.9.2 Test tablet responsiveness
    - [ ]* 7.9.3 Test desktop responsiveness
    - Estimated: 1 hour
  
  - [ ] 7.10 Add testing utilities
    - [ ]* 7.10.1 Set up React Testing Library
    - [ ]* 7.10.2 Create test utilities
    - [ ]* 7.10.3 Add mock API service
    - Estimated: 1.5 hours
  
  - [ ] 7.11 Add authentication state tests
    - [ ]* 7.11.1 Test AuthContext
    - [ ]* 7.11.2 Test ProtectedRoute
    - Estimated: 1 hour
  
  - [ ] 7.12 Add layout component tests
    - [ ]* 7.12.1 Test Header component
    - [ ]* 7.12.2 Test Footer component
    - Estimated: 1 hour
  
  - [ ] 7.13 Add responsive design tests
    - [ ]* 7.13.1 Test mobile view
    - [ ]* 7.13.2 Test tablet view
    - [ ]* 7.13.3 Test desktop view
    - Estimated: 1 hour
  
  - [ ] 7.14 Create frontend documentation
    - Document component structure
    - Document API client usage
    - Document state management patterns
    - Estimated: 1 hour

### Phase 8: Frontend Components

- [ ] 8. Implement student issue submission
  - [ ] 8.1 Create IssueForm component
    - Textarea for issue description
    - Location selector
    - Submit button
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 6.5_
    - Estimated: 2 hours
  
  - [ ] 8.2 Create PreviewModal component
    - Display AI analysis results
    - Show summary, category, severity
    - Include confirm/cancel buttons
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
    - Estimated: 2 hours
  
  - [ ] 8.3 Add form validation
    - [ ]* 8.3.1 Implement description validation
      - Minimum length check
      - Maximum length check
      - _Requirements: 3.1_
    
    - [ ]* 8.3.2 Implement location validation
      - Optional field but must be valid if provided
      - _Requirements: 3.1_
    - Estimated: 1 hour
  
  - [ ] 8.4 Add submission success state
    - [ ]* 8.4.1 Create SuccessAlert component
      - Show success message
      - Provide tracking link
      - _Requirements: 5.4_
    
    - [ ]* 8.4.2 Create tracking link generation
      - Display unique tracking link
      - Add copy to clipboard
      - _Requirements: 6.4_
    - Estimated: 1.5 hours
  
  - [ ] 8.5 Add issue submission tests
    - [ ]* 8.5.1 Test IssueForm component
    - [ ]* 8.5.2 Test PreviewModal component
    - [ ]* 8.5.3 Test form validation
    - [ ]* 8.5.4 Test submission flow
    - Estimated: 2 hours
  
  - [ ] 8.6 Implement student issue tracking
    - [ ]* 8.6.1 Create MyReports component
      - List of student's issues
      - Issue cards with status
      - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
    
    - [ ]* 8.6.2 Create ReportStatusCard component
      - Display issue details
      - Show status history
      - _Requirements: 8.1, 8.2, 8.3, 8.4_
    - Estimated: 2.5 hours
  
  - [ ] 8.7 Add issue tracking tests
    - [ ]* 8.7.1 Test MyReports component
    - [ ]* 8.7.2 Test ReportStatusCard component
    - [ ]* 8.7.3 Test status history display
    - Estimated: 1.5 hours
  
  - [ ] 8.8 Implement admin dashboard layout
    - [ ]* 8.8.1 Create DashboardLayout component
      - Sidebar navigation
      - Main content area
      - _Requirements: 9.1, 9.2, 9.3_
    
    - [ ]* 8.8.2 Create DashboardNav component
      - Dashboard links
      - Logout button
      - _Requirements: 9.1, 9.2, 9.3_
    - Estimated: 2 hours
  
  - [ ] 8.9 Create IssueTable component
    - [ ]* 8.9.1 Implement sortable table
      - Priority score sorting
      - Date sorting
      - Category sorting
      - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
    
    - [ ]* 8.9.2 Add color-coded priority indicators
      - Visual priority levels
      - Color scheme
      - _Requirements: 11.3_
    - Estimated: 2 hours
  
  - [ ] 8.10 Add filtering panel
    - [ ]* 8.10.1 Create FiltersPanel component
      - Category filter
      - Location filter
      - Severity filter
      - Status filter
      - Date range filter
      - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
    
    - [ ]* 8.10.2 Implement filter logic
      - Apply all filters with AND logic
      - Clear all filters
      - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
    - Estimated: 2.5 hours
  
  - [ ] 8.11 Add dashboard tests
    - [ ]* 8.11.1 Test IssueTable component
    - [ ]* 8.11.2 Test FiltersPanel component
    - [ ]* 8.11.3 Test filter logic
    - Estimated: 1.5 hours
  
  - [ ] 8.12 Implement issue details view
    - [ ]* 8.12.1 Create IssueDetailsModal component
      - Full issue information
      - AI analysis details
      - Priority score display
      - Status history
      - _Requirements: 15.1, 15.2_
    
    - [ ]* 8.12.2 Create StatusHistory component
      - Timeline of status changes
      - Changed by information
      - Timestamps
      - _Requirements: 8.1, 8.2, 8.3, 8.4_
    - Estimated: 2 hours
  
  - [ ] 8.13 Add analytics components
    - [ ]* 8.13.1 Create CampusPulse component
      - AI-generated summary
      - Key metrics display
      - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
    
    - [ ]* 8.13.2 Create analytics charts
      - Category distribution
      - Severity distribution
      - Time series chart
      - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
    - Estimated: 2.5 hours
  
  - [ ] 8.14 Add analytics tests
    - [ ]* 8.14.1 Test CampusPulse component
    - [ ]* 8.14.2 Test analytics charts
    - Estimated: 1.5 hours

### Phase 9: Testing and Quality Assurance

- [ ] 9. Create comprehensive test suite
  - [ ] 9.1 Set up test infrastructure
    - Configure pytest for backend
    - Configure Vitest for frontend
    - Set up test data fixtures
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 9.2 Create property-based tests
    - [ ]* 9.2.1 Property 1: Issue Analysis Consistency
      - Test semantic similarity categorization
      - _Requirements: 4.1, 4.2, 4.3_
    
    - [ ]* 9.2.2 Property 2: Priority Score Calculation
      - Test all priority combinations
      - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_
    
    - [ ]* 9.2.3 Property 3: Duplicate Detection Threshold
      - Test embedding similarity at threshold
      - _Requirements: 13.1, 13.2, 13.3_
    
    - [ ]* 9.2.4 Property 4: Status Transition Validity
      - Test valid and invalid transitions
      - _Requirements: 8.1_
    
    - [ ]* 9.2.5 Property 5: Duplicate Count Accuracy
      - Test duplicate count updates
      - _Requirements: 13.3_
    
    - [ ]* 9.2.6 Property 6: Campus Pulse Caching
      - Test cache hit/miss scenarios
      - _Requirements: 16.5_
    
    - [ ]* 9.2.7 Property 7: User Authorization Enforcement
      - Test role-based access
      - _Requirements: 1.5, 3.2, 9.2, 15.2_
    - Estimated: 4 hours
  
  - [ ] 9.3 Create unit tests
    - [ ]* 9.3.1 Backend unit tests
      - Test all service functions
      - Test all utility functions
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    
    - [ ]* 9.3.2 Frontend unit tests
      - Test all components
      - Test all hooks
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 3 hours
  
  - [ ] 9.4 Create integration tests
    - [ ]* 9.4.1 Backend integration tests
      - Test all API endpoints
      - Test database operations
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    
    - [ ]* 9.4.2 Frontend integration tests
      - Test component interactions
      - Test API integration
      - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 3 hours
  
  - [ ] 9.5 Create E2E tests
    - [ ]* 9.5.1 Complete student workflow
      - Register, login, submit issue
      - _Requirements: 1, 2, 3, 4, 5, 6, 7_
    
    - [ ]* 9.5.2 Complete admin workflow
      - Login, view dashboard, filter, update status
      - _Requirements: 2, 9, 10, 11, 14_
    
    - [ ]* 9.5.3 Duplicate detection workflow
      - Submit similar issues
      - Verify duplicate detection
      - _Requirements: 13_
    - Estimated: 3 hours
  
  - [ ] 9.6 Add test coverage reporting
    - [ ]* 9.6.1 Configure coverage reports
    - [ ]* 9.6.2 Set up coverage thresholds
    - [ ]* 9.6.3 Generate coverage summary
    - Estimated: 1 hour
  
  - [ ] 9.7 Add performance testing
    - [ ]* 9.7.1 Test API response times
    - [ ]* 9.7.2 Test database query performance
    - [ ]* 9.7.3 Test embedding generation performance
    - Estimated: 2 hours
  
  - [ ] 9.8 Create test documentation
    - Document testing strategy
    - Document test patterns
    - Document how to run tests
    - Estimated: 1 hour
  
  - [ ] 9.9 Run final test suite
    - [ ]* 9.9.1 Run all tests
    - [ ]* 9.9.2 Verify coverage
    - [ ]* 9.9.3 Fix any failing tests
    - Estimated: 2 hours

### Phase 10: Security and Performance

- [ ] 10. Implement security measures
  - [ ] 10.1 Add input sanitization
    - Sanitize user inputs
    - Prevent XSS attacks
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 10.2 Implement rate limiting
    - Rate limit authentication endpoints
    - Rate limit API endpoints
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 10.3 Add security headers
    - Implement CSP headers
    - Add CORS configuration
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour
  
  - [ ] 10.4 Add logging and monitoring
    - Implement request logging
    - Add error logging
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 10.5 Add security tests
    - [ ]* 10.5.1 Test XSS prevention
    - [ ]* 10.5.2 Test rate limiting
    - [ ]* 10.5.3 Test input sanitization
    - Estimated: 1.5 hours
  
  - [ ] 10.6 Create security documentation
    - Document security measures
    - Document threat model
    - Estimated: 1 hour
  
  - [ ] 10.7 Optimize database queries
    - [ ]* 10.7.1 Add query optimization
    - [ ]* 10.7.2 Implement caching
    - Estimated: 2 hours
  
  - [ ] 10.8 Add performance monitoring
    - [ ]* 10.8.1 Set up performance metrics
    - [ ]* 10.8.2 Add query time monitoring
    - Estimated: 1.5 hours
  
  - [ ] 10.9 Create deployment configuration
    - [ ]* 10.9.1 Configure production build
    - [ ]* 10.9.2 Create deployment scripts
    - Estimated: 2 hours
  
  - [ ] 10.10 Add deployment tests
    - [ ]* 10.10.1 Test production build
    - [ ]* 10.10.2 Test deployment scripts
    - Estimated: 1.5 hours
  
  - [ ] 10.11 Create deployment documentation
    - Document deployment process
    - Document environment setup
    - Estimated: 1 hour
  
  - [ ] 10.12 Add security documentation
    - Document security measures
    - Document incident response
    - Estimated: 1 hour
  
  - [ ] 10.13 Run security audit
    - [ ]* 10.13.1 Run security scan
    - [ ]* 10.13.2 Fix any vulnerabilities
    - Estimated: 2 hours

### Phase 11: Final Integration and Documentation

- [ ] 11. Complete integration and documentation
  - [ ] 11.1 Wire all components together
    - Connect frontend to backend
    - Connect backend to external services
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 3 hours
  
  - [ ] 11.2 Add comprehensive error handling
    - Implement global error handling
    - Add user-friendly error messages
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 11.3 Add logging system
    - Implement structured logging
    - Add logging levels
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 11.4 Create API documentation
    - Document all endpoints
    - Add request/response examples
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 11.5 Add user documentation
    - Create student guide
    - Create admin guide
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 11.6 Add developer documentation
    - Document codebase structure
    - Document development setup
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 2 hours
  
  - [ ] 11.7 Create README documentation
    - Project overview
    - Setup instructions
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1.5 hours
  
  - [ ] 11.8 Add deployment documentation
    - Document deployment process
    - Document environment variables
    - _Requirements: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15_
    - Estimated: 1 hour
  
  - [ ] 11.9 Create final integration tests
    - [ ]* 11.9.1 Test complete student workflow
    - [ ]* 11.9.2 Test complete admin workflow
    - [ ]* 11.9.3 Test duplicate detection
    - Estimated: 2 hours
  
  - [ ] 11.10 Run final test suite
    - [ ]* 11.10.1 Run all tests
    - [ ]* 11.10.2 Verify all requirements
    - Estimated: 2 hours
  - [ ] 11.11 Add performance tests
    - [ ]* 11.11.1 Test API performance
    - [ ]* 11.11.2 Test database performance
    - Estimated: 1.5 hours
  
  - [ ] 11.12 Create final documentation
    - [ ]* 11.12.1 Create comprehensive documentation
    - [ ]* 11.12.2 Document all features
    - Estimated: 2 hours

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Integration tests validate system components working together
- E2E tests validate complete user workflows
- Security measures should be implemented incrementally throughout development
- Documentation should be updated as features are implemented
- Testing should be run after each phase for continuous validation

## Task Dependency Graph

See the Task Dependency Graph section at the top of this document for the complete execution plan with 30 waves of tasks.
