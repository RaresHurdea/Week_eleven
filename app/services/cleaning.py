import csv
import os


def analyze_missing_data(input_file='penguins.csv', data_dir='./data'):
    """Reports missing values in CSV"""
    input_path = os.path.join(data_dir, input_file)
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames or []
            missing_counts = {field: 0 for field in fieldnames}
            total_rows = 0

            for row in reader:
                total_rows += 1
                for field in fieldnames:
                    value = row.get(field, '').strip()
                    if not value or value.lower() in ['na', 'n/a', 'nan', 'null', '']:
                        missing_counts[field] += 1

        print("\nMissing Data Analysis:")
        for field, count in missing_counts.items():
            if count > 0:
                print(f"  - {field}: {count} missing")
        print(f"Total rows: {total_rows}")

    except Exception as e:
        print(f"Error analyzing data: {e}")


def preprocess_penguins_data(input_file='penguins.csv', output_file='penguins_data.csv', data_dir='./data'):
    """Cleans raw data and saves to new file"""
    column_mapping = {
        'Species': 'species', 'Island': 'island',
        'Culmen Length (mm)': 'culmen_length_mm', 'Culmen Depth (mm)': 'culmen_depth_mm',
        'Flipper Length (mm)': 'flipper_length_mm', 'Body Mass (g)': 'body_mass_g',
        'Sex': 'sex'
    }
    required_fields = list(column_mapping.values())

    input_path = os.path.join(data_dir, input_file)
    output_path = os.path.join(data_dir, output_file)

    if not os.path.exists(input_path):
        return

    try:
        filtered_data = []
        with open(input_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            input_fieldnames = reader.fieldnames or []

            # Check if input is already clean (has snake_case headers)
            # If so, update mapping to identity
            if set(required_fields).issubset(set(input_fieldnames)):
                column_mapping = {f: f for f in required_fields}

            for row in reader:
                has_all_data = True
                cleaned_row = {}

                for raw, clean in column_mapping.items():
                    val = row.get(raw, '').strip()

                    # Validation
                    if not val or val.lower() in ['na', 'n/a', 'nan', 'null', '.', '']:
                        has_all_data = False
                        break

                    # Specific cleanup
                    if clean == 'species' and '(' in val:
                        val = val.split()[0]
                    if clean == 'sex':
                        val = val.lower()
                    if val == '.':
                        has_all_data = False
                        break

                    cleaned_row[clean] = val

                if has_all_data:
                    filtered_data.append(cleaned_row)

        with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=required_fields)
            writer.writeheader()
            writer.writerows(filtered_data)

        print(f"Cleaned data saved to {output_file}. Rows: {len(filtered_data)}")

    except Exception as e:
        print(f"Error preprocessing: {e}")