import argparse
import csv

from parser.filewalker import get_filepaths
from parser.parser import FileParserCSV, FileParserText, FileParserPipe


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Folder containing corpus files.",
                        type=str, required=True)
    parser.add_argument("--output",
                        help="Folder to store the generated statistics in.",
                        type=str, required=True)
    parser.add_argument("--filter",
                        help="Filenames must contain this.",
                        type=str, required=False, default='.txt')
    parser.add_argument("--format",
                        help="Format of the used corpus.",
                        choices=['text', 'pipe', 'csv'],
                        required=True)

    args = parser.parse_args()

    rows = []
    max_numer_of_hashtags = 0
    for data_file in get_filepaths(args.input, args.filter):
        file_title = data_file[data_file.rfind('/') + 1:]

        print("{}...".format(file_title))

        fp = {
            'text': FileParserText,
            'pipe': FileParserPipe,
            'csv': FileParserCSV
         }[args.format](data_file)

        stats = fp.get_data_as_dict()
        stats["Filename"] = file_title
        rows.append(stats)

        max_numer_of_hashtags = max(
            max_numer_of_hashtags,
            len([x for x in stats.keys() if x.startswith('#')])
        )

        with open("{}stats_{}".format(args.output, file_title), 'w') as f:
            f.write(str(fp))

    # Make CSV
    with open("{}summary.csv".format(args.output), 'w') as csvfile:
        fieldnames = [
            "Filename",
            "Number Of Tweets",
            "Absolute Number Of Hashtags",
            "Number Of Hashtags",
            "Tweets with Hashtag",
            "Most Common Hashtag",
            "Most Common Hashtag Count"
        ]

        for i in range(1, max_numer_of_hashtags + 1):
            fieldnames.append("#_{}".format(i))

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='0')
        writer.writeheader()
        for row in sorted(rows, key=lambda x: x['Filename']):
            writer.writerow(row)

    print("Done.")

if __name__ == '__main__':
    run()