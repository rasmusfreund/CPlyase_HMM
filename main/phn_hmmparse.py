import subprocess
import os
import argparse
from main import set_path


def run_hmmer(hmm_model, fasta_file, output_file):
    cmd = f"hmmscan --tblout {output_file} {hmm_model} {fasta_file}"
    subprocess.run(cmd, shell=True)


def hmm_press(hmm_model):
    cmd = f"hmmpress {hmm_model}"
    subprocess.run(cmd, shell=True)


def is_hmm_pressed(hmm_model):
    # Check for the existence of .h3m, .h3i, .h3f, and .h3p files
    extensions = ['.h3m', '.h3i', '.h3f', '.h3p']
    return all(os.path.exists(hmm_model + ext) for ext in extensions)


def validation(data_path, press_hmm=False):
    hmm_path = os.path.join(data_path, "phmms")
    test_path = os.path.join(data_path, "test")
    gene_families = [f"phn{chr(family)}" for family in range(ord("C"), ord("P") + 1)]

    if not os.path.exists(os.path.join(data_path, "validation")):
        os.mkdir(os.path.join(data_path, "validation"))

    output_path = os.path.join(data_path, "validation")

    for family in gene_families:
        hmm_model = os.path.join(hmm_path, f"{family}_train.hmm")
        if not is_hmm_pressed(hmm_model):
            if press_hmm:
                hmm_press(hmm_model)
            else:
                print(f"Error: HMM file {hmm_model} not pressed. Run with --press to process HMM files.")
                return

        fasta_file = os.path.join(test_path, f"{family}_test.fna")
        output_file = os.path.join(output_path, f"{family}_hmmer_output.out")
        run_hmmer(hmm_model, fasta_file, output_file)


def main():
    parser = argparse.ArgumentParser(description="HMMER Validation and Processing Script")
    parser.add_argument('--validation', action='store_true', help='Run validation')
    parser.add_argument('--press', action='store_true', help='Press HMM files with hmmpress')
    args = parser.parse_args()

    if args.validation or args.press:
        data_path = set_path()
        validation(data_path, press_hmm=args.press)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
