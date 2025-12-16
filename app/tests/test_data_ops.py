import unittest
from app.services.data_ops import DataOperations
from app.exceptions import NonNumericAttributeException, InvalidColumnException

class TestDataOperations(unittest.TestCase):

    def setUp(self):
        """Set up a sample dataset for testing"""
        self.sample_data = [
            {'species': 'Adelie', 'body_mass_g': '3750', 'flipper_length_mm': '181'},
            {'species': 'Gentoo', 'body_mass_g': '5000', 'flipper_length_mm': '210'},
            {'species': 'Adelie', 'body_mass_g': '3200', 'flipper_length_mm': '190'},
            {'species': 'Chinstrap', 'body_mass_g': '3750', 'flipper_length_mm': '195'},
        ]

    def test_describe_attribute(self):
        """Test calculation of min, max, and mean"""
        min_val, max_val, mean_val = DataOperations.describe_attribute(self.sample_data, 'body_mass_g')
        self.assertEqual(min_val, 3200.0)
        self.assertEqual(max_val, 5000.0)
        self.assertEqual(mean_val, 3925.0)

    def test_describe_attribute_invalid_col(self):
        """Test that invalid columns raise exceptions"""
        with self.assertRaises(InvalidColumnException):
            DataOperations.describe_attribute(self.sample_data, 'non_existent_col')

    def test_filter_data_numeric(self):
        """Test filtering by numeric value (greater than)"""
        # Filter penguins heavier than 4000g
        result = DataOperations.filter_data(self.sample_data, 'body_mass_g', '4000')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['species'], 'Gentoo')

    def test_filter_data_string(self):
        """Test filtering by exact string match"""
        result = DataOperations.filter_data(self.sample_data, 'species', 'Adelie')
        self.assertEqual(len(result), 2)

    def test_unique_values(self):
        """Test counting unique occurrences"""
        counts = DataOperations.unique_values(self.sample_data, 'species')
        self.assertEqual(counts['Adelie'], 2)
        self.assertEqual(counts['Gentoo'], 1)
        self.assertEqual(counts['Chinstrap'], 1)

    def test_merge_sort_asc(self):
        """Test Merge Sort in ascending order"""
        sorted_data = DataOperations.merge_sort(self.sample_data, 'body_mass_g', reverse=False)
        self.assertEqual(float(sorted_data[0]['body_mass_g']), 3200)
        self.assertEqual(float(sorted_data[-1]['body_mass_g']), 5000)

    def test_quick_sort_desc(self):
        """Test Quick Sort in descending order"""
        sorted_data = DataOperations.quick_sort(self.sample_data, 'flipper_length_mm', reverse=True)
        self.assertEqual(float(sorted_data[0]['flipper_length_mm']), 210)
        self.assertEqual(float(sorted_data[-1]['flipper_length_mm']), 181)

if __name__ == '__main__':
    unittest.main()