import csv
import os


def create_sample_penguins_csv(output_file='penguins.csv', data_dir='./data'):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    output_path = os.path.join(data_dir, output_file)

    # Headers matching original raw data
    sample_data = [
        ['Species', 'Island', 'Culmen Length (mm)', 'Culmen Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)', 'Sex'],
        ['Adelie', 'Torgersen', '39.1', '18.7', '181', '3750', 'MALE'],
        ['Adelie', 'Torgersen', '39.5', '17.4', '186', '3800', 'FEMALE'],
        ['Gentoo', 'Biscoe', '46.1', '13.2', '211', '4500', 'FEMALE'],
        ['Chinstrap', 'Dream', '46.5', '17.9', '192', '3500', 'FEMALE'],
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

    print(f"Sample data created at {output_path}")