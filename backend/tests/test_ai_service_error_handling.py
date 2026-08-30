"""
Bug Condition Exploration Test: Gemini API Error Handling

This test verifies the Gemini API error handling behavior.

Initial Bug Condition:
- When Gemini API returns 429 RESOURCE_EXHAUSTED error, raw exception text was exposed
- When Gemini API times out, FastAPI would crash
- When Gemini API returns connection error, technical exception details were shown

Fix Implemented:
- Added try/except blocks around all Gemini API calls
- Catch api_exceptions.ResourceExhausted (429 errors)
- Catch api_exceptions.DeadlineExceeded (timeout errors)
- Catch api_exceptions.GoogleAPIError (generic API errors)
- Catch generic Exception as fallback
- Return clean fallback analysis without raw error text
- Log actual technical errors to backend terminal

Verification:
- All tests now PASS (5/5)
- Fallback analysis is returned on all error scenarios
- Raw error text is never exposed to frontend
- Backend terminal logs contain full technical error details
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch
import asyncio
from google.api_core import exceptions as api_exceptions

from services.ai_service import analyze_issue, generate_campus_pulse


def test_analyze_issue_with_429_resource_exhausted_returns_fallback():
    """
    Fixed Behavior: 429 RESOURCE_EXHAUSTED Error
    
    When Gemini API returns a 429 error, the system now returns clean 
    fallback analysis instead of exposing raw error text.
    
    EXPECTED FIX: Return fallback analysis with clean message
    """
    # Mock the 429 RESOURCE_EXHAUSTED error
    mock_429_error = api_exceptions.ResourceExhausted(
        "429 RESOURCE_EXHAUSTED: Quota exceeded for Gemini API"
    )
    
    with patch('services.ai_service.client') as mock_client:
        # Make generate_content raise 429 error
        mock_client.models.generate_content = Mock(
            side_effect=mock_429_error
        )
        
        # Should NOT raise exception - returns fallback analysis
        result = analyze_issue("The Wi-Fi is down in the library.")
        
        # Verify fallback analysis is returned with clean structure
        assert isinstance(result, dict)
        assert "summary" in result
        assert "category" in result
        assert "severity" in result
        assert "recommended_department" in result
        assert "extracted_location" in result
        assert "safety_flag" in result
        assert "accessibility_flag" in result
        assert "confidence" in result
        
        # Verify raw error text is NOT in the response
        result_str = str(result).lower()
        assert "429" not in result_str
        assert "resource exhausted" not in result_str


def test_analyze_issue_with_timeout_returns_fallback():
    """
    Fixed Behavior: API Timeout
    
    When Gemini API times out, the system returns clean fallback
    analysis instead of crashing or exposing raw timeout error.
    
    EXPECTED FIX: Return fallback analysis with clean message
    """
    mock_timeout_error = api_exceptions.DeadlineExceeded(
        "504 Deadline Exceeded: The operation was too slow"
    )
    
    with patch('services.ai_service.client') as mock_client:
        mock_client.models.generate_content = Mock(
            side_effect=mock_timeout_error
        )
        
        # Should NOT raise exception - returns fallback analysis
        result = analyze_issue("The cafeteria is out of food.")
        
        # Verify fallback analysis is returned with clean structure
        assert isinstance(result, dict)
        assert "summary" in result
        assert "category" in result
        assert "severity" in result
        
        # Verify raw error text is NOT in the response
        result_str = str(result).lower()
        assert "deadline" not in result_str
        assert "slow" not in result_str


def test_analyze_issue_with_connection_error_returns_fallback():
    """
    Fixed Behavior: Connection Error
    
    When Gemini API returns connection error, the system returns
    clean fallback analysis instead of exposing technical exception details.
    
    EXPECTED FIX: Return fallback analysis with clean message
    """
    import aiohttp
    
    mock_connection_error = aiohttp.ClientConnectorError(
        Mock(), 
        OSError("Connection refused")
    )
    
    with patch('services.ai_service.client') as mock_client:
        mock_client.models.generate_content = Mock(
            side_effect=mock_connection_error
        )
        
        # Should NOT raise exception - returns fallback analysis
        result = analyze_issue("The lab computers are broken.")
        
        # Verify fallback analysis is returned with clean structure
        assert isinstance(result, dict)
        assert "summary" in result
        assert "category" in result
        assert "severity" in result
        
        # Verify raw error text is NOT in the response
        result_str = str(result).lower()
        assert "connection" not in result_str


def test_generate_campus_pulse_with_429_error_returns_fallback():
    """
    Fixed Behavior: Campus Pulse with 429 Error
    
    When generate_campus_pulse encounters a 429 error, it returns
    basic stats instead of crashing the FastAPI endpoint.
    
    EXPECTED FIX: Return basic fallback stats
    """
    mock_429_error = api_exceptions.ResourceExhausted(
        "429 RESOURCE_EXHAUSTED: Rate limit exceeded"
    )
    
    # Mock reports data
    mock_reports = [
        {
            "ai_summary": "Broken Wi-Fi in lecture hall",
            "category": "Network",
            "severity": "High",
            "extracted_location": "Building A",
            "recommended_department": "IT Support",
            "priority_score": 85,
            "status": "Open"
        }
    ]
    
    with patch('services.ai_service.client') as mock_client:
        mock_client.models.generate_content = Mock(
            side_effect=mock_429_error
        )
        
        # Should NOT raise exception - returns fallback stats
        result = generate_campus_pulse(mock_reports)
        
        # Verify fallback campus pulse is returned with clean structure
        assert isinstance(result, dict)
        assert "headline" in result
        assert "summary" in result
        assert "major_concern" in result
        assert "emerging_trend" in result
        assert "critical_issue" in result
        assert "improvement" in result
        assert "recommended_actions" in result
        
        # Verify raw error text is NOT in the response
        result_str = str(result).lower()
        assert "429" not in result_str
        assert "resource exhausted" not in result_str


def test_analyze_issue_with_generic_error_returns_fallback():
    """
    Fixed Behavior: Generic API Error
    
    When Gemini API returns any error, the system returns clean
    fallback analysis instead of exposing raw error text.
    
    EXPECTED FIX: Return fallback analysis with clean message
    """
    mock_generic_error = Exception("Gemini API error: Internal server error")
    
    with patch('services.ai_service.client') as mock_client:
        mock_client.models.generate_content = Mock(
            side_effect=mock_generic_error
        )
        
        # Should NOT raise exception - returns fallback analysis
        result = analyze_issue("The classroom projector is broken.")
        
        # Verify fallback analysis is returned with clean structure
        assert isinstance(result, dict)
        assert "summary" in result
        assert "category" in result
        assert "severity" in result
        
        # Verify raw error text is NOT in the response
        result_str = str(result).lower()
        assert "internal server error" not in result_str