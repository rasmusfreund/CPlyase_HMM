"""Probably need some kind of loader for FASTA files"""
import numpy as np


def observed_states(x: str) -> list[int]:
    """
    Map a DNA sequence to HMM emission
    :param x: 'CAGTCGTA'
    :return: [1, 0, 2, 3, 1, 2, 3, 0]
    """
    _map = {"A": 0, "C": 1, "G": 2, "T": 3}
    return [_map[a] for a in x]


def rev_observed_states(obs: list[int]) -> str:
    """
    Reverse the observable state mapping in
    order to decode
    :param obs: [1, 0, 2, 3, 1, 2, 3, 0]
    :return: 'CAGTCGTA'
    """
    return "".join("ACGT"[x] for x in obs)


def hidden_states(
    x: str,
) -> list[int]:  ### Probably 3 states?? Noncode(0), code(1), reverse code??(2)
    """
    Map genome annotation to hidden states
    :param x: 'NCCCCNNRRRN'
    :return: [0, 1, 1, 1, 1, 0, 0, 2, 2, 2, 0]
    """
    _map = {"N": 0, "C": 1, "R": 2}
    return [_map[i] for i in x]


def rev_hidden_states(hidden: list[int]) -> str:
    """
    Reverse the mapping of hidden states
    :param hidden: [0, 1, 1, 1, 1, 0, 0, 2, 2, 2, 0]
    :return: 'NCCCCNNRRRN'
    """
    return "".join("NCR"[i] for i in hidden)
