import subprocess
import argparse

parser = argparse.ArgumentParser(description = "Download genome data via the NCBI datasets")

parser.add_argument("file", help = "Path to the .txt file containing the organism names")

args = parser.parse_args()


def download(input_file: str) -> None:
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()

            command = f"datasets download genome --reference taxon \"{line}\" --filename \"{line}.zip\""
            print(command)

            subprocess.call(command, shell = True)


def main():
    file_name = args.file
    download(file_name)


if __name__ == '__main__':
    main()

