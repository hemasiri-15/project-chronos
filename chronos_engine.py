# chronos_engine.py
import os
import time
import logging
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load env
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
CSE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("chronos")

# Try/except import for google-genai so file can be imported during tests without keys.
try:
    from google import genai
except Exception:
    genai = None
    logger.warning("google-genai not available; gemini calls will be skipped in this environment.")

# --- Helpers ---
def exponential_backoff(attempt: int, base: float = 0.5, cap: float = 8.0):
    sleep_for = min(cap, base * (2 ** attempt))
    time.sleep(sleep_for)

def safe_request_get(url: str, params: dict, max_retries: int = 3, timeout: int = 10) -> dict:
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.warning("Request failed (attempt %d): %s", attempt + 1, e)
            if attempt + 1 == max_retries:
                logger.error("Max retries reached for %s", url)
                raise
            exponential_backoff(attempt)

# --- Gemini (GenAI) call ---
def call_gemini_reconstruct(fragment: str, model_name: str = "gemini-1.5-pro") -> Dict[str, Any]:
    """
    Calls Gemini via google-genai and returns a dict with 'reconstruction' and 'rationale'.
    If genai is not available or key not set, returns a fallback message.
    """
    if genai is None or GEMINI_KEY is None:
        logger.info("GenAI SDK or GEMINI_API_KEY not configured; returning fallback.")
        return {"reconstruction": fragment, "rationale": "No Gemini call made (SDK or key missing).", "inferred": []}

    # Configure the client (this uses environment auth; key may be set differently per SDK)
    genai.configure(api_key=GEMINI_KEY)  # can raise if not configured

    prompt = f"""
You are an editor reconstructing an informal, fragmented internet post into a single clear sentence.
1) Provide the reconstructed sentence.
2) On the next line, provide a short rationale (1-2 lines) and mark any inferred words with [INFERRED].
Output in JSON with keys: reconstruction, rationale, inferred_tokens.
Fragment: \"\"\"{fragment}\"\"\""""

    # Use a simple call pattern for the SDK. Adapt if the SDK API differs.
    try:
        model = genai.Model(model_name)
        response = model.generate(prompt=prompt, max_output_tokens=400)
        text = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        logger.exception("Gemini call failed: %s", e)
        return {"reconstruction": fragment, "rationale": f"Gemini call failed: {e}", "inferred": []}

    # Basic parsing: try to extract reconstruction (best-effort).
    # The model prompt asks for JSON-like output, but be defensive.
    # For demo, we return the entire text as reconstruction.
    return {"reconstruction": text.strip(), "rationale": "Model-provided rationale (raw).", "inferred": []}

# --- Google Custom Search (CSE) ---
def google_custom_search(query: str, num: int = 3) -> List[Dict[str, Any]]:
    if not GOOGLE_SEARCH_KEY or not CSE_ID:
        logger.info("GOOGLE_SEARCH_KEY or CSE_ID not configured; skipping search.")
        return []

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_SEARCH_KEY, "cx": CSE_ID, "q": query, "num": num}
    try:
        data = safe_request_get(url, params)
    except Exception:
        logger.exception("Custom Search request failed for query: %s", query)
        return []

    items = data.get("items", [])
    results = []
    for it in items:
        results.append({
            "title": it.get("title"),
            "link": it.get("link"),
            "snippet": it.get("snippet"),
            "displayLink": it.get("displayLink"),
        })
    return results

# --- Main engine class ---
class ChronosReconstructionEngine:
    def __init__(self):
        self.model_name = "gemini-1.5-pro"

    def process(self, fragment: str) -> Dict[str, Any]:
        logger.info("Processing fragment: %s", fragment)
        # 1) Normalize basic whitespace
        original = fragment.strip()

        # 2) Call Gemini to reconstruct
        try:
            gemini_out = call_gemini_reconstruct(original, model_name=self.model_name)
        except Exception as e:
            logger.exception("Error calling Gemini: %s", e)
            gemini_out = {"reconstruction": original, "rationale": f"Error: {e}", "inferred": []}

        reconstructed_text = gemini_out.get("reconstruction", original)

        # 3) Auto-keyword extraction (very simple): top N words, remove very short tokens
        tokens = [t for t in reconstructed_text.split() if len(t) > 2]
        query = " ".join(tokens[:6]) if tokens else original

        # 4) Search web for context
        try:
            sources = google_custom_search(query, num=3)
        except Exception:
            sources = []

        # 5) Build report
        report = {
            "original": original,
            "reconstruction": reconstructed_text,
            "rationale": gemini_out.get("rationale"),
            "inferred_tokens": gemini_out.get("inferred", []),
            "query_used_for_search": query,
            "sources": sources,
            "meta": {"engine": "ChronosReconstructionEngine", "model": self.model_name, "timestamp": time.time()},
        }
        return report

# Utility for printing a basic formatted report
def format_report_text(report: dict) -> str:
    lines = []
    lines.append("=== Project Chronos: Reconstruction Report ===")
    lines.append(f"Original: {report.get('original')}")
    lines.append("")
    lines.append("Reconstruction:")
    lines.append(report.get("reconstruction", ""))
    lines.append("")
    lines.append("Rationale:")
    lines.append(report.get("rationale", ""))
    lines.append("")
    lines.append("Sources:")
    for s in report.get("sources", []):
        lines.append(f"- {s.get('title')} ({s.get('displayLink')}): {s.get('link')}")
        lines.append(f"  snippet: {s.get('snippet')}")
    return "\n".join(lines)
