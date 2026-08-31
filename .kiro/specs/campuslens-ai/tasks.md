# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Gemini API Error Handling
  - **IMPORTANT**: Write this property-based test BEFORE implementing the fix
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: For deterministic bugs, scope the property to concrete failing cases
  - Test that analyze_issue() exposes raw error text when Gemini returns 429 error
  - Test that analyze_issue() exposes raw error text when Gemini times out
  - Test that generate_campus_pulse() crashes when Gemini returns 429 error
  - Run test on UNFIXED code - expect FAILURE (this confirms the bug exists)
  - Document counterexamples found (e.g., "analyze_issue() with 429 error returns exception with raw text instead of fallback")
  - _Requirements: 1.1, 1.2, 1.3, 2.5_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Normal Gemini Functionality
  - **IMPORTANT**: Follow observation-first methodology
  - Observe: analyze_issue() with valid Gemini returns full analysis with summary, category, severity, etc.
  - Observe: generate_campus_pulse() with valid Gemini returns detailed campus pulse with headline, summary, recommendations
  - Write property-based test: for all valid Gemini responses, result contains all analysis fields with meaningful values
  - Verify test passes on UNFIXED code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 3. Fix for Gemini API failure handling

  - [x] 3.1 Implement the fix in ai_service.py
    - Add try/except block around Gemini API call in analyze_issue()
    - Import logging module and log actual errors
    - Return fallback analysis with specific fields when exception occurs
    - Add try/except block around Gemini API call in generate_campus_pulse()
    - Return basic statistics when exception occurs
    - _Bug_Condition: isBugCondition(api_response) where Gemini API returns error_
    - _Expected_Behavior: expectedBehavior(result) from design - fallback analysis structure_
    - _Preservation: Preservation Requirements from design - all existing functionality unchanged when Gemini available_
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 3.2 Implement the fix in main.py
    - Add try/except around analyze_issue() call in create_report()
    - Ensure report submission completes even with fallback analysis
    - Verify HTTPException doesn't expose raw error details
    - _Bug_Condition: analyze_issue() returns fallback when Gemini fails_
    - _Expected_Behavior: report submission succeeds with fallback data_
    - _Preservation: duplicate detection, priority scoring, etc. work with fallback analysis_
    - _Requirements: 2.3, 3.1, 3.2, 3.3_

  - [x] 3.3 Update error handling in frontend (ReportIssue.jsx)
    - Update error handling to show friendly message when AI is unavailable
    - Display user-friendly message for Gemini failures
    - _Bug_Condition: Gemini API returns error_
    - _Expected_Behavior: user sees friendly message instead of raw error_
    - _Preservation: normal Gemini errors still displayed if relevant_
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 3.4 Update error handling in frontend (MyReports.jsx)
    - Update error display to show "AI analysis is temporarily unavailable. Please try again later."
    - Check for Gemini-related error patterns
    - _Bug_Condition: Gemini API returns error_
    - _Expected_Behavior: user sees friendly message instead of raw error_
    - _Preservation: other errors still displayed appropriately_
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 3.5 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Gemini API Error Handling
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3, 2.5_

  - [x] 3.6 Verify preservation tests still pass
    - **Property 2: Preservation** - Normal Gemini Functionality
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
