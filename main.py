# main.py
import sys
from chronos_engine import ChronosReconstructionEngine, format_report_text

def main():
    if len(sys.argv) > 1:
        fragmented_text = " ".join(sys.argv[1:])
    else:
        fragmented_text = "smh at the top 8 drama. ppl need to chill. g2g, ttyl."

    engine = ChronosReconstructionEngine()
    report = engine.process(fragmented_text)

    if 'error' in report:
        print(f"❌ Error: {report['error']}")
    else:
        print(format_report_text(report))

if __name__ == "__main__":
    main()
