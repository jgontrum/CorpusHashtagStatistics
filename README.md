# CorpusHashtagStatistics
Generates statistics for the hashtag usage in text corpus.

## Preparations
- Install Python 3.5
- Install virtualenv

## Usage
```
usage: main.py [-h] --input INPUT --output OUTPUT [--filter FILTER] --format
               {text,pipe,csv}

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Folder containing corpus files.
  --output OUTPUT       Folder to store the generated statistics in.
  --filter FILTER       Filenames must contain this.
  --format {text,pipe,csv}
                        Format of the used corpus.
```
