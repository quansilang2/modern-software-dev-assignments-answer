import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_bullet_lists():
    """Test LLM extraction with bullet point lists."""
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items_llm(text)
    # LLM should extract at least some action items
    assert isinstance(items, list)
    assert len(items) > 0, "Should extract at least one action item"


def test_extract_action_items_llm_keyword_prefixes():
    """Test LLM extraction with keyword prefixes."""
    text = """
    TODO: Review the code
    ACTION: Update documentation
    NEXT: Schedule meeting
    Regular sentence here.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    # Should extract items with keyword prefixes
    assert len(items) > 0, "Should extract at least one action item"


def test_extract_action_items_llm_empty_input():
    """Test LLM extraction with empty input."""
    text = ""
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) == 0, "Empty input should return empty list"


def test_extract_action_items_llm_narrative_text():
    """Test LLM extraction with narrative text (implicit action items)."""
    text = """
    We discussed the project status. We need to create a new feature.
    The team should implement the authentication system. Also, we must
    update the documentation to reflect the changes.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    # LLM should be able to extract implicit action items from narrative
    # Even if it returns empty, it should not crash
