import matplotlib.pyplot as plt
from typing import List, Dict
from app.exceptions import NonNumericAttributeException
from app.services.data_ops import DataOperations

class Visualizer:
    @staticmethod
    def create_scatter(data: List[Dict], attr1: str, attr2: str, filename: str = None) -> None:
        if attr1 not in DataOperations.NUMERIC_COLUMNS or attr2 not in DataOperations.NUMERIC_COLUMNS:
            raise NonNumericAttributeException("Both attributes must be numeric for scatter plot.")

        x_vals = []
        y_vals = []

        for row in data:
            try:
                x_vals.append(float(row[attr1]))
                y_vals.append(float(row[attr2]))
            except (ValueError, KeyError):
                continue

        plt.figure(figsize=(10, 6))
        plt.scatter(x_vals, y_vals, alpha=0.6)
        plt.xlabel(attr1.replace('_', ' ').title())
        plt.ylabel(attr2.replace('_', ' ').title())
        plt.title(f'{attr1} vs {attr2}')
        plt.grid(True, alpha=0.3)

        if filename:
            plt.savefig(filename)
            print(f"Scatter plot saved to {filename}")
        else:
            plt.show()
        plt.close()

    @staticmethod
    def create_histogram(data: List[Dict], attribute: str, bins: int, filename: str = None) -> None:
        if attribute not in DataOperations.NUMERIC_COLUMNS:
            raise NonNumericAttributeException(f"The attribute '{attribute}' is not numeric.")

        values = []
        for row in data:
            try:
                values.append(float(row[attribute]))
            except (ValueError, KeyError):
                continue

        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=bins, edgecolor='black', alpha=0.7)
        plt.xlabel(attribute.replace('_', ' ').title())
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {attribute}')
        plt.grid(True, alpha=0.3, axis='y')

        if filename:
            plt.savefig(filename)
            print(f"Histogram saved to {filename}")
        else:
            plt.show()
        plt.close()

    @staticmethod
    def create_boxplot(data: List[Dict], group_by: str, attribute: str, filename: str = None) -> None:
        if attribute not in DataOperations.NUMERIC_COLUMNS:
            raise NonNumericAttributeException(f"The attribute '{attribute}' is not numeric.")

        groups = {}
        for row in data:
            group = row.get(group_by)
            if group:
                if group not in groups:
                    groups[group] = []
                try:
                    groups[group].append(float(row[attribute]))
                except (ValueError, KeyError):
                    continue

        plt.figure(figsize=(10, 6))
        plt.boxplot(groups.values(), labels=groups.keys())
        plt.xlabel(group_by.title())
        plt.ylabel(attribute.replace('_', ' ').title())
        plt.title(f'{attribute} by {group_by}')
        plt.grid(True, alpha=0.3, axis='y')

        if filename:
            plt.savefig(filename)
            print(f"Boxplot saved to {filename}")
        else:
            plt.show()
        plt.close()