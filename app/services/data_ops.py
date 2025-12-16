import random
from typing import List, Dict, Any, Tuple
from app.exceptions import (
    FileNotLoadedException, InvalidColumnException,
    NonNumericAttributeException, PenguinDataException
)


class DataOperations:
    NUMERIC_COLUMNS = {
        'Flipper Length (mm)', 'Culmen Length (mm)', 'Culmen Depth (mm)', 'Body Mass (g)',
        'flipper_length_mm', 'culmen_length_mm', 'culmen_depth_mm', 'body_mass_g'
    }
    STRING_COLUMNS = {
        'Species', 'Island', 'Sex', 'species', 'island', 'sex'
    }

    @staticmethod
    def filter_data(data: List[Dict], attribute: str, value: str) -> List[Dict]:
        if not data:
            raise FileNotLoadedException("No data loaded. Please load a file first.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"The specified column '{attribute}' does not exist.")

        filtered = []
        if attribute in DataOperations.NUMERIC_COLUMNS:
            try:
                numeric_value = float(value)
                for row in data:
                    try:
                        if float(row[attribute]) > numeric_value:
                            filtered.append(row)
                    except (ValueError, KeyError):
                        continue
            except ValueError:
                # Fallback if user provides non-numeric filter for numeric col
                pass
        else:
            for row in data:
                if row.get(attribute) == value:
                    filtered.append(row)
        return filtered

    @staticmethod
    def describe_attribute(data: List[Dict], attribute: str) -> Tuple[float, float, float]:
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"Column '{attribute}' does not exist.")
        if attribute not in DataOperations.NUMERIC_COLUMNS:
            raise NonNumericAttributeException(f"'{attribute}' is not numeric.")

        values = []
        for row in data:
            try:
                values.append(float(row[attribute]))
            except (ValueError, KeyError):
                continue

        if not values:
            raise PenguinDataException(f"No valid numeric values found for '{attribute}'")

        return min(values), max(values), sum(values) / len(values)

    @staticmethod
    def unique_values(data: List[Dict], attribute: str) -> Dict[str, int]:
        if not data:
            raise FileNotLoadedException("No data loaded.")
        if attribute not in data[0]:
            raise InvalidColumnException(f"Column '{attribute}' does not exist.")

        counts = {}
        for row in data:
            val = row.get(attribute, '')
            if val:
                counts[val] = counts.get(val, 0) + 1
        return counts

    @staticmethod
    def augment_data(data: List[Dict], percent: int, method: str) -> List[Dict]:
        if not data:
            raise FileNotLoadedException("No data loaded.")

        num_to_add = int(len(data) * percent / 100)
        new_data = data.copy()

        if method == 'duplicate':
            for _ in range(num_to_add):
                new_data.append(random.choice(data).copy())
        elif method == 'create':
            columns = list(data[0].keys())
            # Simple random generation based on existing data range
            for _ in range(num_to_add):
                new_row = {}
                for col in columns:
                    if col in DataOperations.NUMERIC_COLUMNS:
                        vals = [float(r[col]) for r in data if r.get(col)]
                        if vals:
                            new_row[col] = round(random.uniform(min(vals), max(vals)), 1)
                        else:
                            new_row[col] = 0
                    elif col in DataOperations.STRING_COLUMNS:
                        vals = [r[col] for r in data if r.get(col)]
                        new_row[col] = random.choice(vals) if vals else ''
                    else:
                        new_row[col] = ''
                new_data.append(new_row)
        return new_data

    # --- Sorting Algorithms ---

    @staticmethod
    def _get_comparable_value(row: Dict, key: str) -> Any:
        value = row.get(key, '')
        if key in DataOperations.NUMERIC_COLUMNS:
            try:
                return float(value)
            except (ValueError, TypeError):
                return float('inf')
        return str(value)

    @staticmethod
    def bubble_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                val1 = DataOperations._get_comparable_value(result[j], key)
                val2 = DataOperations._get_comparable_value(result[j + 1], key)

                if reverse:
                    if val1 < val2:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
                else:
                    if val1 > val2:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
            if not swapped:
                break
        return result

    @staticmethod
    def merge_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = DataOperations.merge_sort(data[:mid], key, reverse)
        right = DataOperations.merge_sort(data[mid:], key, reverse)
        return DataOperations._merge(left, right, key, reverse)

    @staticmethod
    def _merge(left, right, key, reverse):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            l_val = DataOperations._get_comparable_value(left[i], key)
            r_val = DataOperations._get_comparable_value(right[j], key)

            condition = (l_val >= r_val) if reverse else (l_val <= r_val)
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def quick_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        pivot_val = DataOperations._get_comparable_value(pivot, key)

        left = []
        middle = []
        right = []

        for item in data:
            val = DataOperations._get_comparable_value(item, key)
            if val < pivot_val:
                left.append(item)
            elif val > pivot_val:
                right.append(item)
            else:
                middle.append(item)

        if reverse:
            return DataOperations.quick_sort(right, key, reverse) + middle + DataOperations.quick_sort(left, key,
                                                                                                       reverse)
        else:
            return DataOperations.quick_sort(left, key, reverse) + middle + DataOperations.quick_sort(right, key,
                                                                                                      reverse)

    @staticmethod
    def insertion_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        result = data.copy()
        for i in range(1, len(result)):
            key_item = result[i]
            key_val = DataOperations._get_comparable_value(key_item, key)
            j = i - 1
            while j >= 0:
                comp_val = DataOperations._get_comparable_value(result[j], key)
                condition = (comp_val < key_val) if reverse else (comp_val > key_val)

                if condition:
                    result[j + 1] = result[j]
                    j -= 1
                else:
                    break
            result[j + 1] = key_item
        return result

    @staticmethod
    def selection_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        result = data.copy()
        for i in range(len(result)):
            extreme_idx = i
            extreme_val = DataOperations._get_comparable_value(result[i], key)

            for j in range(i + 1, len(result)):
                curr_val = DataOperations._get_comparable_value(result[j], key)
                condition = (curr_val > extreme_val) if reverse else (curr_val < extreme_val)

                if condition:
                    extreme_idx = j
                    extreme_val = curr_val

            result[i], result[extreme_idx] = result[extreme_idx], result[i]
        return result