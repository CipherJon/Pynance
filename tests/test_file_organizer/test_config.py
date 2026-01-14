import unittest
from pathlib import Path

from file_organizer.config import (
    BASE_DIR,
    DATE_ORGANIZATION,
    DUPLICATE_HANDLING,
    FILE_TYPES,
    DateOrganization,
    DuplicateHandling,
)


class TestConfig(unittest.TestCase):
    def test_base_dir(self):
        """Test that BASE_DIR is a Path object."""
        self.assertIsInstance(BASE_DIR, Path)
        self.assertTrue(str(BASE_DIR).endswith("Downloads"))

    def test_file_types_structure(self):
        """Test that FILE_TYPES has the correct structure."""
        self.assertIsInstance(FILE_TYPES, dict)
        for category, extensions in FILE_TYPES.items():
            self.assertIsInstance(category, str)
            self.assertIsInstance(extensions, list)
            for ext in extensions:
                self.assertIsInstance(ext, str)
                self.assertTrue(ext.startswith("."))

    def test_file_types_categories(self):
        """Test that FILE_TYPES contains expected categories."""
        expected_categories = [
            "images",
            "documents",
            "archives",
            "videos",
            "music",
            "others",
        ]
        for category in expected_categories:
            self.assertIn(category, FILE_TYPES)

    def test_duplicate_handling_defaults(self):
        """Test DuplicateHandling dataclass defaults."""
        dh = DuplicateHandling()
        self.assertTrue(dh.enabled)
        self.assertEqual(dh.detection_method, "hash")
        self.assertEqual(dh.handle_duplicates, "move")
        self.assertEqual(dh.duplicates_dir, "_duplicates")

    def test_date_organization_defaults(self):
        """Test DateOrganization dataclass defaults."""
        do = DateOrganization()
        self.assertFalse(do.enabled)
        self.assertTrue(do.use_creation_date)
        self.assertEqual(do.folder_format, "monthly")

    def test_duplicate_handling_config(self):
        """Test DUPLICATE_HANDLING configuration."""
        self.assertIsInstance(DUPLICATE_HANDLING, DuplicateHandling)
        self.assertTrue(DUPLICATE_HANDLING.enabled)

    def test_date_organization_config(self):
        """Test DATE_ORGANIZATION configuration."""
        self.assertIsInstance(DATE_ORGANIZATION, DateOrganization)
        self.assertFalse(DATE_ORGANIZATION.enabled)


if __name__ == "__main__":
    unittest.main()
