import re
import os


def parser(filename: str) -> None:
    organisms = []
    refseq = []
    with open(filename, 'r') as f:
        for line in f:
            _refseq = re.search("^\t\d+", line) # Look for digits in the first place after a tab indentation
            _organism = re.search("\[.+\]", line) # Look for organism names inside "[]"
            if _organism and _organism.group(0).strip("[]") not in organisms:
                organisms.append(_organism.group(0).strip("[]"))
            if _refseq and _refseq.group(0).strip("\t") not in refseq:
                refseq.append(_refseq.group(0).strip("\t"))
    f.close()

    _path = os.path.split(filename)
    _org_path = os.path.join(_path[0], _path[1].split('_')[0] + "_organisms.txt")
    _refseq_path = os.path.join(_path[0], _path[1].split('_')[0] + "_refseq.txt")

    with open(_org_path, 'w') as f:
        for i in range(len(organisms)):
            f.write(organisms[i] + "\n")
    f.close()

    with open(_refseq_path, 'w') as f:
        for i in range(len(refseq)):
            f.write(refseq[i] + "\n")
    f.close()
