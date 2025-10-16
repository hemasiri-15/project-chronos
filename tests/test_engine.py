# tests/test_engine.py
import unittest
from chronos_engine import ChronosReconstructionEngine

class TestEngine(unittest.TestCase):
    def test_process_basic(self):
        engine = ChronosReconstructionEngine()
        r = engine.process("tl;dr thread got locked by mods")
        self.assertIn("original", r)
        self.assertIn("reconstruction", r)
        self.assertIn("sources", r)

if __name__ == "__main__":
    unittest.main()
