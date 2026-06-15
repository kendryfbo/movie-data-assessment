# Movie Data Processor

This is a simple Python project to parse, filter, and sort movie data.

## How it works
The project splits the work into two clear steps:
1. **Data Parsing:** It takes a raw list of lists and converts it into a clean list of `Movie` objects. If any row has corrupt data or an invalid rating, it logs the error and skips it so the app doesn't crash.
2. **Filtering and Sorting:** It filters movies by whether they are "certified fresh" and sorts them by rating (highest first). If two movies have the same rating, it breaks the tie alphabetically by title.

I used Python dataclasses with `frozen=True` and `slots=True` to keep the data immutable and fast.

## Requirements
- Python 3.10+
- `pytest` (only needed to run the tests)

## How to Run

To run the script and see the sample output:
```bash
python main.py