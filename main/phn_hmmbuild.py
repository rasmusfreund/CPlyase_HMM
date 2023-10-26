import os
import subprocess
from main import set_path

# Create phmms directory if it doesn't exist
data_path = set_path()
phmms_dir = os.path.join(data_path, 'phmms')
if not os.path.exists(phmms_dir):
    os.makedirs(phmms_dir)

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