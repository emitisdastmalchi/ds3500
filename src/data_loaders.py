from pathlib import Path
import logging
import pandas as pd
import json
import yaml

# Do not call logging.basicConfig() here.
# Why: pipeline.py's setup_logging() is the ONE place that configures
# logging for the whole program. Every other module just grabs its own
# named logger (below) and writes to it — the actual level/format/output
# destination is controlled centrally.
logger = logging.getLogger(__name__)
# __name__ here evaluates to "data_loaders" — this is what makes your log
# lines later show "data_loaders" as the source, distinct from "__main__".


def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    # TODO:
    # - Use pd.read_csv(filepath) to load the file into a DataFrame.
    df = pd.read_csv(filepath)

    # - Log an INFO message that includes the filepath AND the row count.
    #   (Use len() on the DataFrame to get row count.)

    logger.info("Loaded CSV file: %s (%d rows)", filepath, len(df))
    #   Why INFO and not DEBUG? Because "I successfully loaded your file"
    #   is useful to see on every normal run, not just when debugging. also debug is for BTS updates
    # - Return the DataFrame.
    return df 


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).
    filepath is a Path object.
    """
    # TODO:
    # - Open the file using a `with open(filepath) as f:` block.
    #   Why `with`? It guarantees the file gets closed automatically,
    #   even if something goes wrong while reading it.
    # - Inside that block, use json.load(f) to parse its contents.
    with open(filepath) as f:
        dataJ = json.load(f) 
    # - Log an INFO message naming the file that was loaded.
        logger.info("Loaded JSON file: %s", filepath)
    # - Return the parsed object.
        return dataJ 


def load_yaml(filepath):
    """Load a YAML file into a Python object.
    filepath is a Path object.
    """
    # TODO:
    # - Same `with open(filepath) as f:` pattern as load_json.
    # - Use yaml.safe_load(f) instead of json.load(f).
    #   Why "safe" load specifically? Because yaml.load() (without "safe")
    #   can execute arbitrary Python objects embedded in the file — safe_load
    #   restricts parsing to plain data (dicts, lists, strings, numbers).
    with open(filepath) as f:
        dataY = yaml.safe_load(f)
    # - Log an INFO message naming the file that was loaded.
        logger.info("Loaded YAML file: %s", filepath)

    # - Return the parsed object.
    return dataY


def load_data(filepath):
    """Load a file based on its extension.
    filepath is a string, such as 'fixtures/sample.csv'
    """
    # TODO:
    # - Convert filepath (a string) into a Path object: Path(filepath)
    file_path = Path(filepath)
    # - Get its extension in lowercase: path.suffix.lower()
    extension = file_path.suffix.lower()
    #   (.suffix includes the dot, e.g. ".csv" — and .lower() means
    #   ".CSV" still matches your comparisons below)
    #
    if extension == ".csv":
        return load_csv(file_path)
    elif extension == ".json":
        return load_json(file_path)
    elif extension == ".yaml":
        return load_yaml(file_path)
    else:
        logger.error("Unsupported file format: %s", extension)
        raise ValueError(f"Unsupported file format: {extension}")
    # - If the extension is ".csv": call load_csv(path) and return its result.
    # - If the extension is ".json": call load_json(path) and return its result.
    # - If the extension is ".yaml": call load_yaml(path) and return its result.
    #   IMPORTANT: pass `path` (the Path object you built), not the original
    #   `filepath` string, to whichever loader you call.
    #
    # - If the extension matches none of those:
    #     - Log an ERROR message naming the unsupported extension.
    #     - raise ValueError(...) with a message naming the extension too.
    #   Why both log AND raise? The log is for visibility in the terminal
    #   output; the raise is what actually stops execution and gets caught
    #   by whoever called load_data() (that'll be pipeline.py).
