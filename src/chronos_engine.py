"""
chronos_engine.py — Project Chronos Core AI Reconstruction Engine
Author: Hema Siri Guduru (SE24UCSE043), Mahindra University
Powered by: Google Gemini API
"""

import os
import json
import logging
from dataclasses import dataclass, asdict
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class SlangTerm:
    term: str
    meaning: str


@dataclass
class Source:
    title: str
    url: str


@dataclass
class ReconstructionResult:
    """Structured output of a Chronos analysis."""
    era: str
    platform: str
    confidence: int
    reconstruction: str
    slang: list[SlangTerm]
    context: str
    sources: list[Source]
    word_count: int
    raw_input: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


SYSTEM_PROMPT = """You are the Chronos Engine — an expert in digital archaeology and internet linguistic history.

Analyze fragmented internet text and reconstruct its meaning, cultural era, and context.

Respond with ONLY valid JSON (no markdown fences, no extra text):
{
  "era": "Era name with approximate date range, e.g. 'MySpace Era (2003-2009)'",
  "platform": "Most likely platform: MySpace | IRC | AIM | MSN | Twitter | Facebook | Tumblr | Reddit | Discord | TikTok | BBS | Unknown",
  "confidence": <integer 0-100>,
  "reconstruction": "Full natural-language reconstruction of what the fragment means in modern English",
  "slang": [
    { "term": "original term", "meaning": "modern English equivalent + brief cultural note" }
  ],
  "context": "2-4 sentences of cultural context about internet culture in this era",
  "sources": [
    { "title": "Reference title", "url": "realistic reference URL" }
  ],
  "wordCount": <number of words in the input fragment>
}

Be historically precise. Sources should cite real domains: knowyourmeme.com, netlingo.com, internetslang.com, dictionary.com/e/slang, web.archive.org."""

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class ChronosEngine:
    """
    AI-powered reconstruction engine for fragmented internet communications.
    Uses the Google Gemini API (gemini-2.0-flash) to detect era, decode slang,
    and reconstruct the original meaning of internet text artifacts.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in your .env file or pass it directly.\n"
                "Get a free key at: https://ai.google.dev/"
            )
        logger.info("ChronosEngine initialized (Gemini 2.0 Flash).")

    def _call_gemini(self, user_message: str) -> str:
        """Make a single call to the Gemini API and return raw text output."""
        url = f"{GEMINI_API_URL}?key={self.api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": user_message}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "maxOutputTokens": 1200,
                "temperature": 0.3,
            },
        }

        resp = requests.post(url, json=payload, timeout=30)

        if resp.status_code == 400:
            raise ValueError("Invalid Gemini API key or request. Check your key at https://ai.google.dev/")
        if resp.status_code == 429:
            raise RuntimeError("Gemini API quota exceeded. Wait a moment and try again.")
        if not resp.ok:
            raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError) as exc:
            raise ValueError(f"Unexpected Gemini response structure: {exc}") from exc

    def analyze(self, fragment: str) -> ReconstructionResult:
        """
        Analyze a text fragment and return a structured ReconstructionResult.

        Args:
            fragment: The internet text fragment to reconstruct.

        Returns:
            ReconstructionResult with era, slang, reconstruction, and sources.

        Raises:
            ValueError: If the fragment is empty or the API returns unparseable output.
            RuntimeError: On API connectivity or quota issues.
        """
        if not fragment.strip():
            raise ValueError("Fragment cannot be empty.")

        logger.info("Analyzing fragment (%d chars)...", len(fragment))

        raw = self._call_gemini(f'Analyze this internet text fragment: "{fragment}"')
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse Gemini response: %s", raw[:200])
            raise ValueError(f"Gemini returned non-JSON output: {exc}") from exc

        return ReconstructionResult(
            era=data.get("era", "Unknown Era"),
            platform=data.get("platform", "Unknown"),
            confidence=int(data.get("confidence", 0)),
            reconstruction=data.get("reconstruction", fragment),
            slang=[SlangTerm(**s) for s in data.get("slang", [])],
            context=data.get("context", ""),
            sources=[Source(**s) for s in data.get("sources", [])],
            word_count=data.get("wordCount", len(fragment.split())),
            raw_input=fragment,
        )

    def analyze_batch(self, fragments: list[str]) -> list[Optional[ReconstructionResult]]:
        """Analyze multiple fragments. Returns results in order; failed analyses return None."""
        results = []
        for i, frag in enumerate(fragments, 1):
            logger.info("Processing fragment %d/%d", i, len(fragments))
            try:
                results.append(self.analyze(frag))
            except Exception as exc:
                logger.warning("Fragment %d failed: %s", i, exc)
                results.append(None)
        return results
