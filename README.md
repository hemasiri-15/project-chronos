# Project Chronos: The AI Archeologist

## Student Information
- **Name:** Hema Siri Guduru 
- **ID:** SE24UCSE043
- **Institution:** Mahindra University
- **Department:** CSE

## Project Description

Project Chronos is an AI-powered digital archaeology system that reconstructs fragmented internet artifacts and provides contextual analysis. Using Google Gemini API for intelligent text reconstruction and Google Custom Search for web searching, it transforms obscure historical internet communications into comprehensible, documented reconstructions with relevant sourcing.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/hemasiri-15/project-chronos.git
cd project-chronos
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
Create a `.env` file in the project root:
```bash
nano .env
```

Add your API keys:
```
GEMINI_API_KEY=your_actual_key_from_ai.google.dev
GOOGLE_SEARCH_API_KEY=your_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

**Getting API Keys:**
- **Gemini API:** Visit https://ai.google.dev/ and create a free API key
- **Search API:** Go to https://console.cloud.google.com/ to set up Custom Search

Save the file: `Ctrl+X`, `Y`, `Enter`

## Usage Guide

### Basic Usage
```bash
python main.py "fragmented text here"
```

### Examples

**MySpace Era Text:**
```bash
python main.py "smh at the top 8 drama. ppl need to chill. g2g, ttyl."
```

**IRC Era Text:**
```bash
python main.py "asl? im in the lobby. brb 10 mins."
```

**Modern Slang:**
```bash
python main.py "no cap fr fr bestie is sus lowkey"
```

### Output
The program generates:
1. **Console Report** - Formatted output with reconstruction, confidence score, era, slang detected, and sources
2. **JSON File** - `reconstruction_report.json` with structured data

## Project Structure
```
project-chronos/
├── chronos_engine.py          # Core AI reconstruction and search logic
├── main.py                    # Command-line interface
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env                       # API keys (NEVER commit)
├── .gitignore                 # Git exclusions
├── reconstruction_report.json # Generated output
└── tests/
    └── test_engine.py         # Unit tests
```

## Features

- **Intelligent AI Reconstruction** - Uses Google Gemini to expand cryptic text
- **Confidence Scoring** - Reliability assessment for each reconstruction
- **Era Detection** - Identifies when the text was likely written
- **Automated Web Search** - Finds relevant sources for context
- **JSON Output** - Machine-readable structured data
- **Error Handling** - Graceful fallbacks if APIs unavailable
- **Secure API Management** - Keys never exposed in code

## Technologies Used

- **Python 3.8+**
- **Google Gemini API** - AI text reconstruction
- **Google Custom Search API** - Web searching
- **python-dotenv** - Environment configuration
- **requests** - HTTP operations

## Future Improvements & Roadmap

### Phase 2: Enhanced Features
- Multi-language Support
- Historical Database
- Web UI (Flask/React)
- Batch Processing
- Custom Prompts

### Phase 3: Advanced Capabilities
- Fine-tuned Models
- Platform Detection
- Sentiment Analysis
- PDF/HTML Reports
- REST API

### Known Limitations
- Requires active internet connection
- Limited to Gemini's training data (cutoff: April 2024)
- Cannot reconstruct completely novel terms
- Web search depends on current indexing

## Testing

Run unit tests:
```bash
python -m unittest discover -s tests -v
```

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in project root
2. Check file contains: `GEMINI_API_KEY=your_actual_key`
3. Ensure no spaces around the equals sign
4. Restart terminal after creating/updating `.env`
```bash
cat .env  # Verify file contents
```

---

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

### Issue: "Program returns original text unchanged"

**Cause:** API key not properly configured or Gemini API unavailable

**Solution:**
1. Verify API key is valid at https://ai.google.dev
2. Check internet connection
3. Try again - may be temporary API issue
4. Check logs for error messages
```bash
python main.py "test text" 2>&1 | grep -i error
```

---

### Issue: "No sources found / Empty sources list"

**Cause:** Search API not configured or quota exceeded

**Solution:**
1. Optional - if you didn't set up Google Custom Search API, that's fine
2. System uses fallback sources automatically
3. If you want custom sources, set up `GOOGLE_SEARCH_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID`
4. Check Google Cloud Console for quota limits
```bash
cat .env  # Verify both API keys are set
```

---

### Issue: "JSON parsing error" or "Unexpected Gemini response"

**Cause:** Gemini API returned non-JSON format

**Solution:**
1. Verify API key is active
2. Try with simpler input text
3. Check if API key has usage quota remaining
4. System includes graceful fallback - report still generated

---

### Issue: "Connection timeout" or "Network error"

**Cause:** Internet connectivity issue

**Solution:**
```bash
# Test internet connection
ping google.com

# Try again with longer timeout
python main.py "test"

# Check if APIs are accessible
curl https://generativelanguage.googleapis.com
```

---

### Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: GEMINI_API_KEY not set` | Missing .env file or variable | Create .env with GEMINI_API_KEY |
| `requests.exceptions.Timeout` | API call too slow | Check internet, try again |
| `json.JSONDecodeError` | Gemini returned invalid JSON | Retry, may be temporary |
| `KeyError: 'reconstructed'` | Unexpected API response format | Check API key validity |

## License

[Your License Choice]

## References

- Google Gemini API: https://ai.google.dev/
- Google Custom Search: https://developers.google.com/custom-search
- Internet Slang: https://www.dictionary.com/e/slang/

  ---

## Usage Guide

Once setup is complete, you can run the Project Chronos engine using:

```bash
python main.py "your fragmented text here"

