from Bio import Entrez
from tqdm import tqdm

Entrez.email = "201700273@post.au.dk"


def search_fetch(path: str, genes: list[str]) -> None:

    BATCH_SIZE = 50

    for gene in tqdm(genes):
        search_handle = Entrez.esearch(
            db="gene",
            term=f"({gene}[All Fields]) AND Bacteria[Filter] AND alive[prop]",  # alive[prop] excludes discontinued and replaced items
            usehistory="y",
            idtype="acc",
        )
        search_results = Entrez.read(search_handle)
        search_handle.close()

        count = int(search_results["Count"])

        webenv = search_results["WebEnv"]
        query_key = search_results["QueryKey"]

        out_handle = open(f"{path}/{gene}.txt", "w")

        for start in range(0, count, BATCH_SIZE):
            end = min(count, start + BATCH_SIZE)
            print(
                f"Downloading record {int(start + 1)} to {int(end)} of {count} for {gene}"
            )
            fetch_handle = Entrez.efetch(
                db="gene",
                rettype="fasta",
                retmode="text",
                retstart=start,
                retmax=BATCH_SIZE,
                webenv=webenv,
                query_key=query_key,
                idtype="acc",
            )
            data = fetch_handle.read()
            fetch_handle.close()
            out_handle.write(data)
        out_handle.close()

    return