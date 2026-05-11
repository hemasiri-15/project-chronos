# 🏛️ Project Chronos — AI Archaeological Engine

> Reconstructing the fragmented linguistic artifacts of the early internet using large language models and contextual analysis.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%20API-4285F4?style=flat&logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)]()

---

## Overview

**Project Chronos** is an AI-powered digital archaeology system that decodes, reconstructs, and contextualizes fragmented internet communications. Given a cryptic text fragment from any internet era — IRC chatrooms, MySpace comments, early forums, AIM conversations, or modern Gen Z vernacular — Chronos produces a structured linguistic analysis with cultural grounding.

This project was developed as part of the Computer Science Engineering curriculum at **Mahindra University** (ID: SE24UCSE043).

---

## Core NLP Features

| Feature | Description |
|---------|-------------|
| **Era Classification** | Identifies the time period of the fragment using temporal linguistic cues and platform-specific markers |
| **Slang Extraction** | Detects and decodes informal abbreviations, neologisms, and platform-specific vernacular |
| **Contextual Reconstruction** | Rewrites the fragment in modern natural English using prompt-guided LLM inference |
| **Confidence Scoring** | Assigns a reliability score (0–100) to each era classification |
| **Cultural Context** | Generates a paragraph situating the fragment in its historical internet moment |
| **Reference Sourcing** | Links to lexicographic and archival sources for each reconstruction |

**Pipeline overview:**
```
Input Fragment
      │
      ▼
Slang Extraction ──► Era Classification (temporal cues + platform markers)
      │                       │
      ▼                       ▼
Contextual Reconstruction ◄── Confidence Scoring
      │
      ▼
Structured JSON Output (era, platform, slang glossary, context, sources)
```

---

## Repository Structure

```
project-chronos/
├── src/
│   ├── chronos_engine.py       # Core reconstruction pipeline
│   ├── era_classifier.py       # Era detection and confidence scoring
│   ├── slang_extractor.py      # Slang term identification and decoding
│   └── search_integration.py  # Web reference sourcing
├── web/
│   └── index.html              # Browser-based interactive demo (Gemini API)
├── tests/
│   ├── test_engine.py          # Unit tests for core engine
│   └── fixtures/               # Sample fragments per era
├── docs/
│   └── research_paper.docx    # IEEE-style research manuscript
├── assets/
│   └── sample_outputs/         # Example JSON reconstructions
├── main.py                     # CLI entrypoint
├── requirements.txt
├── .env.example
└── README.md
```

> **Note:** `src/chronos_engine.py` is the canonical engine module. The root-level `chronos_engine.py` (if present) is a legacy file and can be deleted.

---

## Setup

### 1. Clone

```bash
git clone https://github.com/hemasiri-15/project-chronos.git
cd project-chronos
```

### 2. Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. API Keys

```bash
cp .env.example .env
nano .env
```

```env
GEMINI_API_KEY=AIza-your-key-here
GOOGLE_SEARCH_API_KEY=your-key          # Optional
GOOGLE_SEARCH_ENGINE_ID=your-engine-id  # Optional
```

