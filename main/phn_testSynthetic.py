from Bio import SeqIO
import random
import os
from main import set_path


def generate_synthetic_sequence_with_inserts(input_fasta_path, output_fasta_path, gc_content=0.6, mutation_rate=0.01):
    # Read sequences from input FASTA file
    sequences = list(SeqIO.parse(input_fasta_path, "fasta"))

    # Define nucleotide frequencies based on GC-content
    gc_frequency = gc_content / 2
    at_frequency = (1 - gc_content) / 2
    synthetic_sequences = []

    for seq_record in sequences:
        # Generate a synthetic DNA sequence of length 1000 (change as needed)
        synthetic_sequence = ''.join(
            random.choices(['A', 'C', 'G', 'T'], weights=[at_frequency, gc_frequency, gc_frequency, at_frequency],
                           k=1000))

        # Your test sequence
        test_sequence = str(seq_record.seq)

        # Introduce mutations in the test sequence
        mutated_test_sequence = ""
        for nt in test_sequence:
            if random.random() < mutation_rate:
                mutated_test_sequence += random.choice(['A', 'C', 'G', 'T'])
            else:
                mutated_test_sequence += nt

        # Insert the test (potentially mutated) sequence at a random position in the synthetic sequence
        insert_pos = random.randint(0, len(synthetic_sequence) - len(test_sequence))
        final_sequence = synthetic_sequence[:insert_pos] + mutated_test_sequence + synthetic_sequence[
                                                                                   insert_pos + len(test_sequence):]

        # Create a new SeqRecord and append to list
        new_seq_record = SeqIO.SeqRecord(seq=final_sequence, id=seq_record.id + "_synthetic", description="")
        synthetic_sequences.append(new_seq_record)

    # Write synthetic sequences to output FASTA file
    SeqIO.write(synthetic_sequences, output_fasta_path, "fasta")


# Usage
# generate_synthetic_sequence_with_inserts("path/to/input/fasta/file", "path/to/output/fasta/file")
