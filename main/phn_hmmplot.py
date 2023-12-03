import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from main import set_path


def parse_hmmer_output(file_path):
    data = list()
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                parts = line.split()
                query_name = parts[2]
                e_value = float(parts[4]) # Full sequence E-value, change to 6 for best domain
                is_negative = '_NEG' in query_name
                data.append({'query': query_name, 'e_value': e_value, 'is_negative': is_negative})
    return pd.DataFrame(data)


def count_fasta_seqs(fasta_file):
    true_negatives = 0
    true_positives = 0
    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                if '_NEG' in line:
                    true_negatives += 1
                else:
                    true_positives += 1
    return true_negatives, true_positives


def compare_length(dataframe, test_file):
    df_true_negatives = len(dataframe[dataframe['is_negative']])
    df_true_positives = len(dataframe[~dataframe['is_negative']])

    fasta_true_negatives, fasta_true_positives = count_fasta_seqs(test_file)

    filtered_negatives = fasta_true_negatives - df_true_negatives
    filtered_positives = fasta_true_positives - df_true_positives

    return filtered_negatives, filtered_positives


def plot_e_values(df, family, filtered_negatives, filtered_positives, output_file = None):
    # Convert E-value to negative log scale
    eps = 1e-200 # Avoiding log(0)
    df['neg_log_e_value'] = -np.log10(df['e_value'] + eps)

    # Max-value true negative
    max_neg = df[df['is_negative']]['neg_log_e_value'].max()
    print(max_neg)

    plt.figure(figsize=(10, 6))

    # Separate data into true positives and true negatives
    true_positives = df[df['is_negative'] == False]
    true_negatives = df[df['is_negative'] == True]

    plt.scatter(range(len(true_positives)),
                true_positives['neg_log_e_value'],
                color='seagreen',
                label='True Positives')

    plt.scatter(range(len(true_negatives)),
                true_negatives['neg_log_e_value'],
                color='steelblue',
                label='True Negatives')

    # Separation line
    plt.axhline(y=max_neg,
                color='red',
                linestyle='--',
                label='Separation Threshold')

    plt.xlabel('Sequence')
    plt.ylabel('-log10(E-value)')
    plt.xticks([])
    plt.title(f'HMMER E-value distribution for {family}\n'
              f'Filtered: {filtered_positives} True Positives | {filtered_negatives} True Negatives')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=3)
    plt.tight_layout()

    if output_file is not None:
        plt.savefig(output_file, format='png', dpi=300)
    #plt.show()

    # Save data to CSV for presentation
    #df[['query', 'neg_log_e_value', 'is_negative']].to_csv(output_csv, index=False)


for gene_family in range(ord('C'), ord('P') + 1):
    hmmer_out_path = os.path.join(set_path(), 'validation')
    hmmer_df = parse_hmmer_output(os.path.join(hmmer_out_path, f'phn{chr(gene_family)}_hmmer_output.out'))

    test_path = os.path.join(set_path(), 'test')
    test_file = os.path.join(test_path, f'phn{chr(gene_family)}_test.fna')

    filtered_negatives, filtered_positives = compare_length(hmmer_df, test_file)
    output_plot_file = os.path.join(hmmer_out_path, f'phn{chr(gene_family)}_plot.png')

    plot_e_values(hmmer_df, os.path.split(test_file)[1][:4], filtered_negatives, filtered_positives, output_plot_file)


#output_csv = os.path.join(hmmer_out_path, 'hmmer_plot_data.csv')
#plot_e_values(hmmer_df, output_csv)
