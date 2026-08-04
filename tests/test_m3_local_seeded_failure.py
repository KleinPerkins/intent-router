import unittest


class M3LocalSeededFailure(unittest.TestCase):
    def test_custom_failure_blocks_local_merge(self) -> None:
        self.fail("M3 local evidence: deliberate gating custom-job failure")


if __name__ == "__main__":
    unittest.main()
