import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import strip_markdown_for_speech

class BasicTests(unittest.TestCase):
    def test_strip(self):
        x=strip_markdown_for_speech('# Title\n[SHOT-01]\n**こんにちは**。')
        self.assertNotIn('SHOT',x)
        self.assertIn('こんにちは',x)
    def test_core_files(self):
        for rel in ['AGENTS.md','config/channel.yaml','config/production.yaml','episodes/001_google_security/sources.md']:
            self.assertTrue((ROOT/rel).exists(),rel)

if __name__=='__main__': unittest.main()
