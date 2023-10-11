from main import set_path
import re
import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description="Download gene data via the NCBI datasets")

parser.add_argument(
    "-p",
    "--protein",
    action="store_true",
    help="Include protein sequences in download file",
)

args = parser.parse_args()

GENE_DIRS = [
    "phnC_genes",
    "phnD_genes",
    "phnE_genes",
    "phnF_genes",
    "phnG_genes",
    "phnH_genes",
    "phnI_genes",
    "phnJ_genes",
    "phnK_genes",
    "phnL_genes",
    "phnM_genes",
    "phnN_genes",
    "phnO_genes",
    "phnP_genes",
]


def directories():
    """
    Checks to see if relevant directories exist; if not, creates them
    """

    data_path = set_path()
    for folder in GENE_DIRS:
        exists = False
        if folder in os.listdir(data_path):
            exists = True
        if not exists:
            os.mkdir(os.path.join(data_path, folder))


def get_files() -> list[str]:
    data_path = set_path()
    content = os.listdir(data_path)
    pattern = re.findall("phn[C-P]_refseq", ",".join(content))
    gene_list = [f"{element}.txt" for element in pattern]
    return gene_list


def download() -> None:

    data_path = set_path()
    gene_list = get_files()
    for i in range(len(gene_list)):
        dir_path = os.path.join(data_path, GENE_DIRS[i])
        input_file = os.path.join(data_path, gene_list[i])

        # Don't download if the file already exists
        if 'ncbi_dataset.zip' in os.listdir(dir_path):
            print(f"Skipping {gene_list[i]} because the zip-file already exists")
            continue

        os.chdir(dir_path)

        if args.protein:
            command = f'datasets download gene gene-id --inputfile "{input_file}" --include gene,protein'
        else:
            command = (
                f'datasets download gene gene-id --inputfile "{input_file}" --include gene'
            )
        print(command)

        subprocess.call(command, shell=True)


def main():
    directories()
    get_files()
    download()


if __name__ == "__main__":
    main()
