import pytest
from app import get_system_prompt, analyze_decision

def test_system_prompt_alignment():
    """[Testing & Problem Statement Alignment] Check karta hai ki AI ko decision lene se rokne wali rule prompt mein hai ya nahi."""
    prompt = get_system_prompt()
    assert "NEVER make the decision" in prompt, "Prompt is missing the critical boundary rule!"
    assert "Socratic" in prompt, "Prompt should mention Socratic questioning."

def test_invalid_api_key_format():
    """[Testing & Security] Check karta hai ki fake API keys properly block ho rahi hain."""
    result = analyze_decision("invalid_key_123", "I want to buy a new electric vehicle.")
    assert result is None, "Function should return None for invalid API keys."

def test_input_validation():
    """[Testing & Efficiency] Check karta hai ki empty string prompt pass hone par fail safe active hai."""
    result = analyze_decision("", "")
    assert result is None, "Empty inputs should be caught by validation."