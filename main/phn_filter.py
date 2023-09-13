import re


def filter_ids(path: str, genes: dict[str], ids: list[str]) -> None:
    symbols = [i.strip(".txt") for i in ids]

    for i in range(len(symbols)):
        keywords = set(genes[symbols[i]])
        match symbols[i]:
            case "phnJ":
                no_ids = 0
                with open(f"{path}/{ids[i]}", "r") as f:
                    lines = f.readlines()
                    with open(f"{path}/{symbols[i]}_IDs.txt", "w") as out:
                        for idx in range(len(lines)):
                            if re.search("^\d+\.", lines[idx]):
                                _desc = set(lines[idx + 1].split("[")[0].split(" "))
                                if _desc.intersection(keywords) == keywords:
                                    _organism = re.search("\[.+\]", lines[idx + 1])
                                    for j in range(1, 5):
                                        if re.search("^ID:", lines[idx + j]):
                                            out.write(_organism.group(0) + "\n")
                                            out.write(
                                                "\t" + lines[idx + j].strip("ID: ")
                                            )
                                            no_ids += 1
                            continue
                    print(f"Wrote {no_ids} IDs to file {symbols[i]}_IDs.txt")
                    out.close()
                f.close()

            case _:
                no_ids = 0
                with open(f"{path}/{ids[i]}", "r") as f:
                    lines = f.readlines()
                    with open(f"{path}/{symbols[i]}_IDs.txt", "w") as out:
                        for idx in range(len(lines)):
                            if re.search("^\d+\.", lines[idx]):
                                _desc = lines[idx + 1]
                                key_check = [i for i in keywords if i in _desc]
                                if key_check:
                                    _organism = re.search("\[.+\]", lines[idx + 1])
                                    for j in range(1, 5):
                                        if re.search("^ID:", lines[idx + j]):
                                            out.write(_organism.group(0) + "\n")
                                            out.write(
                                                "\t" + lines[idx + j].strip("ID: ")
                                            )
                                            no_ids += 1
                            continue
                    print(f"Wrote {no_ids} IDs to file {symbols[i]}_IDs.txt")
                    out.close()
                f.close()
