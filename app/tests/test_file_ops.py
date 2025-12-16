import unittest
import os
import shutil
import tempfile
from app.services.file_ops import FileOperations


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory for file tests"""
        self.test_dir = tempfile.mkdtemp()
        self.file_ops = FileOperations(data_directory=self.test_dir)
        self.sample_data = [{'col1': 'val1', 'col2': 'val2'}]

    def tearDown(self):
        """Remove the temporary directory after tests"""
        shutil.rmtree(self.test_dir)

    def test_save_and_load_csv(self):
        """Test that data saved is identical when loaded back"""
        filename = "test_file.csv"

        # Save
        self.file_ops.save_csv(filename, self.sample_data)

        # Check if file exists
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

        # Load
        loaded_data = self.file_ops.load_csv(filename)
        self.assertEqual(loaded_data, self.sample_data)

    def test_list_csv_files(self):
        """Test listing CSV files in directory"""
        self.file_ops.save_csv("file1.csv", self.sample_data)
        self.file_ops.save_csv("file2.csv", self.sample_data)
        # Create a non-csv file to ensure it's ignored
        with open(os.path.join(self.test_dir, "ignore.txt"), 'w') as f:
            f.write("text")

        files = self.file_ops.list_csv_files()
        self.assertIn("file1.csv", files)
        self.assertIn("file2.csv", files)
        self.assertNotIn("ignore.txt", files)


if __name__ == '__main__':
    unittest.main()