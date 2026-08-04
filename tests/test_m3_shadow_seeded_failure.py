import unittest


class M3ShadowSeededFailure(unittest.TestCase):
    def test_custom_failure_is_informational_in_shadow(self) -> None:
        self.fail("M3 shadow evidence: deliberate custom-job failure")


if __name__ == "__main__":
    unittest.main()
