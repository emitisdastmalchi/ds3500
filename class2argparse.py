import argparse
from pathlib import Path

# #creating an object
# parser = argparse.ArgumentParser(description="Analyze a data file")

# #adding an input
# parser.add_argument(
#                     "--input",
#                      "-i", 
#                      required=True, 
#                      help="Path to input CSV file")

# #adding an output
# parser.add_argument("--output", 
#                     "-o",
#                     default="results.txt", 
#                     help="Output file path")

# parser.add_argument("--verbose",
#                     "-v",
#                     action="store_true",
#                     help="Print detailed information")

# args = parser.parse_args()
import csv
import sys
from pathlib import Path


def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows


# TODO 1: Create an ArgumentParser
# Description: "Check the quality of a CSV file."
parser = argparse.ArgumentParser(description="Check the quality of a CSV file")


# TODO 2: Add a named argument (required):
# Long form: --input
# Short form: -i
# Help: "CSV file to check"
parser.add_argument("--input",
                    "-r",
                    required=True,
                    help="CSV file to check")


# TODO 3: Add an named argument (optional):
# Long form: --output
# Short form: -o
# Default: "data_quality.txt"
# Help: "Output report filename"
parser.add_argument("--output",
                    "-o",
                    default="data_quality.txt",
                    help="output report filename")

# TODO 4: Add a boolean flag:
# Long form: --verbose
# Short form: -v
# Use action="store_true"
# Help: "Show detailed DEBUG messages"
parser.add_argument("--verbose",
                    "-v",
                    action="store_true",
                    help="show detailed message")

# TODO 5: Parse the command-line arguments
args = parser.parse_args()

# Check if the file exists 
p = Path(args.input)
if not p.is_file():
    print(f"File not found: '{args.input}'")
    sys.exit(1)

print(f"File validated: '{args.input}'")

# Check the data
header, data, missing_rows = check_data(args.input)

# Save the report
with open(args.output, "w") as f:
    f.write(f"Number of rows: {len(data)}\n")
    f.write(f"Number of columns: {len(header)}\n")
    f.write(f"Number of rows with missing values: {len(missing_rows)}\n")

    ### Try These Commands

# ```bash
# python class2_data_checker.py --input students.csv
# ```

# ```bash
# python class2_data_checker.py --input students.csv --output report.txt
# ```
    

git commit -m "Complete CSV data checker CLI"