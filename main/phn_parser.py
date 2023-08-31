import argparse

parser = argparse.ArgumentParser(
    "Parses text-files containing data acquired from the NCBI gene database and returns objects that contains genome and genome positions."
)

parser.add_argument("-f", "--file",
                    help = "File should be in .txt format")

args = parser.parse_args()

gene_file = open(args.file, 'r')

class Genes:
    """
    Genes class for parsing NCBI gene database output
    """

    def __init__(self, file):
        self.in_file = gene_file.read()


print(Genes)