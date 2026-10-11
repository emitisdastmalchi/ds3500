# MP1 Data Pipeline

This data pipeline takes in a messy csv file and turns it into a cleaned file with one command.
It's run from the command line with a file that it takes in, an output path, and a yaml config file that controls which columns are checked.
In terms of organization, `data_loaders.py` opens the input and config files, and chooses the correct loader based on the file type. Then, `data_validator.py` checks that all required columns exist and removes rows with non-numeric values in columns that should be numeric. Then, `data_processor.py` cleans the data by removing duplicate rows, rows with missing values, and outliers, using the iqr or z-score method set in the config. Lastly, `data_output.py` saves the cleaned data in a csv, creates the folder if it doesn't exist, and the pipeline prints a cleaning report. 
`pipeline.py` structures all of the steps in order, while `utils.py` sets up the logging and verifies that the files exist.


## Example
``` 
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

```

## Output:

```
17:15:54 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
17:15:54 INFO     src.utils — input file validated: fixtures/sample_data.csv
17:15:54 INFO     src.utils — input file validated: config/config.yaml
17:15:54 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
17:15:54 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
17:15:54 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
17:15:54 DEBUG    src.data_validator — Validation: 100 -> 98 rows
17:15:54 INFO     __main__ — Validation complete: 100 -> 98 rows
17:15:54 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
17:15:54 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
17:15:54 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
17:15:54 INFO     __main__ — Processing complete: 98 -> 92 rows
17:15:54 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
17:15:54 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0} 

```