| Key | Required | Get it at |
|-----|----------|-----------|
| `GEMINI_API_KEY` | ✅ Yes | [ai.google.dev](https://ai.google.dev) — free tier available |
| `GOOGLE_SEARCH_API_KEY` | ⬜ Optional | [console.cloud.google.com](https://console.cloud.google.com) |
| `GOOGLE_SEARCH_ENGINE_ID` | ⬜ Optional | Google Custom Search |

---

## Usage

### CLI

```bash
# Basic reconstruction
python main.py "smh at the top 8 drama. ppl need to chill. g2g, ttyl."

# With cultural context
python main.py --verbose "asl? im in the lobby. brb 10 mins."

# Save JSON report
python main.py --output report.json "no cap fr fr bestie is sus lowkey"

# Batch mode (one fragment per line in a text file)
python main.py --batch fragments.txt

# Machine-readable JSON only
python main.py --json "lol rofl kthxbye"
```

### Python API

```python
from src.chronos_engine import ChronosEngine

engine = ChronosEngine()
result = engine.analyze("smh at the top 8 drama. ppl need to chill.")

print(result.era)            # "MySpace Era (2003–2009)"
print(result.confidence)     # 91
print(result.reconstruction) # "I'm shaking my head at the Top 8 drama..."
for term in result.slang:
    print(f"{term.term} → {term.meaning}")
```

### Web Demo

No server needed — open directly in your browser:

```bash
open web/index.html           # Mac
start web/index.html          # Windows
```

Enter your Gemini API key in the interface. All processing is client-side; no fragment data is stored or sent anywhere except Google's Gemini API.

---

## Sample Output

**Input:** `"smh at the top 8 drama. ppl need to chill. g2g, ttyl."`

```json
{
  "era": "MySpace Era (2003–2009)",
  "platform": "MySpace",
  "confidence": 91,
  "reconstruction": "I'm shaking my head at this Top 8 friend-list drama. People really need to calm down. I have to go now — talk to you later.",
  "slang": [
    { "term": "smh",   "meaning": "shaking my head — expression of disbelief or disappointment" },
    { "term": "top 8", "meaning": "MySpace's friend-ranking feature; a major social signifier of the era" },
    { "term": "ppl",   "meaning": "people" },
    { "term": "g2g",   "meaning": "got to go" },
    { "term": "ttyl",  "meaning": "talk to you later" }
  ],
  "context": "MySpace (2003–2009) was the dominant social network before Facebook...",
  "sources": [
    { "title": "MySpace Top 8 — Know Your Meme", "url": "https://knowyourmeme.com/memes/myspace-top-8" }
  ]
}
```

---

## Supported Eras

| Era | Period | Platforms | Characteristic Slang |
|-----|--------|-----------|----------------------|
| Proto-Internet | 1990–1997 | Usenet, BBS | `IMHO`, `RTFM`, `lurker`, `flame` |
| IRC / Early Chat | 1997–2002 | IRC, ICQ | `asl`, `brb`, `a/s/l`, `ops` |
| IM Golden Age | 2001–2007 | AIM, MSN Messenger | `ttyl`, `lol`, `:-P`, `nm` |
| MySpace Era | 2003–2009 | MySpace | `top 8`, `smh`, `g2g`, `ily` |
| Early Social | 2006–2012 | Facebook, Twitter | `fail`, `epic`, `ftw`, `irl` |
| Tumblr / Reddit | 2010–2016 | Tumblr, Reddit | `feels`, `OTP`, `shipping`, `fandom` |
| Modern Gen Z | 2018–present | TikTok, Discord | `no cap`, `sus`, `slay`, `lowkey` |

---

## Research

An IEEE-style research manuscript documenting the system architecture, NLP pipeline design, evaluation methodology, and results is included at `docs/research_paper.docx`. The manuscript describes a 420-fragment evaluation corpus achieving 87.3% era classification accuracy across the seven eras above.

---

## Testing

```bash
# Run full test suite
python -m unittest discover -s tests -v

# With coverage report
pip install coverage
coverage run -m pytest tests/
coverage report -m
```

---

## Roadmap

- [ ] Multi-language support (non-English internet communities)
- [ ] Fine-tuned era classifier model
- [ ] Google Custom Search integration for live source verification
- [ ] REST API endpoint
- [ ] GitHub Pages deployment for shareable web demo
- [ ] PDF/HTML report export

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/era-detector-v2`
3. Use conventional commits: `git commit -m "feat: add Proto-Internet era detection"`
4. Open a pull request against `main`

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Hema Siri Guduru**  
B.Tech Computer Science Engineering  
Mahindra University, Hyderabad  
ID: SE24UCSE043

---

*"Every fragment is a fossil. Every slang term, a stratum. Chronos reads the rock."*
