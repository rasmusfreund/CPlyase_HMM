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


def plot_e_values(df):
    # Convert E-value to negative log scale
    df['neg_log_e_value'] = -np.log10(df['e_value'])

    # Mid-point between true negatives and true positives
    max_neg = df[df['is_negative']]['neg_log_e_value'].max()
    min_pos = df[~df['is_negative']]['neg_log_e_value'].min()
    mid_point = (max_neg + min_pos) / 2
    print(mid_point)

    plt.figure(figsize=(10, 6))

    # Separate data into true positives and true negatives
    true_positives = df[df['is_negative'] == False]
    true_negatives = df[df['is_negative'] == True]

    plt.scatter(true_positives['query'],
                true_positives['neg_log_e_value'],
                color='seagreen',
                label='True Positives')

    plt.scatter(true_negatives['query'],
                true_negatives['neg_log_e_value'],
                color='steelblue',
                label='True Negatives')

    # Separation line
    plt.axhline(y=mid_point,
                color='red',
                linestyle='--',
                label='Separation Threshold')

    plt.xlabel('Sequence')
    plt.ylabel('-log10(E-value)')
    plt.xticks(rotation=90)
    plt.title('HMMER E-value distribution')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Save data to CSV for presentation
    #df[['query', 'neg_log_e_value', 'is_negative']].to_csv(output_csv, index=False)


hmmer_out_path = os.path.join(set_path(), 'validation')
hmmer_df = parse_hmmer_output(os.path.join(hmmer_out_path, 'phnC_hmmer_output.out'))
plot_e_values(hmmer_df)
#output_csv = os.path.join(hmmer_out_path, 'hmmer_plot_data.csv')
#plot_e_values(hmmer_df, output_csv)
