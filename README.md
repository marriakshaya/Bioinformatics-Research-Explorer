# 🧬 Bioinformatics Gene Explorer

**Bioinformatics Gene Explorer** is an interactive web application developed using Python and Streamlit to simplify the exploration of genetic information and biological research data.

The application integrates gene information from NCBI, DNA sequence analysis, protein data retrieval, and PubMed literature search within a single platform. It also provides sequence downloads and PDF research report generation through a user-friendly interface featuring a modern pink-and-rose color theme.

## ✨ Features

### 🧬 Gene Explorer

* Search genes by gene symbol and organism.
* Retrieve gene identifiers and available gene information from NCBI.
* View gene descriptions and related metadata.
---
## 🌐 Live Demo

🚀 **[Open Bioinformatics Gene Explorer](https://bioinformatics-gene-explorer-bu8wphwh8mufr7p223wryk.streamlit.app/)**

---
### 🧪 DNA Sequence Analysis

* Retrieve linked nucleotide and mRNA sequences.
* Display sequence accessions and descriptions.
* Calculate sequence length and nucleotide composition.
* Analyze GC and AT percentages.
* Visualize nucleotide counts.
* Download nucleotide sequences in FASTA format.

### 🔬 Protein Explorer

* Retrieve protein records associated with the selected gene.
* Explore protein accessions, descriptions, and amino acid sequences.
* Download protein sequences in FASTA format.

### 📚 Scientific Literature Search

* Search PubMed for research articles related to a gene.
* View article titles, authors, publication years, and abstracts.
* Access original publications through PubMed links.

### 📄 Research Summary and PDF Export

* Present a consolidated summary of the selected gene and available analysis results.
* Export a downloadable PDF research report.

### 🎨 User Interface

* Custom pink, blush, and rose-red color theme.
* Interactive Streamlit tabs.
* Organized sections for gene, DNA, protein, and literature exploration.
* Simple workflow designed for students and bioinformatics learners.

## 🛠️ Technologies Used

| Technology       | Purpose                                             |
| ---------------- | --------------------------------------------------- |
| Python           | Core application logic                              |
| Streamlit        | Interactive web interface                           |
| Requests         | Communication with NCBI and PubMed APIs             |
| Pandas           | Tabular data handling                               |
| NCBI E-utilities | Gene, nucleotide, and protein information retrieval |
| PubMed           | Scientific literature retrieval                     |
| ReportLab        | PDF report generation                               |

## 📁 Project Structure

```text
Bioinformatics Gene Explorer/
│
├── app.py
├── requirements.txt
│
├── services/
│   ├── __init__.py
│   ├── ncbi_gene.py
│   ├── ncbi_sequence.py
│   ├── ncbi_protein.py
│   └── pubmed.py
│
└── utils/
    ├── __init__.py
    ├── sequence_analysis.py
    └── report_generator.py
```

## 🚀 Installation and Setup

### Prerequisites

* Python 3.10 or a compatible version for the installed dependencies.
* Internet access to retrieve information from NCBI and PubMed.
* Git, if you want to clone the repository.

### 1. Clone the repository

### 2. Navigate to the project folder

### 3. Install dependencies

### 4. Run the application

Streamlit will provide a local URL in the terminal. Open that URL in your browser to use GeneLens AI.

> **Note:** This project can be run with a normal Python installation; creating a virtual environment is optional.

## 🧭 How to Use

1. Launch the application.
2. Enter a gene symbol, such as `BRCA1`, and select the organism.
3. Click the search button to retrieve the available gene information.
4. Explore the **Gene Overview** tab.
5. Open **DNA Analysis** to inspect nucleotide sequences and composition.
6. Use **Protein Explorer** to retrieve and download available protein records.
7. Search for related publications in **Literature**.
8. Open **Research Summary** to review the available results and export a PDF report.

Results depend on the selected gene and the records available through the connected databases.

## 🎯 Project Objectives

* Make commonly used gene information easier to explore in one interface.
* Simplify basic nucleotide sequence analysis.
* Connect gene research with related protein records and scientific publications.
* Provide downloadable sequence data and research summaries.
* Develop practical skills in Python, API integration, data processing, and bioinformatics application development.

## 🎓 Skills Demonstrated

* Python programming
* Bioinformatics data exploration
* REST API integration
* Biological sequence analysis
* Data visualization and presentation
* Streamlit application development
* Modular software design
* Scientific research and documentation

## 🔮 Future Improvements

Potential future enhancements include:

* Open reading frame (ORF) detection.
* DNA motif search.
* Additional sequence analysis tools.
* Improved data provenance and retrieval metadata.
* More report customization options.

These are possible future extensions and are not presented as existing features.

## ⚠️ Limitations

* Gene and sequence availability varies by organism and database record.
* The application requires internet access for live database retrieval.
* Results should be checked against the original scientific sources before being used in formal research.
* The application is intended as a research and learning aid, not a substitute for expert biological interpretation.

## 👩‍💻 Author

**Marri Akshaya**
