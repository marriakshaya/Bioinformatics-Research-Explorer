
import requests
from Bio import SeqIO
from io import StringIO

NCBI_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
)


def get_gene_proteins(gene_id):
    """Retrieve protein records linked to an NCBI Gene ID."""

    params = {
        "db": "protein",
        "term": f"{gene_id}[GeneID]",
        "retmode": "json",
        "retmax": 5
    }

    response = requests.get(
        NCBI_URL + "esearch.fcgi",
        params=params,
        timeout=30
    )
    response.raise_for_status()

    protein_ids = response.json()["esearchresult"]["idlist"]

    if not protein_ids:
        return []

    fetch_params = {
        "db": "protein",
        "id": ",".join(protein_ids),
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