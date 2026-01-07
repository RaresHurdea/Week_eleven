from typing import List, Dict

def show_help_text():
    print("""
    Available Commands:
    -------------------
    print available_data              - List all CSV files in the data directory
    load <filename>                   - Load data from a CSV file
    filter <attribute> <value>        - Filter data based on attribute and value
    describe <attribute>              - Show min, max, mean for numeric attribute
    unique <attribute>                - Show unique values and their counts
    sort <attribute> <asc|desc>       - Sort data by attribute
    augument <percent> <method>       - Augment data (method: duplicate or create)
    save_random <k> <filename>        - Save k random penguins to a new CSV file
    generate research_groups <k>      - Generate groups of size k with all species (max 10 loaded)
    split_into_groups <threshold>     - Split penguins into 2 groups by mass (max 10 loaded)
    scatter <attr1> <attr2>           - Create scatter plot
    hist <attribute> <bins>           - Create histogram
    boxplot <group> <attribute>       - Create boxplot (group: island or species)
    random_fact                       - Display a random penguin fact
    draw_penguin                      - Draw an ASCII penguin
    img_to_ascii                      - Convert image to ascii
    help                              - Show this help message
    quit                              - Exit the program
    """)

def display_data_rows(data: List[Dict], max_rows: int = 20):
    if not data:
        print("No data to display.")
        return

    print(f"\nDisplaying first {min(len(data), max_rows)} of {len(data)} rows:\n")

    for i, row in enumerate(data[:max_rows]):
        print(f"Penguin {i+1}:")
        for key, value in row.items():
            print(f"  {key}: {value}")
        print()

    if len(data) > max_rows:
        print(f"... and {len(data) - max_rows} more rows")