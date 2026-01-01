from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using Ollama LLM.
    
    This function uses a large language model to identify and extract
    action items from free-form text, providing better context understanding
    compared to the rule-based extract_action_items() function.
    
    The function requests structured JSON array output from the LLM and
    handles various response formats (pure JSON, markdown-wrapped JSON, etc.).
    If the LLM call fails, it falls back to the rule-based extraction method.
    
    Args:
        text: Input note text to extract action items from
        
    Returns:
        List of extracted action items as strings. Returns empty list if
        input is empty or invalid.
        
    Note:
        Requires Ollama service to be running locally with at least one
        model installed (default: llama3.1). The model can be configured
        via OLLAMA_MODEL environment variable.
    """
    # Handle empty input
    if not text or not text.strip():
        return []
    
    # Get model name from environment variable or use default
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    # Construct prompt to extract action items and request JSON format
    prompt = f"""Extract all action items (todo items, tasks) from the following note text.
Only extract clear, actionable items. Ignore completed items and general descriptions.

Note text:
{text}

Return the result as a JSON array of strings. Format: ["item1", "item2", "item3"]
Return only the JSON array, no additional explanation."""
    
    try:
        # Call Ollama API with structured output request
        response = chat(
            model=model_name,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a professional action item extraction assistant. Always return results as a JSON array of strings in the format: ["item1", "item2", "item3"]. Return only the JSON array, no markdown, no explanations.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.3,  # Lower temperature for more consistent results
                'num_predict': 500,  # Maximum tokens to generate
            }
        )
        
        # Extract content from response
        content = response['message']['content'].strip()
        
        # Handle markdown code blocks (LLM might wrap JSON in ```json ... ```)
        if content.startswith('```'):
            # Remove markdown code block markers
            lines = content.split('\n')
            json_lines = [line for line in lines if not line.strip().startswith('```')]
            content = '\n'.join(json_lines)
        
        # Try to parse JSON directly
        try:
            action_items = json.loads(content)
            if isinstance(action_items, list):
                # Ensure all elements are strings and filter out empty ones
                result = [str(item).strip() for item in action_items if str(item).strip()]
                return result
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the response
            # Look for the first '[' and last ']'
            start_idx = content.find('[')
            end_idx = content.rfind(']')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx + 1]
                try:
                    action_items = json.loads(json_str)
                    if isinstance(action_items, list):
                        result = [str(item).strip() for item in action_items if str(item).strip()]
                        return result
                except json.JSONDecodeError:
                    pass
        
        # Fallback: if JSON parsing fails, try to extract items line by line
        # This handles cases where LLM returns a list but not in JSON format
        lines = content.split('\n')
        extracted = []
        for line in lines:
            line = line.strip()
            # Skip empty lines and JSON structure markers
            if not line or line.startswith('[') or line.startswith(']'):
                continue
            # Remove common list markers
            for prefix in ['-', '*', '•', '"', "'"]:
                if line.startswith(prefix):
                    line = line[len(prefix):].strip()
            # Remove trailing commas and quotes
            line = line.removesuffix(',').strip()
            line = line.removeprefix('"').removesuffix('"').strip()
            if line and not line.startswith('[') and not line.startswith(']'):
                extracted.append(line)
        
        return extracted if extracted else []
        
    except Exception as e:
        # If LLM call fails, fall back to rule-based extraction
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "A",
                    "location": "extract.py:extract_action_items_llm:exception",
                    "message": "Exception caught, falling back",
                    "data": {"error_type": type(e).__name__, "error_message": str(e)},
                    "timestamp": int(datetime.now().timestamp() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion
        # In production, you might want to log this error
        print(f"Error calling Ollama LLM: {e}. Falling back to rule-based extraction.")
        fallback_result = extract_action_items(text)
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "A",
                    "location": "extract.py:extract_action_items_llm:fallback_return",
                    "message": "Returning fallback result",
                    "data": {"fallback_result_count": len(fallback_result), "fallback_result": fallback_result},
                    "timestamp": int(datetime.now().timestamp() * 1000)
                }) + "\n")
        except Exception:
            pass
        # #endregion
        return fallback_result
