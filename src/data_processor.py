import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows"""
    rows_before = len(df) 
    df = df.drop_duplicates()
    logger.debug("remove_duplicates: %d -> %d rows", rows_before, len(df))
    return df

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        rows_before = len(df)
        df = df.dropna()
        logger.debug("handle_missing: %d -> %d rows", rows_before, len(df))
    elif axis == "columns":
        cols_before = len(df.columns)
        df = df.dropna(axis=1)
        logger.debug("handle_missing: %d -> %d columns", cols_before, len(df.columns))
    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")
    return df

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column not found: %s", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column is not numeric: %s", col)
            continue

        rows_before = len(df) 

        if method == "iqr":
            q1 = df[col].quantile(.25)
            q3 = df[col].quantile(.75)
            iqr = q3 - q1 
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            df = df[df[col].between(lower, upper)]
        else:
            z = (df[col] - df[col].mean()) / df[col].std()
            df = df[z.abs() <= threshold]

        removed = rows_before - len(df)
        logger.debug("%s: method=%s, threshold=%s, removed=%d", col, method, threshold, removed)

    return df

def process_data(df, config):
    """Apply the processing steps enabled in the configuration"""
    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    if settings["missing"]["enabled"]:
        df = handle_missing(df, settings["missing"]["axis"])

    if settings["outliers"]["enabled"]:
        outliers = settings["outliers"]
        df = remove_outliers(df, outliers["columns"], outliers["method"], outliers["threshold"])

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) -len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }