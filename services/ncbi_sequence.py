
import requests
from Bio import Entrez, SeqIO
from io import StringIO

NCBI_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def get_gene_sequences(gene_id):
    """Retrieve linked nucleotide records for an NCBI Gene ID."""
    params = {
        "db": "nuccore",
        "term": f"{gene_id}[GeneID] AND biomol_mrna[PROP]",
        "retmode": "json",
        "retmax": 5
    }

    response = requests.get(
        NCBI_URL + "esearch.fcgi",
        params=params,
        timeout=30
    )
    response.raise_for_status()

    ids = response.json()["esearchresult"]["idlist"]

    if not ids:
        return []

    fetch_params = {
        "db": "nuccore",
        "id": ",".join(ids),
        "rettype": "fasta",
        "retmode": "text"
    }

    response = requests.get(
        NCBI_URL + "efetch.fcgi",
        params=fetch_params,
        timeout=30
    )
    response.raise_for_status()

    records = list(
        SeqIO.parse(StringIO(response.text), "fasta")
    )

    return [
        {
            "accession": record.id,
            "description": record.description,
            "sequence": str(record.seq)
        }
        for record in records
    ]