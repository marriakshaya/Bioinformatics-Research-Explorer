
import requests
import xml.etree.ElementTree as ET

NCBI_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def search_pubmed(gene_symbol, max_results=10):
    """Search PubMed for articles related to a gene symbol."""

    params = {
        "db": "pubmed",
        "term": f'"{gene_symbol}"[Title/Abstract]',
        "retmax": max_results,
        "sort": "relevance",
        "retmode": "json"
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
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }

    response = requests.get(
        NCBI_URL + "efetch.fcgi",
        params=fetch_params,
        timeout=30
    )
    response.raise_for_status()

    root = ET.fromstring(response.text)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        title_element = article.find(".//ArticleTitle")

        title = (
            "".join(title_element.itertext())
            if title_element is not None
            else "Title unavailable"
        )

        abstract_parts = article.findall(
            ".//Abstract/AbstractText"
        )
        abstract = " ".join(
            "".join(part.itertext())
            for part in abstract_parts
        )

        authors = []

        for author in article.findall(
            ".//AuthorList/Author"
        ):
            last = author.findtext("LastName", "")
            first = author.findtext("ForeName", "")
            collective = author.findtext("CollectiveName", "")

            name = collective or " ".join(
                value for value in [first, last] if value
            )

            if name:
                authors.append(name)

        year = article.findtext(
            ".//JournalIssue/PubDate/Year",
            "Year unavailable"
        )

        pmid = article.findtext(".//PMID", "")

        articles.append({
            "pmid": pmid,
            "title": title,
            "authors": ", ".join(authors) or "Authors unavailable",
            "year": year,
            "abstract": abstract or "Abstract unavailable",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })

    return articles