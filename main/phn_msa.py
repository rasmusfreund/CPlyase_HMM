import os
import subprocess
from main import set_path

# Base path to data folder
data_base_path = set_path()
user_email = "rasmus3141@gmail.com"
kalign_path = os.path.join(os.path.split(data_base_path)[0], "main")


# Loop through each gene family folder
for gene_family in range(ord("C"), ord("P") + 1):
    gene_family = "phn" + chr(
        gene_family
    )  # Convert ASCII to char ('phnC', 'phnD', ..., 'phnP')
    gene_folder_path = os.path.join(data_base_path, f"{gene_family}_genes")

    # Input and output file paths
    input_file_path = os.path.join(gene_folder_path, "gene.fna")
    output_file_path = os.path.join(gene_folder_path, f"msa_output_{gene_family}.fna")

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
            ]
        )
        print(f"Successfully completed MSA for {gene_family}")
    except Exception as e:
        print(f"Failed to run MSA for {gene_family}: {e}")

print("MSA process completed.")
