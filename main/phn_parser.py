import argparse
import re

parser = argparse.ArgumentParser(
    "Parses text-files containing data acquired from the NCBI gene database and returns a list of IDs."
)

parser.add_argument(
    "file",
    metavar="F",
    type=argparse.FileType("r"),
    help="File should be in .txt format.",
)

args = parser.parse_args()

gene_file = args.file


def parser(file: str) -> None:
    """
    :param file: File containing data acquired from entrez.py
    :return: Output file with all RefSeq IDs found in the input file.
    """
    id_list = []

    """Isolate name of input file and append '_IDs' to it"""
    new_file_name = gene_file.name.strip(".txt")
    new_file_name += "_IDs.txt"

    """Open file, read each line, locate lines containing
     'ID:' followed by a string of numbers"""

    with open(new_file_name, "w") as f:
        for line in file:
            if re.search("ID: \d+", line):
                id_list.append(line.strip("ID: \n"))

        """Write to output file"""
        f.write("\n".join(id_list))

        print(f"Found {len(id_list)} ID numbers in {gene_file.name}.")
        print(f"IDs written to {new_file_name}")

    f.close()

    return
