import os
import csv
from datetime import datetime
from typing import List, Dict


class FileOperations:
    def __init__(self, data_directory: str = "./data"):
        self.data_directory = data_directory
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

    def list_csv_files(self) -> List[str]:
        if not os.path.exists(self.data_directory):
            return []
        return [f for f in os.listdir(self.data_directory) if f.endswith('.csv')]

    def load_csv(self, filename: str) -> List[Dict]:
        filepath = os.path.join(self.data_directory, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filename}' not found in {self.data_directory}")

        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def save_csv(self, filename: str, data: List[Dict]) -> None:
        if not data:
            return
        filepath = os.path.join(self.data_directory, filename)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def log_sorting(self, num_rows: int, algorithm: str, execution_time: float) -> None:
        log_file = os.path.join(self.data_directory, 'sorting_log.csv')
        file_exists = os.path.exists(log_file)

        with open(log_file, 'a', encoding='utf-8', newline='') as f:
            fieldnames = ['date_of_run', 'time_of_run', 'number_of_rows',
                          'sorting_algorithm', 'execution_time_in_seconds']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'date_of_run': datetime.now().strftime('%Y-%m-%d'),
                'time_of_run': datetime.now().strftime('%H:%M:%S'),
                'number_of_rows': num_rows,
                'sorting_algorithm': algorithm,
                'execution_time_in_seconds': f'{execution_time:.6f}'
            })