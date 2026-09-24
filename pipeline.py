import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)

# if verbose flag, use debug
# if no verbose, use info
def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    if verbose:
        LEVEL = logging.DEBUG
    else:
        LEVEL = logging.INFO
        
#setting up format for logger     
# use logger instead of print bc timestamp and severity level   
    logging.basicConfig(
        level = LEVEL, #sets level based on verbose flag
        format = "%(asctime)s %(levelname)-8s %(message)s", #format for timestamp
        datefmt = "%H:%M:%S" #hour, min, sec timestamp
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    #input, output, format, verbose
    parser.add_argument("--input","--i", required = True, help = " path to input file")

    parser.add_argument("--output", "--o", required = True, help = "path to output file")

#format doesn't have a shorthand
    parser.add_argument("--format", choices = ["csv", "json"], default = "csv") #debugging, make sure no space b/w --format

#if v flag, switch to true, otherwise, stays false
    parser.add_argument("--verbose", "--v", action = "store_true")

    return parser.parse_args()



def validate_input(filepath):
    """Check whether the input path exists and is a file."""
#.is_file() checks if the input is a file
    if Path(filepath).is_file():
        logger.info("input file validated: %s", filepath)
        return True
    else:
        logger.error("input file not found: %s", filepath)
        return False


# 1. parse arguments
# 2. set up logging
# 3. log the arguments at DEBUG level
# 4. validate the input
# 5. exit with code 1 if invalid
def main():
    """Main pipeline function."""
    #parse args
    args = parse_arguments()
    #set up logging
    setup_logging(args.verbose)

#verbose flag so set to debug
    logger.debug(
        "arguments parsed: input= %s, output = %s, format = %s",
        args.input,
        args.output,
        args.format 
    )
#validate input
    if not validate_input(args.input):
        sys.exit(1) #quits due to ERROR




if __name__ == "__main__":
    main()