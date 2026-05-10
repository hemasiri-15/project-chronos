"""
chronos_engine.py — Project Chronos Core AI Reconstruction Engine
Author: Hema Siri Guduru (SE24UCSE043), Mahindra University
"""

import os
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
import anthropic
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
  "era": "Era name with approximate date range, e.g. 'MySpace Era (2003–2009)'",
  "platform": "Most likely platform: MySpace | IRC | AIM | MSN | Twitter | Facebook | Tumblr | Reddit | Discord | TikTok | BBS | Unknown",
  "confidence": <integer 0-100>,
  "reconstruction": "Full natural-language reconstruction of what the fragment means in modern English",
  "slang": [
    { "term": "original term", "meaning": "modern English equivalent + brief cultural note" }
  ],
  "context": "2–4 sentences of cultural context about internet culture in this era",
  "sources": [
    { "title": "Reference title", "url": "realistic reference URL" }
  ],
  "wordCount": <number of words in the input fragment>
}

Be historically precise. Sources should cite real domains: knowyourmeme.com, netlingo.com, internetslang.com, dictionary.com/e/slang, web.archive.org."""


class ChronosEngine:
    """
    AI-powered reconstruction engine for fragmented internet communications.

    Uses the Anthropic Claude API to detect era, decode slang, and reconstruct
    the original meaning of internet text artifacts.
    """

    MODEL = "claude-opus-4-5"

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set it in your .env file or pass it directly."
            )
        self.client = anthropic.Anthropic(api_key=key)
        logger.info("ChronosEngine initialized.")

    def analyze(self, fragment: str) -> ReconstructionResult:
        """
        Analyze a text fragment and return a structured ReconstructionResult.

        Args:
            fragment: The internet text fragment to reconstruct.

        Returns:
            ReconstructionResult with era, slang, reconstruction, and sources.

        Raises:
            ValueError: If the API returns unparseable output.
            anthropic.APIError: On API connectivity issues.
        """
        if not fragment.strip():
            raise ValueError("Fragment cannot be empty.")

        logger.info("Analyzing fragment (%d chars)...", len(fragment))

        message = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f'Analyze this internet text fragment: "{fragment}"'}
            ],
        )

        raw = message.content[0].text.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse API response: %s", raw[:200])
            raise ValueError(f"API returned non-JSON output: {exc}") from exc

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

    def analyze_batch(self, fragments: list[str]) -> list[ReconstructionResult]:
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
