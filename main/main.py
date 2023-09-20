import os
import re
import entrez
import phn_filter
import phn_parser
from tqdm import tqdm


GENES = {
    "phnC": ["ABC transporter"],
    "phnD": ["ABC transporter"],
    "phnE": ["ABC transporter"],
    "phnF": ["regulator"],
    "phnG": ["C-P lyase system"],
    "phnH": ["C-P lyase system"],
    "phnI": ["carbon-phosphorus"],
    "phnJ": [
        "alpha-D-ribose",
        "1-methylphosphonate",
        "5-phosphate",
        "C-P-lyase",
    ],  # All required
    "phnK": ["C-P-lyase system", "ATP-binding", "ABC transporter"],  # Either required
    "phnL": ["C-P lyase system", "ABC transporter"],  # Either required
    "phnM": ["diphosphatase", "diphosphohydrolase"],  # Either required
    "phnN": ["phosphokinase"],
    "phnO": ["N-acetyltransferase"],
    "phnP": ["phosphonate metabolism", "phosphodiesterase"],  # Either required
}


def set_path() -> str:
    path = os.path.split(os.getcwd())
    data_path = ""

    if path[1] == "CPlyase_HMM":
        # If current dir is CPlyase_HMM, then append "data"
        data_path = os.path.join(path[0], path[1], "data")
    else:
        # If current dir is main, then exchange with "data"
        data_path = os.path.join(path[0], "data")
    return data_path


def check_existing_entrez() -> str and list[str | None]:
    data_path = set_path()

    # Get existing data
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

    return data_path, missing_data


def check_existing_id() -> list[str | None]:
    data_path = set_path()

    # Get existing files in the directory
    file_list = os.listdir(data_path)

    # Split the file_list into two lists
    entrez_files = []
    id_files = []

    for i in file_list:
        if "IDs" not in i:
            entrez_files.append(i)
        else:
            id_files.append(i)

    # Check if each gene is in both lists
    # If gene is not in both lists, store the name of the gene
    id_present = False
    missing_ids = []
    for i in entrez_files:
        gene_name = i.strip(".txt")
        for j in id_files:
            if gene_name in j:
                id_present = True
        if not id_present:
            missing_ids.append(i)
        id_present = False

    return missing_ids


def download_data(path, genes) -> None:
    # Download missing data
    print("Downloading data for:", ", ".join(genes))
    entrez.search_fetch(path, genes)
    return


def filter_gene_ids(path, genes, missing_ids) -> None:
    phn_filter.filter_ids(path, genes, missing_ids)
    return


def extract_ids(files: list) -> None:
    data_path = set_path()
    for i in range(len(files)):
        phn_parser.parser(os.path.join(data_path, files[i]))


def main() -> None:
    print("Checking for existing data:")
    path, genes = tqdm(check_existing_entrez())
    if genes:
        download_data(path, genes)

    ids = check_existing_id()
    if ids:
        print("Filtering genes and writing ID files")
        filter_gene_ids(path, GENES, ids)

    id_files = [i for i in os.listdir(set_path()) if "IDs" in i]
    extract_ids(id_files)


if __name__ == "__main__":
    main()
