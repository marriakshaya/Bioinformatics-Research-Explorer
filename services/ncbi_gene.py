
import requests

NCBI_URL = (
    "https://eutils.ncbi.nlm.nih.gov/"
    "entrez/eutils/"
)

ORGANISMS = {
    "Homo sapiens": "9606",
    "Mus musculus": "10090",
    "Escherichia coli": "562"
}


def search_gene(gene_symbol, organism="Homo sapiens"):
    tax_id = ORGANISMS[organism]

    params = {
        "db": "gene",
        "term": (
            f'"{gene_symbol}"[Gene Name] '
            f"AND {tax_id}[Taxonomy ID]"
        ),
        "retmode": "json",
        "retmax": 5
    }

    response = requests.get(
        NCBI_URL + "esearch.fcgi",
        params=params,
        timeout=20
    )
    response.raise_for_status()

    ids = response.json()["esearchresult"]["idlist"]

    return ids[0] if ids else None


def get_gene_summary(gene_id):
    params = {
        "db": "gene",
        "id": gene_id,
        "retmode": "json"
    }

    response = requests.get(
        NCBI_URL + "esummary.fcgi",
        params=params,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()["result"]

    return data.get(gene_id)