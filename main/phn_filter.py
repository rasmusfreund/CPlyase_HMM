import re
import os

def filter(path: str, genes: dict[str], ids: list[str]) -> None:

    ids = [i.strip(".txt") for i in ids]

    filter_id_keys = []
    filter_id_vals = []



    files = os.listdir(path)
