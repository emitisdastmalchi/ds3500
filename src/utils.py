import logging
from pathlib import Path

logger = logging.getLogger(__name__)

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
        format = "%(asctime)s %(levelname)-8s %(name)s — %(message)s", #change to (name)s to print file name in log message
        datefmt = "%H:%M:%S" #hour, min, sec timestamp
    )

def validate_input(filepath):
    """Check whether the input path exists and is a file."""
#.is_file() checks if the input is a file
    if Path(filepath).is_file():
        logger.info("input file validated: %s", filepath)
        return True
    else:
        logger.error("input file not found: %s", filepath)
        return False