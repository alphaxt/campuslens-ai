# CampusLens AI Gemini API Failure Handling Bugfix Design

## Overview

This bugfix addresses the current issue where Gemini API failures (such as 429 RESOURCE_EXHAUSTED errors) can expose raw technical exception text to users. The fix adds comprehensive error handling around all Gemini API calls in ai_service.py, providing fallback analysis when Gemini is unavailable. The design ensures FastAPI remains running, allows report submission with fallback data, and logs actual errors for debugging while showing users only friendly messages.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when Gemini API returns a 429 RESOURCE_EXHAUSTED error or any other error
- **Property (P)**: The desired behavior when Gemini API fails - return clean fallback analysis with specific fields and user-friendly error messages
- **Preservation**: Existing Gemini analysis functionality that must remain unchanged when API is available
- **ai_service.py**: The Python file containing Gemini API calls for issue analysis and campus pulse generation
- **main.py**: The FastAPI backend file containing the create_report endpoint
- **fallback_analysis**: The predefined analysis structure to return when Gemini is unavailable

## Bug Details

### Bug Condition

The bug manifests when the Gemini API returns a 429 RESOURCE_EXHAUSTED error or any other API error. The `analyze_issue()` function in ai_service.py directly calls the Gemini API without try/except blocks, causing exceptions to bubble up to main.py where they may expose raw error text to users.

**Formal Specification:**
```
FUNCTION isBugCondition(api_response)
  INPUT: api_response of type Gemini API response or Exception
  OUTPUT: boolean
  
  RETURN api_response.status_code = 429
         OR api_response.is_error = true
         OR exception_is_raised
END FUNCTION
```

### Examples

- **Example 1**: When Gemini API returns 429 RESOURCE_EXHAUSTED, current code raises an exception with raw error text that may be exposed to frontend
- **Example 2**: When Gemini API times out, current code crashes FastAPI or creates partially processed reports
- **Example 3**: When Gemini API returns connection error, current code shows technical exception details to students
- **Edge Case**: When Gemini API is unavailable during Campus Pulse generation, the analytics endpoint crashes

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- When Gemini API is available, full AI analysis with summary, category, severity, etc. must continue to work exactly as before
- All existing functionality (authentication, duplicate detection, priority scoring, status history) must remain completely unchanged
- Report submission flow must continue to work without modification when Gemini is available
- Campus Pulse generation must return detailed analysis when Gemini is available

**Scope:**
All inputs that do NOT involve Gemini API failures should be completely unaffected by this fix. This includes:
- Normal report submissions with successful Gemini analysis
- Duplicate detection logic
- Priority scoring calculations
- User authentication and authorization
- All existing API endpoints

## Hypothesized Root Cause

Based on the bug description, the most likely issues are:

1. **Missing Error Handling**: The `analyze_issue()` function in ai_service.py does not wrap the Gemini API call in try/except blocks
   - No handling for 429 RESOURCE_EXHAUSTED errors
   - No handling for timeout errors
   - No handling for connection errors

2. **Missing Error Handling in generate_campus_pulse()**: The campus pulse generation function also lacks error handling
   - No fallback for analytics endpoint when Gemini unavailable
   - No graceful degradation of service

3. **Error Propagation in main.py**: The create_report endpoint catches generic Exception but may expose raw error text
   - The `str(error)` conversion in HTTPException detail may expose Gemini error details

4. **Missing Fallback Analysis**: No predefined fallback analysis structure exists
   - No standardized response when Gemini is unavailable
   - No way to allow report submission with partial data

## Correctness Properties

Property 1: Bug Condition - Gemini API Error Handling

_For any_ Gemini API response where an error occurs (429 RESOURCE_EXHAUSTED, timeout, connection failure, or other errors), the fixed code SHALL return a clean fallback analysis with summary "AI analysis unavailable", category "Uncategorized", severity "Medium", recommended_department "Campus Facilities", extracted_location null, safety_flag false, accessibility_flag false, and confidence 0.5.

**Validates: Requirements 2.1, 2.2, 2.3, 2.5**

Property 2: Preservation - Normal Gemini Functionality

_For any_ Gemini API response where no error occurs, the fixed code SHALL produce exactly the same result as the original function, preserving all existing functionality for successful API calls including full AI analysis with summary, category, severity, location extraction, safety/accessibility flags, and confidence scores.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Fix Implementation

### Changes Required

**File**: `backend/services/ai_service.py`

**Function**: `analyze_issue()`

**Specific Changes**:

1. **Add try/except block around Gemini API call**: Wrap the `client.models.generate_content()` call in try/except to catch all exceptions
   - Import Python's logging module
   - Add try/except block around the API call
   - Catch generic Exception to handle all error types (429, timeout, connection, etc.)
   - Log the actual error with logging.error() for admin debugging

2. **Add fallback analysis return**: When any exception occurs, return the predefined fallback analysis structure
   - Return dictionary with: summary="AI analysis unavailable", category="Uncategorized", severity="Medium", recommended_department="Campus Facilities", extracted_location=null, safety_flag=false, accessibility_flag=false, confidence=0.5

3. **Update generate_campus_pulse()**: Add similar error handling for campus pulse generation
   - Wrap the API call in try/except
   - Return basic statistics structure when Gemini unavailable
   - Log the actual error for debugging

**File**: `backend/main.py`

**Function**: `create_report()`

**Specific Changes**:

