import re

def parser(path: str, file: str) -> None:
    """
    :param file: File containing data acquired from entrez.py
    :return: Output file with all RefSeq IDs found in the input file.
    """
    id_list = []

    """Isolate name of input file and append '_IDs' to it"""
    new_file_name = file.strip(".txt")
    new_file_name += "_IDs.txt"

    """Open file, read each line, locate lines containing
     'ID:' followed by a string of numbers"""
    entrez_file = open(f"{path}/{file}", "r")

    with open(f"{path}/{new_file_name}", "w") as f:
        for line in entrez_file:
            if re.search("ID: \d+", line):
                id_list.append(line.strip("ID: \n"))

        """Write to output file"""
        f.write("\n".join(id_list))

        print(f"Found {len(id_list)} ID numbers in {file}.")
        print(f"IDs written to {new_file_name}")

    f.close()

    return
