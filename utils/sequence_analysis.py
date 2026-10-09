
from Bio.Seq import Seq


def analyze_sequence(sequence):
    sequence = "".join(sequence.split()).upper()

    if not sequence:
        raise ValueError("The sequence is empty.")

    valid_bases = set("ATGCN")
    invalid_bases = set(sequence) - valid_bases

    if invalid_bases:
        raise ValueError(
            f"Invalid DNA characters: {', '.join(sorted(invalid_bases))}"
        )

    length = len(sequence)
    counts = {
        base: sequence.count(base)
        for base in "ATGCN"
    }

    gc_count = counts["G"] + counts["C"]
    at_count = counts["A"] + counts["T"]

    return {
        "length": length,
        "counts": counts,
        "gc_percentage": (
            gc_count / length * 100 if length else 0
        ),
        "at_percentage": (
            at_count / length * 100 if length else 0
        )
    }