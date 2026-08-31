# Bugfix Requirements Document

## Introduction

This bugfix addresses the current issue where Gemini API failures (such as 429 RESOURCE_EXHAUSTED errors) can expose raw technical exception text to users, making the application appear broken. The application must gracefully handle these failures and return user-friendly messages while maintaining all existing functionality.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN Gemini API returns a 429 RESOURCE_EXHAUSTED error THEN the system exposes raw exception text to the frontend/user

1.2 WHEN Gemini API returns any error (rate limit, timeout, or other failures) THEN the system may crash FastAPI or create partially processed reports

1.3 WHEN Gemini API is unavailable THEN the system prevents report submission, blocking all users from submitting reports

### Expected Behavior (Correct)

2.1 WHEN Gemini API returns a 429 RESOURCE_EXHAUSTED error THEN the system SHALL catch the error, log it for debugging, and return a clean fallback analysis with: summary "AI analysis unavailable", category "Uncategorized", severity "Medium", recommended_department "Campus Facilities", extracted_location null, safety_flag false, accessibility_flag false, confidence 0.5

2.2 WHEN Gemini API returns any other error (timeout, connection failure, etc.) THEN the system SHALL return the same fallback analysis without exposing raw error details to users

2.3 WHEN fallback analysis is used THEN FastAPI SHALL remain running and allow report submission to complete successfully

2.4 WHEN fallback analysis is used THEN the system SHALL log the actual Gemini error details for admin/debugging purposes only

2.5 WHEN Gemini API fails during Campus Pulse generation THEN the system SHALL return basic statistics instead of crashing the analytics endpoint

### Unchanged Behavior (Regression Prevention)

3.1 WHEN Gemini API is available and returns successful results THEN the system SHALL CONTINUE TO return full AI analysis with all fields populated normally

3.2 WHEN Gemini API is available THEN the system SHALL CONTINUE TO perform duplicate detection, priority scoring, and all other existing functionality without any changes

3.3 WHEN Gemini API fails THEN the system SHALL CONTINUE TO allow report submission with fallback analysis (not block report submission)

3.4 WHEN Gemini API fails THEN the system SHALL CONTINUE TO keep authentication, duplicate detection, priority scoring, status history, admin dashboard, and Campus Pulse features intact

3.5 WHEN Gemini API is available THEN the system SHALL CONTINUE TO use the full Gemini analysis for all reports (no fallback behavior)
