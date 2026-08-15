"""Temporary G4-F required-check proof probe."""

import unittest


class TestG4RequirednessProbe(unittest.TestCase):
    def test_required_job_blocks_failure(self):
        self.assertTrue(False, "G4-F requiredness failure proof")
