import os
import zipfile
import glob
import re
import shutil
from main import set_path, timer_decorator


def get_dirs() -> list[str]:
    gene_dirs = glob.glob(
        "*_genes"
    )  # Get a list of directories that matches the pattern
    return gene_dirs


@timer_decorator
def unzip(dir_names: list[str]) -> None:
    data_path = set_path()  # get the path for the data directory
    for folder in dir_names:
        files = os.listdir(os.path.join(data_path, folder))

        # If a fasta file exists, skip the iteration
        fna_files = re.search("(.+\.fna|.+\.fasta)", " ".join(files))
        if fna_files:
            continue

        os.chdir(os.path.join(data_path, folder))
        # Unzip if no fasta file exists
        with zipfile.ZipFile(files[0], "r") as myzip:
            # Get path to the fasta file
            gene_file = re.search(
                "ncbi_dataset.+gene\.fna", " ".join(zipfile.ZipFile.namelist(myzip))
            )

            # Get path to the current directory
            current_dir = os.path.join(data_path, folder)

            print(f"Unzipping fasta file to {folder}")
            # Open the fasta file, open an empty fasta file in the current directory,
            # copy the content of the zipped fasta file to the empty file
            with myzip.open(gene_file.group(0)) as mygene_file, open(
                os.path.join(current_dir, "gene.fna"), "wb"
            ) as f:
                shutil.copyfileobj(mygene_file, f)


def main():
    os.chdir(set_path())
    gene_dirs = get_dirs()
    unzip(gene_dirs)
    # Reset working directory
    os.chdir(os.path.split(os.getcwd())[0])


if __name__ == "__main__":
    main()
