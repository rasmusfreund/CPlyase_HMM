from Bio import SeqIO
import random
from main import set_path
import os
from sklearn.model_selection import train_test_split
from copy import deepcopy


# Set a random seed for reproducibility
random.seed(42)


def read_sequences(file_path):
    # Read sequences from a .fna file and return them
    sequences = list(SeqIO.parse(file_path, "fasta"))
    return sequences


def write_sequences(file_path, sequences):
    # Write sequences to a .fna file
    SeqIO.write(sequences, file_path, "fasta")
    return None


# Function to label sequences as negative if they aren't already
def label_as_negative(sequences):
    labeled_sequences = []
    for seq in sequences:
        # Make a deep copy of the sequence to ensure the original is not altered
        seq_copy = deepcopy(seq)
        if seq_copy.id not in sequence_labels:
            # Label sequence as negative if it's not in the dictionary
            seq_copy.id += "_NEG"
            sequence_labels[seq_copy.id] = 'negative'
        labeled_sequences.append(seq_copy)
    return labeled_sequences


# Define data directories
data_dir = set_path()
phmm_dir = os.path.join(data_dir, "phmms")


# Create train/test directories if they don't exist
if not os.path.exists(os.path.join(data_dir, "train")):
    os.makedirs(os.path.join(data_dir, "train"))
if not os.path.exists(os.path.join(data_dir, "test")):
    os.makedirs(os.path.join(data_dir, "test"))


# Train / test directories
train_dir = os.path.join(data_dir, "train")
test_dir = os.path.join(data_dir, "test")

# List for all gene family directories
gene_families = []

# Dictionary to hold all sequences
all_sequences = {}

# Dictionary to track labeling of sequences
sequence_labels = {}

# Read in all sequences for each gene family
for gene_family in range(ord("C"), ord("P") + 1):
    gene_family_name = "phn" + chr(gene_family)  # Convert ASCII to char ('phnC', 'phnD', ..., 'phnP')
    gene_folder_path = os.path.join(data_dir, f"{gene_family_name}_genes")
    gene_file_path = os.path.join(gene_folder_path, "gene.fna")
    gene_families.append(gene_family_name)  # Storing the gene family name
    all_sequences[gene_family_name] = read_sequences(gene_file_path)  # Reading from the .fna file
    print(f"Sequences for {gene_family_name} have been read")

# Iterate over each gene family for train-test splitting
for family in gene_families:
    # Split the positive samples
    pos_train, pos_test = train_test_split(all_sequences[family], test_size=0.2, random_state=42)

    # Create a pool of negative samples from other families
    negative_samples = []
    for other_family in gene_families:
        if other_family != family:
            # Check if there are enough sequences to sample from
            if len(all_sequences[other_family]) >= 15:
                neg_samples = random.sample(all_sequences[other_family], 15)  # Sample 15 sequences
            else:
                # If not enough sequences, either skip or take all
                neg_samples = all_sequences[other_family]  # Take all if less than 15

            # Append a suffix to the ID of negative samples for later identification
            neg_samples = label_as_negative(neg_samples)

            negative_samples.extend(neg_samples)

    # Combine positive and negative samples for testing
    test_set = pos_test + negative_samples
    random.shuffle(test_set)  # Shuffle to avoid any ordering bias

    # Write train and test sets to file
    train_file_path = os.path.join(train_dir, f"{family}_train.fna")
    test_file_path = os.path.join(test_dir, f"{family}_test.fna")

    print(f"Writing training set for {family} to {os.path.split(train_dir)[1]} directory")
    write_sequences(train_file_path, pos_train)
    print(f"Writing test set for {family} to {os.path.split(test_dir)[1]} directory with true negatives marked")
    write_sequences(test_file_path, test_set)

    # Pipeline:
    # 1. Generate the MSA for the training set. Done
    # 2. Build the HMM model from the MSA. Done
    # 3. Validate the HMM model using the test set.
    # 4. Save the HMM model with an appropriate naming convention in phmm_dir.