1. **Add specific 429 error handling**: Check for 429 RESOURCE_EXHAUSTED errors in the exception
   - Add try/except around the analyze_issue() call
   - Specifically handle 429 errors by using fallback analysis
   - Ensure report submission completes successfully

2. **Update error logging**: Ensure Gemini errors are logged but not exposed to users
   - Use Python's logging module to log actual errors
   - Keep HTTPException with user-friendly message

**File**: `frontend/src/pages/ReportIssue.jsx`

**Specific Changes**:

1. **Add user-friendly error display**: Update error handling to show friendly message when AI is unavailable
   - Check for "AI analysis unavailable" in the response
   - Display user-friendly message if Gemini failed

2. **Add fallback display**: Show that analysis was generated with fallback data
   - Indicate when fallback analysis was used

**File**: `frontend/src/pages/MyReports.jsx`

**Specific Changes**:

1. **Update error handling**: Modify error display to show friendly message
   - Check for Gemini-related error patterns
   - Display "AI analysis is temporarily unavailable. Please try again later." for Gemini failures

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, simulate Gemini API failures to verify error handling works, then verify that normal Gemini functionality is preserved.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm or refute the root cause analysis.

**Test Plan**: 
1. Set up environment variable to simulate 429 error (or use mock/patching in tests)
2. Attempt to submit a report and observe the error
3. Verify that raw Gemini error text is exposed (this demonstrates the bug exists)
4. Try Campus Pulse endpoint when Gemini unavailable to observe crash

**Test Cases**:
1. **429 Error Test**: Set GEMINI_API_KEY to invalid value that returns 429 (will fail on unfixed code)
2. **Timeout Test**: Simulate Gemini API timeout (will fail on unfixed code)
3. **Connection Error Test**: Simulate network failure to Gemini (will fail on unfixed code)
4. **Campus Pulse Test**: Attempt Campus Pulse generation when Gemini unavailable (will fail on unfixed code)

**Expected Counterexamples**:
- Raw exception text exposed to frontend (e.g., "429 RESOURCE_EXHAUSTED: ...")
- FastAPI crashes or returns 500 error with technical details
- Report submission blocked when Gemini unavailable
- Campus Pulse endpoint crashes when Gemini unavailable

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed function produces the expected behavior.

**Pseudocode:**
```
FOR ALL Gemini API failure cases WHERE isBugCondition(api_response) DO
  result := analyze_issue_fixed(description)
  ASSERT result.summary = "AI analysis unavailable"
  ASSERT result.category = "Uncategorized"
  ASSERT result.severity = "Medium"
  ASSERT result.recommended_department = "Campus Facilities"
  ASSERT result.extracted_location IS NULL
  ASSERT result.safety_flag = false
  ASSERT result.accessibility_flag = false
  ASSERT result.confidence = 0.5
END FOR
```

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL Gemini API success cases WHERE NOT isBugCondition(api_response) DO
  result := analyze_issue_fixed(description)
  ASSERT result.summary is meaningful
  ASSERT result.category is one of valid categories
  ASSERT result.severity is one of valid severities
  ASSERT result.confidence > 0.5 (full analysis has higher confidence)
END FOR
```

**Testing Approach**: 
1. Use Python's unittest.mock or pytest-mock to patch the Gemini API call
2. Simulate successful responses and verify full analysis is returned
3. Simulate 429, timeout, connection errors and verify fallback is returned
4. Verify that the same description produces same result with and without fix (when Gemini available)

**Test Cases**:
1. **Normal Gemini Test**: Verify full analysis when Gemini returns successful result
2. **Duplicate Detection Test**: Verify duplicate detection still works with fallback analysis
3. **Priority Scoring Test**: Verify priority scoring works with fallback analysis
4. **Report Submission Test**: Verify report submission completes with fallback data

### Unit Tests

- Test analyze_issue() with 429 error mock - verify fallback returned
- Test analyze_issue() with timeout mock - verify fallback returned
- Test analyze_issue() with connection error mock - verify fallback returned
- Test analyze_issue() with successful Gemini response - verify full analysis
- Test generate_campus_pulse() with 429 error - verify basic stats returned
- Test generate_campus_pulse() with successful Gemini response - verify full analysis
- Test that logging occurs when errors happen (admin debugging)

### Property-Based Tests

- Generate random descriptions and verify fallback properties when Gemini mocked to fail
- Generate random descriptions and verify full analysis properties when Gemini mocked to succeed
- Verify confidence score difference between fallback (0.5) and full analysis (>0.5)

### Integration Tests

- Full report submission flow with mocked Gemini 429 error - verify report saved with fallback
- Campus Pulse endpoint with mocked Gemini timeout - verify basic stats returned
- Verify duplicate detection works with fallback category
- Verify priority scoring works with fallback severity

### Manual Testing Without Wasting API Calls

To test without intentionally wasting Gemini API calls:

1. **Set GEMINI_API_KEY to invalid value** (e.g., empty string or fake key) to trigger 429/invalid key errors
2. **Submit a report** via ReportIssue.jsx - verify fallback analysis used
3. **Check MyReports.jsx** - verify no raw error text shown
4. **Check backend logs** - verify actual error logged for debugging
5. **Verify report saved** - check database for report with fallback analysis
6. **Test Campus Pulse** - verify basic stats returned when Gemini unavailable

For preservation testing, use valid GEMINI_API_KEY and verify normal behavior continues.