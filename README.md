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

## Testing

Run unit tests:
```bash
python -m unittest discover -s tests -v
```

## Troubleshooting

**"GEMINI_API_KEY not found"**
- Verify `.env` file exists in project root
- Check you have a valid Gemini API key from ai.google.dev

**"No reconstruction output"**
- Ensure `.env` has GEMINI_API_KEY set
- Check internet connection
- Verify API key is active

## License

[Your License Choice]

## References

- Google Gemini API: https://ai.google.dev/
- Google Custom Search: https://developers.google.com/custom-search
- Internet Slang: https://www.dictionary.com/e/slang/
