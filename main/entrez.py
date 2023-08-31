from Bio import Entrez

Entrez.email = "201700273@post.au.dk"

genes = [
    "phnC",
    "phnD",
    "phnE",
    "phnF",
    "phnG",
    "phnH",
    "phnI",
    "phnJ",
    "phnK",
    "phnL",
    "phnM",
    "phnN",
    "phnO",
    "phnP",
]
BATCH_SIZE = 20

for gene in genes:
    search_handle = Entrez.esearch(
        db="gene",
        term=f"({gene}[All Fields]) AND Bacteria[Filter] AND alive[prop]",  # alive[prop] excludes discontinued and replaced items
        usehistory="y",
        idtype="acc",
    )
    search_results = Entrez.read(search_handle)

    acc_list = search_results["IdList"]
    count = int(search_results["Count"])
    webenv = search_results[
        "WebEnv"
    ]  # Cookie received from search; allows us to append searches and thereby download data in smaller batches
    query_key = search_results[
        "QueryKey"
    ]  # Query key is returned from previous search call and assists with appending search results
    search_handle.close()

    out_handle = open(f"{gene}.txt", "w")

    for start in range(0, count, BATCH_SIZE):
        end = min(count, start + BATCH_SIZE)
        print(f"Downloading record {int(start + 1)} to {int(end)} of {count} for {gene}")
        fetch_handle = Entrez.efetch(
            db = "gene",
            rettype = "fasta",
            retmode = "text",
            retmax = BATCH_SIZE,
            webenv = webenv,
            query_key = query_key,
            idtype = "acc"
        )
        data = fetch_handle.read()
        fetch_handle.close()
        out_handle.write(data)
    out_handle.close()