import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "--i", required=True, help="path to input file")
    parser.add_argument("--config", required=True, help="path to YAML config file")
    parser.add_argument("--output", "--o", required=True, help="path to output file")
    parser.add_argument("--verbose", "--v", action="store_true")
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments parsed: input=%s, config=%s, output=%s",
                 args.input, args.config, args.output)

    # validate both paths
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # load data and config in one try
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # validate the DataFrame
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]
    rows_loaded = len(data)
    try:
        df = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows", rows_loaded, len(df))

    # process (the "before" copy is made AFTER validation)
    df_before = df.copy()
    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)
    report = create_cleaning_report(df_before, df)
    logger.info("Processing complete: %d -> %d rows", len(df_before), len(df))

    # save
    output_path = save_data(df, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    # print report last
    print("Cleaning report:")
    print(report)


if __name__ == "__main__":
    main()