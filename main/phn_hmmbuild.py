import os
import subprocess
import argparse
import re
from main import set_path

# Create phmms directory if it doesn't exist
data_path = set_path()
phmms_dir = os.path.join(data_path, 'phmms')
if not os.path.exists(phmms_dir):
    os.makedirs(phmms_dir)


def final_models():
    # Loop through each gene family folder
    for gene_family in range(ord('C'), ord('P') + 1):
        gene_family = 'phn' + chr(gene_family)  # Convert ASCII to char ('phnC', 'phnD', ..., 'phnP')
        gene_folder_path = os.path.join(data_path, f"{gene_family}_genes")

        # Input MSA file and output HMM file paths
        input_msa_file = os.path.join(gene_folder_path, f"msa_output_{gene_family}.fna.aln-fasta.FASTA")
        output_hmm_file = os.path.join(phmms_dir, f"{gene_family}.hmm")

        # Execute hmmbuild using subprocess
        try:
            subprocess.run(['hmmbuild', output_hmm_file, input_msa_file])
            print(f"Successfully built HMM profile for {gene_family}")
        except Exception as e:
            print(f"Failed to build HMM profile for {gene_family}: {e}")

    print("HMM profile creation process completed.")

    return None


def individual_models(file_path):
    find_gene_family = re.search("phn[C-P]", os.path.split(file_path)[1])
    gene_family = find_gene_family.group(0)

    output_hmm_file = os.path.join(phmms_dir, f"{gene_family}_train.hmm")

    # Execute hmmbuild using subprocess
    try:
        subprocess.run(['hmmbuild', output_hmm_file, file_path])
        print(f"Successfully built HMM profile for {gene_family}")
    except Exception as e:
        print(f"Failed to build HMM profile for {gene_family}: {e}")

    return None


parser = argparse.ArgumentParser(description="Run an MSA through HMMER to build a pHMM of the given sequences")
parser.add_argument("--train", action='store_true')

args = parser.parse_args()


def main():
    if args.train:
        train_path = os.path.join(data_path, "train")
        if not os.path.exists(train_path):
            print(f"Couldn't find train folder in {data_path}")
            return None

        files_in_train_path = os.listdir(train_path)
        msa_files = [file for file in files_in_train_path if "fna.aln-fasta" in file]
        for msa_file in msa_files:
            individual_models(os.path.join(train_path, msa_file))

    else:
        final_models()


if __name__ == "__main__":
    main()
