import logging 
import pandas as pd

logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):

    rows_before_vld = len(df)

    for item in required_columns:
        if item not in df.columns:
            logger.error("Missing required column: %s",  item)
            raise ValueError(f"Missing required column: {item}")
        
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    invalid_rows.append(i)
        if invalid_rows:
            logger.warning("Removed %d rows with invalid numeric values in %s", len(invalid_rows), col)
            df = df.drop(index=invalid_rows)

        df[col] = pd.to_numeric(df[col])

    logger.debug("Validation: %d -> %d rows", rows_before_vld, len(df))

    return df