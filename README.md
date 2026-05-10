# 🏛️ Project Chronos — AI Archaeological Engine

> Reconstructing the fragmented linguistic artifacts of the early internet using large language models and contextual analysis.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
<<<<<<< HEAD
[![Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%20API-4285F4?style=flat&logo=google)](https://ai.google.dev)
=======
[![Claude API](https://img.shields.io/badge/Powered%20by-Claude%20API-D97706?style=flat)](https://anthropic.com)
>>>>>>> d5d35f2 (Removed duplicate and obsolete files)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)]()

---

## Overview

**Project Chronos** is an AI-powered digital archaeology system that decodes, reconstructs, and contextualizes fragmented internet communications. Given a cryptic text fragment from any internet era — IRC chatrooms, MySpace comments, early forums, AIM conversations, or modern Gen Z vernacular — Chronos produces:

- A **full natural-language reconstruction** of the original meaning
- **Era detection** with confidence scoring (e.g., *MySpace Era, 2003–2008*)
- A **slang glossary** mapping each term to its modern equivalent
- **Cultural context** situating the fragment in its historical internet moment
- **Reference sources** for academic citation

This project was developed as part of the Computer Science Engineering curriculum at **Mahindra University** (ID: SE24UCSE043) and has been submitted for academic publication.

---

## Live Demo

<<<<<<< HEAD
Open `web/index.html` in any browser and enter your Gemini API key. The demo runs entirely client-side — no backend required, no data stored.
=======
Open `web/index.html` in any browser and enter your Anthropic API key. The demo runs entirely client-side — no backend required, no data stored.
>>>>>>> d5d35f2 (Removed duplicate and obsolete files)

---

## Architecture

```
chronos-repo/
├── src/
│   ├── chronos_engine.py       # Core AI reconstruction engine
│   ├── era_classifier.py       # Era detection and confidence scoring
│   ├── slang_extractor.py      # Slang term identification
│   └── search_integration.py  # Web reference sourcing
├── web/
<<<<<<< HEAD
│   └── index.html              # Browser-based interactive demo (Gemini API)
=======
│   └── index.html              # Browser-based interactive demo (Claude API)
>>>>>>> d5d35f2 (Removed duplicate and obsolete files)
├── tests/
│   ├── test_engine.py          # Unit tests for core engine
│   └── fixtures/               # Sample fragments per era
├── docs/
│   └── research_paper.pdf      # Published IEEE-style research paper
├── assets/
│   └── sample_outputs/         # Example JSON reconstructions
├── main.py                     # CLI entrypoint
├── requirements.txt            # Python dependencies
├── .env.example                # API key template
└── README.md
```

---

## Setup

### 1. Clone

```bash
git clone https://github.com/hemasiri-15/project-chronos.git
cd project-chronos
```

### 2. Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env
nano .env
```

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_SEARCH_API_KEY=your-key          # Optional: for web sourcing
GOOGLE_SEARCH_ENGINE_ID=your-engine-id  # Optional
```

| Key | Required | Source |
|-----|----------|--------|
<<<<<<< HEAD
| `GEMINI_API_KEY` | ✅ Yes | [ai.google.dev](https://ai.google.dev) |
=======
| `ANTHROPIC_API_KEY` | ✅ Yes | [console.anthropic.com](https://console.anthropic.com) |
>>>>>>> d5d35f2 (Removed duplicate and obsolete files)
| `GOOGLE_SEARCH_API_KEY` | ⬜ Optional | [console.cloud.google.com](https://console.cloud.google.com) |
| `GOOGLE_SEARCH_ENGINE_ID` | ⬜ Optional | Google Custom Search |

---

## Usage

### CLI

```bash
# Basic reconstruction
python main.py "smh at the top 8 drama. ppl need to chill. g2g, ttyl."

# With verbose output
python main.py --verbose "asl? im in the lobby. brb 10 mins."

# Save JSON report
python main.py --output report.json "no cap fr fr bestie is sus lowkey"

# Batch mode (file of fragments)
python main.py --batch fragments.txt
```

### Python API

```python
from src.chronos_engine import ChronosEngine

engine = ChronosEngine()
result = engine.analyze("smh at the top 8 drama. ppl need to chill.")

print(result.era)              # "MySpace Era (2003–2009)"
print(result.confidence)       # 87
print(result.reconstruction)   # "I'm shaking my head at the drama..."
print(result.slang)            # [{"term": "smh", "meaning": "shaking my head"}, ...]
```

### Web Demo

```bash
# No server needed — open directly
open web/index.html
```

<<<<<<< HEAD
Enter your Gemini API key in the interface. All processing happens in your browser.
=======
Enter your Anthropic API key in the interface. All processing happens in your browser.
>>>>>>> d5d35f2 (Removed duplicate and obsolete files)

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
    { "term": "smh",      "meaning": "shaking my head (expression of disbelief)" },
    { "term": "top 8",    "meaning": "MySpace's friend-ranking feature, a major social signifier" },
    { "term": "ppl",      "meaning": "people" },
    { "term": "g2g",      "meaning": "got to go" },
    { "term": "ttyl",     "meaning": "talk to you later" }
  ],
  "context": "The 'Top 8' was a defining feature of early MySpace culture...",
  "sources": [
    { "title": "MySpace Top 8: A Social History", "url": "https://knowyourmeme.com/memes/myspace-top-8" }
  ]
}
```

---

## Supported Eras

| Era | Period | Platforms | Example Slang |
|-----|--------|-----------|---------------|
| Proto-Internet | 1990–1997 | Usenet, BBS | `IMHO`, `RTFM`, `lurker` |
| IRC / Early Chat | 1997–2002 | IRC, ICQ | `asl`, `brb`, `a/s/l` |
| IM Golden Age | 2001–2007 | AIM, MSN | `ttyl`, `lol`, `:-P` |
| MySpace Era | 2003–2009 | MySpace | `top 8`, `smh`, `g2g` |
| Early Social | 2006–2012 | Facebook, Twitter | `fail`, `epic`, `ftw` |
| Tumblr / Reddit | 2010–2016 | Tumblr, Reddit | `feels`, `OTP`, `shipping` |
| Modern Gen Z | 2018–present | TikTok, Discord | `no cap`, `sus`, `slay` |

---

## Research

This project is the subject of a peer-reviewed research paper:

> **Guduru, H. S.** (2025). *Project Chronos: AI-Assisted Reconstruction of Fragmented Internet Linguistic Artifacts*. Submitted to IEEE International Conference on Natural Language Processing and Computational Linguistics.

Full paper available in `docs/research_paper.docx`.

---

## Testing

```bash
# Full test suite
python -m unittest discover -s tests -v

# Coverage report
pip install coverage
coverage run -m pytest tests/
coverage report -m
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/era-detector-v2`
3. Commit with conventional commits: `git commit -m "feat: add Proto-Internet era detection"`
4. Open a pull request

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
