import os
import re
import entrez
import phn_parser

GENES = [
    "phnC",
    "phnD",
    "phnE",
    "phnF",
    "phnG",
    "phnH",
    "phnI",
    "phnJ",
    "phnK",
    "phnL",
    "phnM",
    "phnN",
    "phnO",
    "phnP",
]


def download_data(path, GENES) -> None:
    entrez.search_fetch(path, GENES)

def parse_ids(filename):
    phn_parser.parser(###)


def main() -> None:

    # Change current directory to "data" in check if data already exists
    path = os.getcwd().split("/")
    path[-1] = "data"
    data_path = "/".join(path)

    # Check for existing data
    data_list = os.listdir(data_path)

    # Search existing data and append gene if it contains "phn"
    data_exists = []
    for obj in data_list:
        if re.search("phn", obj):
            data_exists.append(obj[:4])

    # Check if any genes are missing from currently existing data
    data_exists = set(data_exists)  # Convert to set to remove duplicates
    missing_data = []
    if len(GENES) != len(data_exists):
        for obj in GENES:
            if obj not in data_exists:
                missing_data.append(obj)

    # Download missing data if necessary
    if missing_data:
        print("Missing:", missing_data)
    #    download_data(data_path, missing_data)

    print("Exists:", data_exists)



if __name__ == "__main__":
    main()
