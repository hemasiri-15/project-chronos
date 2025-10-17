#!/usr/bin/env python3
import sys
import json
from chronos_engine import ChronosEngine, format_report_text

def main():
    print("\n🏛️  PROJECT CHRONOS - AI Archeologist v1.0")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        fragmented_text = " ".join(sys.argv[1:])
    else:
        fragmented_text = "smh at the top 8 drama. ppl need to chill. g2g, ttyl."
        print(f"\n📝 Using default example: '{fragmented_text}'")
    
    try:
        engine = ChronosEngine()
        report = engine.process(fragmented_text)
        
        if 'error' in report:
            print(f"\n❌ Error: {report['error']}")
        else:
            formatted = format_report_text(report)
            print(formatted)
            
            with open("reconstruction_report.json", 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            print("✅ JSON report saved to reconstruction_report.json")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
