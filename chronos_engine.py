"""
Project Chronos: Text Reconstruction Engine
Uses Google Gemini API for AI reconstruction and Custom Search for context
"""

import os
import json
import logging
import requests
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class ChronosEngine:
    def __init__(self):
        """Initialize Chronos engine with API keys"""
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.search_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        logger.info(f"GEMINI_API_KEY available: {bool(self.gemini_key)}")
        logger.info(f"GOOGLE_SEARCH_API_KEY available: {bool(self.search_key)}")
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
    
    def reconstruct_with_gemini(self, text: str) -> Dict:
        """Use Gemini to reconstruct text"""
        if not self.gemini_key:
            logger.warning("No Gemini API key - using fallback")
            return {
                'reconstructed': text,
                'confidence': 0.0,
                'era': 'Unknown',
                'slang': [],
                'explanation': 'Gemini API key not configured'
            }
        
        try:
            prompt = f"""You are an expert in internet history and digital linguistics.
Reconstruct this fragmented internet text by expanding abbreviations and slang:

"{text}"

Respond ONLY with valid JSON (no markdown, no code blocks):
{{
    "reconstructed": "Full expanded version of the text",
    "confidence": 0.95,
    "era": "Time period (e.g., Early 2000s MySpace Era)",
    "slang": ["list", "of", "slang", "terms"],
    "explanation": "Brief explanation of reconstruction"
}}"""
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            # Parse response
            result = json.loads(response.text)
            logger.info(f"Gemini reconstruction successful: {result['reconstructed'][:50]}...")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return {
                'reconstructed': text,
                'confidence': 0.0,
                'era': 'Unknown',
                'slang': [],
                'explanation': f'Could not parse Gemini response: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return {
                'reconstructed': text,
                'confidence': 0.0,
                'era': 'Unknown',
                'slang': [],
                'explanation': f'Gemini API error: {str(e)}'
            }
    
    def search_web(self, query: str) -> List[Dict]:
        """Search web for sources"""
        if not self.search_key or not self.search_engine_id:
            logger.info("No search API configured - using default sources")
            return self.get_default_sources()
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': query,
                'key': self.search_key,
                'cx': self.search_engine_id,
                'num': 5
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                items = response.json().get('items', [])
                sources = [
                    {
                        'title': item['title'],
                        'url': item['link'],
                        'snippet': item['snippet']
                    }
                    for item in items
                ]
                logger.info(f"Found {len(sources)} sources")
                return sources
            else:
                logger.warning(f"Search API error: {response.status_code}")
                return self.get_default_sources()
                
        except Exception as e:
            logger.error(f"Search error: {e}")
            return self.get_default_sources()
    
    def get_default_sources(self) -> List[Dict]:
        """Return default sources when API unavailable"""
        return [
            {
                'title': 'Internet Slang Dictionary - Dictionary.com',
                'url': 'https://www.dictionary.com/e/slang/',
                'snippet': 'Comprehensive dictionary of internet slang and informal language'
            },
            {
                'title': 'Know Your Meme - Internet Culture Archive',
                'url': 'https://knowyourmeme.com/',
                'snippet': 'Documentation of memes and internet culture phenomena'
            },
            {
                'title': 'Internet History - Wikipedia',
                'url': 'https://en.wikipedia.org/wiki/Internet_culture',
                'snippet': 'Overview of internet culture, communication styles, and history'
            }
        ]
    
    def process(self, fragmented_text: str) -> Dict:
        """Main processing pipeline"""
        if not fragmented_text or not fragmented_text.strip():
            return {'error': 'Input text cannot be empty'}
        
        logger.info(f"Processing fragment: {fragmented_text}")
        
        # Step 1: Reconstruct
        reconstruction = self.reconstruct_with_gemini(fragmented_text)
        
        # Step 2: Search for sources
        search_query = f"{' '.join(reconstruction.get('slang', [])[:3])} internet slang history"
        if not search_query.strip():
            search_query = reconstruction.get('era', 'internet history')
        
        sources = self.search_web(search_query)
        
        # Step 3: Build report
        report = {
            'original': fragmented_text,
            'reconstruction': reconstruction['reconstructed'],
            'confidence': reconstruction['confidence'],
            'era': reconstruction['era'],
            'slang_detected': reconstruction['slang'],
            'explanation': reconstruction['explanation'],
            'sources': sources
        }
        
        return report


def format_report_text(report: Dict) -> str:
    """Format report for console display"""
    if 'error' in report:
        return f"Error: {report['error']}"
    
    output = "\n" + "="*70
    output += "\n🏛️  PROJECT CHRONOS - RECONSTRUCTION REPORT"
    output += "\n" + "="*70
    
    output += f"\n\n📜 ORIGINAL FRAGMENT\n> {report['original']}"
    
    output += f"\n\n✨ AI-RECONSTRUCTED TEXT\n> {report['reconstruction']}"
    
    output += f"\n\n📊 CONFIDENCE: {report['confidence']:.0%}"
    output += f"\n📅 ERA: {report['era']}"
    output += f"\n🔤 SLANG DETECTED: {', '.join(report['slang_detected']) or 'None'}"
    output += f"\n💡 EXPLANATION: {report['explanation']}"
    
    output += f"\n\n🔗 SOURCES ({len(report['sources'])} found)"
    for i, source in enumerate(report['sources'], 1):
        output += f"\n{i}. {source['title']}"
        output += f"\n   URL: {source['url']}"
    
    output += "\n\n" + "="*70 + "\n"
    return output


if __name__ == "__main__":
    import sys
    
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "test"
    
    engine = ChronosEngine()
    report = engine.process(text)
    
    if 'error' not in report:
        print(format_report_text(report))
        
        # Save JSON
        with open('reconstruction_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("✅ Report saved to reconstruction_report.json")
    else:
        print(f"❌ {report['error']}")
