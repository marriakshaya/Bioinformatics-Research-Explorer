import requests
import pandas as pd
import streamlit as st

from services.ncbi_gene import search_gene, get_gene_summary
from services.ncbi_sequence import get_gene_sequences
from services.ncbi_protein import get_gene_proteins
from services.pubmed import search_pubmed
from utils.sequence_analysis import analyze_sequence
from utils.report_generator import create_gene_report


st.set_page_config(
    page_title="Bioinformatics Research Explorer",
    page_icon="🧬",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --rose-50: #fff5f7;
            --rose-100: #ffe4ec;
            --rose-200: #fecdd9;
            --rose-500: #e74670;
            --rose-600: #d92d5c;
            --berry: #9f1239;
            --ink: #38212b;
        }

        .stApp {
            background: linear-gradient(135deg, #fff8fa 0%, #fff5f7 48%, #fff0f3 100%);
            color: var(--ink);
        }
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffe3eb 0%, #fff0f4 52%, #fff8fa 100%);
            border-right: 1px solid #f8bfd0;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label {
            color: #70233d;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #9f1239;
        }
        h1, h2, h3 {
            color: #9f1239;
            letter-spacing: -0.45px;
        }
        h1 { font-weight: 800; }
        [data-testid="stCaptionContainer"] { color: #925064; }

        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #ffffff 0%, #fff0f4 100%);
            border: 1px solid #f7bfd0;
            padding: 16px 18px;
            border-radius: 16px;
            box-shadow: 0 5px 18px rgba(190, 24, 93, 0.07);
        }
        div[data-testid="stMetric"] label {
            color: #9f3656 !important;
            font-weight: 600;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #9f1239;
            font-weight: 750;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #f5bfd0 !important;
            border-radius: 18px !important;
            background: rgba(255, 255, 255, 0.76);
        }
        div[data-testid="stTabs"] button[role="tab"] {
            color: #87334f;
            border-radius: 12px 12px 0 0;
            font-weight: 650;
        }
        div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            color: #b51245;
            background: #ffe4ec;
            border-bottom: 3px solid #e74670;
        }

        .stButton > button, .stDownloadButton > button, .stLinkButton > a {
            border-radius: 12px;
            border: 1px solid #e74670;
            font-weight: 650;
            transition: all 0.18s ease-in-out;
        }
        .stButton > button[kind="primary"] {
            color: #ffffff;
            background: linear-gradient(100deg, #e74670 0%, #be185d 100%);
            border: none;
            box-shadow: 0 5px 14px rgba(190, 24, 93, 0.2);
        }
        .stButton > button[kind="primary"]:hover {
            color: #ffffff;
            background: linear-gradient(100deg, #d92d5c 0%, #9f1239 100%);
            border: none;
            transform: translateY(-1px);
        }
        .stDownloadButton > button, .stLinkButton > a {
            color: #a31243;
            background: #fff0f4;
        }
        .stDownloadButton > button:hover, .stLinkButton > a:hover {
            color: #ffffff;
            background: #be185d;
            border-color: #be185d;
        }

        .stTextInput input, .stSelectbox [data-baseweb="select"] > div {
            border-radius: 11px;
            border-color: #efb4c6;
            background: #fffdfd;
        }
        .stTextInput input:focus {
            border-color: #e74670;
            box-shadow: 0 0 0 1px #e74670;
        }
        [data-testid="stExpander"] {
            border: 1px solid #f4c3d1;
            border-radius: 13px;
            background: rgba(255,255,255,0.7);
        }
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid #f4c3d1;
            border-radius: 12px;
            overflow: hidden;
        }
        [data-testid="stAlert"] { border-radius: 12px; }
        hr { border-color: #f3c5d2; }

        .genelens-hero {
            padding: 1.4rem 1.6rem;
            margin-bottom: 0.65rem;
            border: 1px solid #f6c0d0;
            border-radius: 22px;
            background: linear-gradient(115deg, #ffe1ea 0%, #fff2f5 55%, #ffffff 100%);
            box-shadow: 0 8px 26px rgba(190, 24, 93, 0.08);
        }
        .genelens-eyebrow {
            color: #be185d;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.72rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .genelens-hero h1 {
            margin: 0;
            color: #9f1239;
            font-size: clamp(2rem, 4vw, 2.8rem);
            line-height: 1.12;
        }
        .genelens-hero p {
            margin: 0.55rem 0 0;
            color: #7b4053;
            font-size: 1rem;
        }
        @media (max-width: 700px) {
            .block-container { padding-top: 1rem; }
            .genelens-hero { padding: 1.1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div style="padding: 0.4rem 0 0.7rem;">
      <div style="font-size: 2rem;">🧬</div>
      <div style="font-size: 1.35rem; font-weight: 850; color: #9f1239;">Bioinformatics Research Explorer</div>
      <div style="font-size: 0.88rem; color: #925064;">Your gene research workspace</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **🌸 Research tools**
    - 🧬 Gene information
    - 🧪 Nucleotide sequences
    - 🔬 Protein explorer
    - 📚 PubMed literature
    - 📄 Research report
    """
)
st.sidebar.markdown("---")
st.sidebar.caption("Explore genes. Understand sequences. Discover research.")

st.markdown(
    """
    <div class="Bioinformatics Research Explorer-hero">
      <div class="Bioinformatics Research Explorer-eyebrow">Bioinformatics research workspace</div>
      <h1>🧬 Bioinformatics Research Explorer</h1>
      <p>Explore genes, analyze DNA sequences, discover proteins, and browse biomedical literature — all in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Keep the search form outside the tabs so it is always easy to find.
with st.container(border=True):
    st.subheader("Find a gene")
    search_col, organism_col, button_col = st.columns([2, 2, 1])

    with search_col:
        gene_input = st.text_input(
            "Gene symbol",
            placeholder="TP53, BRCA1, EGFR",
            key="gene_input",
        )

    with organism_col:
        organism_input = st.selectbox(
            "Organism",
            ["Homo sapiens", "Mus musculus", "Escherichia coli"],
            key="organism_input",
        )

    with button_col:
        st.write("")
        st.write("")
        search_clicked = st.button(
            "🔍 Explore Gene",
            type="primary",
            use_container_width=True,
        )

if search_clicked:
    if not gene_input.strip():
        st.warning("Please enter a gene symbol.")
    else:
        try:
            with st.spinner("Searching NCBI Gene..."):
                found_gene_id = search_gene(gene_input.strip(), organism_input)

                if not found_gene_id:
                    st.error(
                        "No matching gene was found. Check the gene symbol "
                        "and selected organism."
                    )
                else:
                    found_data = get_gene_summary(found_gene_id)

                    if not found_data:
                        st.error("The gene summary could not be retrieved.")
                    else:
                        # Clear records from the previous gene to avoid mixing results.
                        for key in (
                            "sequence_records",
                            "protein_records",
                            "pubmed_articles",
                        ):
                            st.session_state.pop(key, None)

                        st.session_state["gene_id"] = found_gene_id
                        st.session_state["gene_name"] = gene_input.strip()
                        st.session_state["selected_organism"] = organism_input
                        st.session_state["gene_data"] = found_data
                        st.success("Gene information retrieved from NCBI.")
        except requests.RequestException as exc:
            st.error(f"Could not connect to NCBI: {exc}")

overview_tab, dna_tab, protein_tab, literature_tab, summary_tab = st.tabs(
    [
        "🧬 Gene Overview",
        "🧪 DNA Analysis",
        "🔬 Protein Explorer",
        "📚 Literature",
        "📄 Research Summary",
    ]
)

# TAB 1: GENE OVERVIEW
with overview_tab:
    st.header("Gene Information")

    if "gene_data" not in st.session_state:
        st.info("Enter a gene symbol above and click Explore Gene.")
    else:
        data = st.session_state["gene_data"]
        gene_id = st.session_state["gene_id"]
        gene_name = st.session_state["gene_name"]

        col1, col2, col3 = st.columns(3)
        col1.metric("NCBI Gene ID", gene_id)
        col2.metric("Chromosome", data.get("chromosome", "N/A"))
        col3.metric(
            "Organism",
            data.get("organism", {}).get("scientificname", "N/A"),
        )

        st.subheader(
            data.get("nomenclaturesymbol") or data.get("name") or gene_name
        )
        st.write(data.get("description", "Description unavailable"))

        st.link_button(
            "Open NCBI Gene record",
            f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}",
        )

# TAB 2: NUCLEOTIDE / DNA ANALYSIS
with dna_tab:
    st.header("Nucleotide / mRNA Sequence")

    if "gene_id" not in st.session_state:
        st.info("Search for a gene first.")
    else:
        if st.button("Fetch mRNA Sequences", key="fetch_mrna"):
            try:
                with st.spinner("Retrieving nucleotide records..."):
                    st.session_state["sequence_records"] = get_gene_sequences(
                        st.session_state["gene_id"]
                    )
            except requests.RequestException as exc:
                st.error(f"Could not retrieve nucleotide records: {exc}")

        records = st.session_state.get("sequence_records", [])

        if records:
            selected_index = st.selectbox(
                "Select a nucleotide record",
                options=list(range(len(records))),
                format_func=lambda i: (
                    f"{records[i]['accession']} — "
                    f"{records[i]['description'][:90]}"
                ),
                key="nucleotide_selector",
            )
            selected_record = records[selected_index]
            sequence = selected_record["sequence"]

            col1, col2 = st.columns(2)
            col1.metric("Accession", selected_record["accession"])
            col2.metric("Sequence length", f"{len(sequence):,} bp")

            with st.expander("View nucleotide sequence"):
                st.code(sequence, language=None)

            fasta_text = (
                f">{selected_record['description']}\n"
                + "\n".join(
                    sequence[i:i + 70] for i in range(0, len(sequence), 70)
                )
            )
            st.download_button(
                "Download FASTA sequence",
                data=fasta_text,
                file_name=f"{selected_record['accession']}.fasta",
                mime="text/plain",
                key="download_dna_fasta",
            )

            st.subheader("Sequence Composition")
            try:
                stats = analyze_sequence(sequence)

                metric1, metric2, metric3 = st.columns(3)
                metric1.metric("Sequence length", f"{stats['length']:,} bp")
                metric2.metric("GC content", f"{stats['gc_percentage']:.2f}%")
                metric3.metric("AT content", f"{stats['at_percentage']:.2f}%")

                counts_df = pd.DataFrame(
                    {
                        "Nucleotide": list(stats["counts"].keys()),
                        "Count": list(stats["counts"].values()),
                    }
                )
                st.bar_chart(counts_df.set_index("Nucleotide"))
                st.dataframe(counts_df, use_container_width=True)
            except ValueError as exc:
                st.warning(f"Sequence analysis could not be completed: {exc}")
        elif "sequence_records" in st.session_state:
            st.info(
                "No linked mRNA records were found for this gene. "
                "Some genes may not have an available linked mRNA record."
            )
        else:
            st.caption("Click Fetch mRNA Sequences to retrieve records.")

# TAB 3: PROTEIN EXPLORER
with protein_tab:
    st.header("Protein Sequence Explorer")

    if "gene_id" not in st.session_state:
        st.info("Search for a gene first.")
    else:
        if st.button("Fetch Protein Sequences", key="fetch_proteins"):
            try:
                with st.spinner("Retrieving protein records..."):
                    st.session_state["protein_records"] = get_gene_proteins(
                        st.session_state["gene_id"]
                    )
            except requests.RequestException as exc:
                st.error(f"Could not retrieve protein records: {exc}")

        proteins = st.session_state.get("protein_records", [])

        if proteins:
            protein_index = st.selectbox(
                "Select a protein record",
                options=list(range(len(proteins))),
                format_func=lambda i: (
                    f"{proteins[i]['accession']} — "
                    f"{proteins[i]['description'][:90]}"
                ),
                key="protein_selector",
            )
            protein = proteins[protein_index]
            protein_sequence = protein["sequence"]

            col1, col2 = st.columns(2)
            col1.metric("Protein accession", protein["accession"])
            col2.metric("Protein length", f"{len(protein_sequence):,} aa")
            st.write(f"**Description:** {protein['description']}")

            with st.expander("View amino acid sequence"):
                st.code(protein_sequence, language=None)

            protein_fasta = (
                f">{protein['description']}\n"
                + "\n".join(
                    protein_sequence[i:i + 70]
                    for i in range(0, len(protein_sequence), 70)
                )
            )
            st.download_button(
                "Download protein FASTA",
                data=protein_fasta,
                file_name=f"{protein['accession']}.fasta",
                mime="text/plain",
                key="download_protein_fasta",
            )
        elif "protein_records" in st.session_state:
            st.info("No linked protein records were found for this gene.")
        else:
            st.caption("Click Fetch Protein Sequences to retrieve records.")

# TAB 4: PUBMED LITERATURE
with literature_tab:
    st.header("PubMed Literature Explorer")

    if "gene_name" not in st.session_state:
        st.info("Search for a gene first.")
    else:
        st.write(
            "Search biomedical literature related to "
            f"**{st.session_state['gene_name']}**."
        )
        max_articles = st.selectbox(
            "Number of articles",
            [5, 10, 20],
            index=1,
            key="max_articles",
        )

        if st.button("Search PubMed", key="search_pubmed"):
            try:
                with st.spinner("Searching PubMed..."):
                    st.session_state["pubmed_articles"] = search_pubmed(
                        st.session_state["gene_name"],
                        max_results=max_articles,
                    )
            except requests.RequestException as exc:
                st.error(f"Could not connect to PubMed: {exc}")

        if "pubmed_articles" in st.session_state:
            articles = st.session_state["pubmed_articles"]
            if articles:
                st.success(f"Retrieved {len(articles)} articles.")
                for article in articles:
                    with st.expander(
                        f"{article['title']} ({article['year']})"
                    ):
                        st.write(f"**Authors:** {article['authors']}")
                        st.write(f"**PMID:** {article['pmid']}")
                        st.write(f"**Abstract:** {article['abstract']}")
                        st.link_button(
                            "Read article on PubMed",
                            article["url"],
                            key=f"pubmed_link_{article['pmid']}",
                        )
            else:
                st.info("No articles were found for this search.")

# TAB 5: RESEARCH SUMMARY AND PDF EXPORT
with summary_tab:
    st.header("Gene Research Summary")

    if "gene_data" not in st.session_state:
        st.info("Search for a gene first to generate a report.")
    else:
        data = st.session_state["gene_data"]
        gene_name = st.session_state.get("gene_name", "Unknown")
        gene_id = st.session_state["gene_id"]
        organism_name = data.get("organism", {}).get(
            "scientificname", "Unavailable"
        )
        chromosome = data.get("chromosome", "Unavailable")
        description = data.get("description", "Unavailable")

        st.subheader(f"Research overview: {gene_name}")
        st.markdown("### Gene profile")
        st.write(f"**Gene symbol searched:** {gene_name}")
        st.write(f"**NCBI Gene ID:** {gene_id}")
        st.write(f"**Organism:** {organism_name}")
        st.write(f"**Chromosome:** {chromosome}")
        st.write(f"**Description:** {description}")

        records = st.session_state.get("sequence_records", [])
        proteins = st.session_state.get("protein_records", [])
        articles = st.session_state.get("pubmed_articles", [])

        selected_stats = None
        if records:
            st.markdown("### Nucleotide records")
            st.write(f"{len(records)} nucleotide record(s) retrieved.")
            selected_index = st.session_state.get("nucleotide_selector", 0)
            if isinstance(selected_index, int) and 0 <= selected_index < len(records):
                try:
                    selected_stats = analyze_sequence(
                        records[selected_index]["sequence"]
                    )
                    st.write(
                        f"**Selected sequence length:** "
                        f"{selected_stats['length']:,} bp"
                    )
                    st.write(
                        f"**GC content:** {selected_stats['gc_percentage']:.2f}%"
                    )
                    st.write(
                        f"**AT content:** {selected_stats['at_percentage']:.2f}%"
                    )
                except ValueError:
                    selected_stats = None

        if proteins:
            st.markdown("### Protein records")
            st.write(f"{len(proteins)} protein record(s) retrieved.")

        if articles:
            st.markdown("### Literature overview")
            st.write(f"{len(articles)} PubMed article(s) retrieved.")
            for article in articles[:3]:
                st.markdown(
                    f"- **{article['title']}** ({article['year']}) "
                    f"[PubMed]({article['url']})"
                )

        st.caption(
            "This summary assembles retrieved database information. "
            "It is not an AI-generated interpretation or clinical advice. "
            "Check the linked source records before drawing conclusions."
        )

        st.divider()
        st.subheader("Export report")

        try:
            pdf_bytes = create_gene_report(
                gene_name=gene_name,
                gene_id=gene_id,
                organism=organism_name,
                chromosome=chromosome,
                description=description,
                sequence_stats=selected_stats,
                articles=articles,
            )
            st.download_button(
                "📄 Download Research Report (PDF)",
                data=pdf_bytes,
                file_name=f"BioinformaticsResearchExplorer_report{gene_name}.pdf",
                mime="application/pdf",
                key="download_research_pdf",
            )
        except Exception as exc:
            st.error(
                "Could not generate the PDF report. Confirm that "
                "utils/report_generator.py exists and contains "
                f"create_gene_report(). Details: {exc}"
            )
