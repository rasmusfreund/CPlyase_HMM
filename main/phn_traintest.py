from Bio import SeqIO
import random
from main import set_path
import os


data_base_path = set_path()


def split_fasta_file(input_fasta_path, train_fasta_path, test_fasta_path, train_ratio=0.8):

    # Create train/test directories if they don't exist
    if not os.path.exists(os.path.join(data_base_path, train_fasta_path)):
        os.makedirs(os.path.join(data_base_path, train_fasta_path))
    if not os.path.exists(os.path.join(data_base_path, test_fasta_path)):
        os.makedirs(os.path.join(data_base_path, test_fasta_path))

    # Parse input sequences and shuffle
    sequences = list(SeqIO.parse(input_fasta_path, "fasta"))
    random.shuffle(sequences)

    num_train = int(len(sequences) * train_ratio)
    train_sequences = sequences[:num_train]
    test_sequences = sequences[num_train:]

    # Save into train and test files
    SeqIO.write(train_sequences, train_fasta_path, "fasta")
    SeqIO.write(test_sequences, test_fasta_path, "fasta")

    return None
# Usage example
# split_fasta_file("path/to/original/fasta/file", "path/to/train.fasta", "path/to/test.fasta")


def main():
    for gene_family in range(ord("C"), ord("P") + 1):
        gene_family = "phn" + chr(
            gene_family
        )  # Convert ASCII to char ('phnC', 'phnD', ..., 'phnP')
        gene_folder_path = os.path.join(data_base_path, f"{gene_family}_genes")


