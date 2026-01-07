from app.services.data_ops import DataOperations
from app.services.file_ops import FileOperations
from app.ui.visualizer import Visualizer
from app.ui.commands import CommandHandler
from app.ui import display


class PenguinAnalyzer:
    def __init__(self, data_directory: str = "./data"):
        self.file_ops = FileOperations(data_directory)
        self.visualizer = Visualizer()

        # Determine sorting algorithm based on name
        self.sorting_algorithms = {
            'bubble': ('Bubble Sort', DataOperations.bubble_sort),
            'insertion': ('Insertion Sort', DataOperations.insertion_sort),
            'selection': ('Selection Sort', DataOperations.selection_sort),
            'quick': ('Quick Sort', DataOperations.quick_sort),
            'merge': ('Merge Sort', DataOperations.merge_sort)
        }

        self.handler = CommandHandler(self.file_ops, self.visualizer, self.sorting_algorithms)

    def run(self):
        print("_-" * 66)
        print("PENGUIN DATA ANALYZER")
        print("_-" * 66)
        print("Type 'help' for available commands or 'quit' to exit.\n")

        while True:
            try:
                command = input(">>> ").strip()
                if not command:
                    continue

                self.process_command(command)

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def process_command(self, command: str):
        parts = command.split()
        user_action = parts[0].lower()

        if user_action == 'quit':
            print("Goodbye!")
            exit(0)

        elif user_action == 'help':
            display.show_help_text()

        elif user_action == 'print' and len(parts) > 1 and parts[1] == 'available_data':
            self.handler.list_files()

        elif user_action == 'load' and len(parts) >= 2:
            self.handler.load_file(parts[1])

        elif user_action == 'filter' and len(parts) >= 3:
            self.handler.filter_data(parts[1], ' '.join(parts[2:]))

        elif user_action == 'describe' and len(parts) >= 2:
            self.handler.describe_attribute(parts[1])

        elif user_action == 'unique' and len(parts) >= 2:
            self.handler.unique_values(parts[1])

        elif user_action == 'sort' and len(parts) >= 3:
            self.handler.sort_data(parts[1], parts[2])

        elif user_action == 'augument' and len(parts) >= 3:
            try:
                percent = int(parts[1])
                method = parts[2]
                self.handler.augment_data(percent, method)
            except ValueError:
                print("Error: Percent must be a number.")

        elif user_action == 'save_random' and len(parts) >= 3:
            try:
                k = int(parts[1])
                filename = parts[2]
                self.handler.save_random(k, filename)
            except ValueError:
                print("Error: k must be an integer.")

        elif user_action == 'generate' and len(parts) >= 3 and parts[1] == 'research_groups':
            try:
                k = int(parts[2])
                self.handler.generate_research_groups(k)
            except ValueError:
                print("Error: k must be an integer.")

        elif user_action == 'split_into_groups' and len(parts) >= 2:
            try:
                threshold = float(parts[1])
                self.handler.split_into_groups(threshold)
            except ValueError:
                print("Error: threshold must be a number.")

        elif user_action == 'scatter' and len(parts) >= 3:
            self.handler.create_scatter(parts[1], parts[2])

        elif user_action == 'hist' and len(parts) >= 3:
            try:
                bins = int(parts[2])
                self.handler.create_histogram(parts[1], bins)
            except ValueError:
                print("Error: Bins must be a number.")

        elif user_action == 'boxplot' and len(parts) >= 3:
            self.handler.create_boxplot(parts[1], parts[2])

        elif user_action == 'random_fact':
            self.handler.random_fact()

        elif user_action == 'draw_penguin':
            self.handler.draw_penguin()

        elif user_action == 'img_to_ascii':
            self.handler.convert_image_to_ascii()

        else:
            print("Unknown command. Type 'help' for available commands.")