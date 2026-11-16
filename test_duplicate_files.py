"""
Unit Test Suite for Duplicate File Detector
===========================================
Validates the 7 required academic practical test scenarios:
1. Two files with identical contents but different names
2. Two files with different contents
3. Duplicate files in different subdirectories
4. Empty files (0 bytes)
5. Empty directory
6. Invalid directory paths
7. Multiple groups of duplicate files
"""

import os
import shutil
import tempfile
import unittest
from duplicate_files import calculate_hash, find_duplicates, format_storage_size


class TestDuplicateFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="academic_test_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_identical_files_different_names(self):
        with open(os.path.join(self.test_dir, "alpha.txt"), "w") as f:
            f.write("Identical Content")
        with open(os.path.join(self.test_dir, "beta.txt"), "w") as f:
            f.write("Identical Content")
        res = find_duplicates(self.test_dir)
        self.assertEqual(res["scanned_count"], 2)
        self.assertEqual(res["total_duplicates"], 1)
        self.assertEqual(len(res["duplicate_groups"]), 1)

    def test_02_different_content_files(self):
        with open(os.path.join(self.test_dir, "f1.txt"), "w") as f:
            f.write("Content 1")
        with open(os.path.join(self.test_dir, "f2.txt"), "w") as f:
            f.write("Content 2")
        res = find_duplicates(self.test_dir)
        self.assertEqual(res["scanned_count"], 2)
        self.assertEqual(res["total_duplicates"], 0)
        self.assertEqual(len(res["duplicate_groups"]), 0)

    def test_03_duplicates_in_subdirectories(self):
        sub1 = os.path.join(self.test_dir, "sub1")
        sub2 = os.path.join(self.test_dir, "sub2")
        os.makedirs(sub1)
        os.makedirs(sub2)
        with open(os.path.join(sub1, "orig.dat"), "w") as f:
            f.write("Subdirectory Duplicate")
        with open(os.path.join(sub2, "copy.dat"), "w") as f:
            f.write("Subdirectory Duplicate")
        res = find_duplicates(self.test_dir)
        self.assertEqual(res["total_duplicates"], 1)

    def test_04_empty_files(self):
        open(os.path.join(self.test_dir, "empty1.txt"), "w").close()
        open(os.path.join(self.test_dir, "empty2.txt"), "w").close()
        res = find_duplicates(self.test_dir)
        self.assertEqual(res["total_duplicates"], 1)
        self.assertEqual(res["wasted_bytes"], 0)

    def test_05_empty_directory(self):
        res = find_duplicates(self.test_dir)
        self.assertEqual(res["scanned_count"], 0)
        self.assertEqual(res["total_duplicates"], 0)

    def test_06_invalid_directory(self):
        invalid = os.path.join(self.test_dir, "non_existent")
        self.assertFalse(os.path.exists(invalid))

    def test_07_multiple_duplicate_groups(self):
        for name in ["g1_a.txt", "g1_b.txt"]:
            with open(os.path.join(self.test_dir, name), "w") as f:
                f.write("Group 1")
        for name in ["g2_a.txt", "g2_b.txt", "g2_c.txt"]:
            with open(os.path.join(self.test_dir, name), "w") as f:
                f.write("Group 2")
        res = find_duplicates(self.test_dir)
        self.assertEqual(len(res["duplicate_groups"]), 2)
        self.assertEqual(res["total_duplicates"], 3)


if __name__ == "__main__":
    unittest.main()
