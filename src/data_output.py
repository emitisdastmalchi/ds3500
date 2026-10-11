import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""
    path = Path(filepath) #turns the text into a path object so u can use libraries; easier to work with

    path.parent.mkdir(parents = True, exist_ok=True) #creates folder if filepath missing

    df.to_csv(path, index=False)
    logger.debug("Saved %d rows to %s", len(df), path)
    
    return path
