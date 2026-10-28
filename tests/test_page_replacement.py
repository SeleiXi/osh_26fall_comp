import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import tempfile
import unittest
from pathlib import Path
from page_replacement import fifo, lru, opt, second_chance, recency_frequency, read_trace

from wfm_experiment import wfm, wfm512
from adaptive import adaptive
from lirs import lirs

class PagingTests(unittest.TestCase):
    def test_classic_trace(self):
        p = '7 0 1 2 0 3 0 4 2 3 0 3 2'.split()
        self.assertEqual(fifo(p, 3), 10)
        self.assertEqual(lru(p, 3), 9)
        self.assertEqual(opt(p, 3), 7)
        self.assertEqual(second_chance(p, 3), 9)
    def test_opt_is_lower_bound(self):
        import random
        rng = random.Random(42)
        for _ in range(100):
            p = [str(rng.randrange(7)) for _ in range(40)]
            for n in (1, 2, 3, 5):
                bound = opt(p, n)
                for algorithm in (fifo, lru, second_chance, recency_frequency, wfm, wfm512, adaptive, lirs):
                    self.assertLessEqual(bound, algorithm(p, n))
    def test_wfm_cycle(self):
        p = list(map(str, range(1, 8))) * 100
        self.assertEqual(wfm(p, 5), 285)
        self.assertEqual(lru(p, 5), 700)
    def test_adaptive_known_results(self):
        p = list(map(str, range(1, 8))) * 100
        self.assertGreaterEqual(adaptive(p, 5), opt(p, 5))
        self.assertLess(adaptive(p, 5), lru(p, 5))
    def test_lirs_pruned_history(self):
        # After 0 is pruned from the stack, a later miss for 0 stays HIR.
        p = '4 4 4 0 4 1 0 3 4'.split()
        self.assertEqual(lirs(p, 2), 5)
        self.assertEqual(lirs(['a', 'b', 'a'], 1), 3)

    def test_input(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'trace.txt'
            p.write_text('  00af\n\n A1 \n', encoding='utf-8')
            self.assertEqual(read_trace(p), ['00af', 'A1'])
            p.write_text('a b\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                read_trace(p)

if __name__ == '__main__':
    unittest.main()
