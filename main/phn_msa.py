import os
import subprocess
import argparse
from main import set_path

# Initialize argument parser
parser = argparse.ArgumentParser(description='Run MSA on the specified folder.')
parser.add_argument('--folder', type=str, help='The folder to run MSA on. Leave empty to run on all family folders.')

# Parse arguments
args = parser.parse_args()

# Base path to data folder
data_base_path = set_path()
user_email = "rasmus3141@gmail.com"
kalign_path = os.path.join(os.path.split(data_base_path)[0], "main")


def run_msa(input_file_path, output_file_path):
    # Execute Kalign using subprocess
    try:
        subprocess.run(
            [
                "python3",
                os.path.join(kalign_path, 'kalign.py'),
                "--email",
                user_email,
                "--stype",
                "dna",
                "--format",
                "fasta",
                "--outfile",
                output_file_path,
                input_file_path,
            ],
            check=True
        )
        print(f"Successfully completed MSA for {os.path.split(input_file_path)[1]}")
    except Exception as e:
        print(f"Failed to run MSA for {os.path.split(input_file_path)[1]}: {e}")


# Check if a specific folder was specified
if args.folder:
    # Ensure that the folder exists
    if not os.path.exists(args.folder):
        print("The specified folder {args.folder} does not exist.")
    else:
        files = [file for file in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, file))]

        # Run MSA on each file inside the folder
        for file in files:
            input_file_path = os.path.join(args.folder, file)
            output_file_path = os.path.join(args.folder, f"msa_output_{file}")
            run_msa(input_file_path, output_file_path)
else:
    # Loop through each gene family folder
    for gene_family in range(ord("C"), ord("P") + 1):
        # Convert ASCII to char ('phnC', 'phnD', ..., 'phnP')
        gene_family_name = "phn" + chr(gene_family)
        gene_folder_path = os.path.join(data_base_path, f"{gene_family}_genes")
        # Assume each folder contain a single gene.fna file
        input_file_path = os.path.join(gene_folder_path, "gene.fna")
        output_file_path = os.path.join(gene_folder_path, f"msa_output_{gene_family_name}.fna")
        run_msa(input_file_path, output_file_path)

print("MSA process completed.")
