# 🧠 Persona-Driven Document Intelligence — Round 1B

**Theme**: *Connect What Matters — For the User Who Matters*

This project implements an intelligent document analysis system that extracts, ranks, and summarizes the most relevant sections from a collection of documents based on a user-defined **persona** and **job-to-be-done (JTBD)**. The goal is to prioritize content that best serves the end user's task using lightweight and fast NLP techniques.

---

## ✨ Key Features

- 🔍 **Persona-Aware Relevance Detection**  
  Dynamically matches document content to persona and task context using sentence embeddings.

- 📄 **Structured Output Generation**  
  Outputs are ranked and formatted in a standardized JSON schema with metadata, key section highlights, and refined summaries.

- ⚙️ **Modular & Scalable Architecture**  
  Supports multiple test cases (document collections) and is easily extensible for different domains or personas.

- 💡 **Offline Execution**  
  All models are pre-downloaded and cached locally — no internet access required at runtime.

---

## 🎯 Use Case

This project is designed for **persona-driven document intelligence**. It takes as input:

- A **collection of PDFs** (e.g., product manuals, help documents, training guides)
- An **`input.json`** file describing:
  - A **persona** (e.g., "HR Professional", "Travel Planner", "Finance Manager")
  - A **Job-To-Be-Done (JTBD)** or goal (e.g., "Create and manage fillable forms", "Plan a 4-day trip")

### The system performs:

1. 📌 **Identification of Relevant Sections**
   - Ranks the most important sections across all documents that align with the persona’s JTBD.

2. 🧾 **Extraction of Key Content**
   - Retrieves fine-grained subsections and summaries from relevant pages.

3. 📤 **Structured Output**
   - Outputs a well-organized `output.json` containing metadata, ranked sections, and detailed summaries for downstream use.

---

## 🧠 Approach

The system follows a modular and extensible pipeline:

### 📄 1. Document Parsing
- **Tool**: [`pdfplumber`](https://github.com/jsvine/pdfplumber)
- **Function**: Extracts per-page text content from each PDF.
- **Structure**: Text is preserved page-wise to maintain layout fidelity for ranking and summarization.

### 📊 2. Section Embedding & Relevance Ranking
- **Tool**: [`sentence-transformers`](https://www.sbert.net/)
- **Model**: `all-MiniLM-L6-v2` (can be customized)
- **Method**:
  - Each paragraph/section is converted into a vector embedding.
  - Persona + JTBD description is also embedded.
  - **Cosine similarity** is used to compare document sections to the persona-JTBD prompt.
  - Top-N most relevant sections are selected for further analysis.

### 📝 3. Summarization
- **Tool**: [`transformers`](https://huggingface.co/transformers)
- **Model**: `distilbart-cnn-12-6` or compatible offline-capable summarizer.
- **Function**:
  - Refines extracted text into concise summaries while preserving semantic context.
  - Ensures the output is focused and relevant to the JTBD.

### 📦 4. JSON Structuring
- **Module**: `generate_output.py`
- **Role**:
  - Wraps all relevant metadata, section ranks, page numbers, and refined summaries into a clean, hierarchical JSON schema.
  - Ensures consistency for downstream use cases like search, visualization, or chatbot integration.

✅ This approach is lightweight, offline-friendly (no external API calls), and extensible for other NLP tasks like keyword extraction, classification, or chat integration.

---

## 🧰 Tech Stack & Models

| Tool | Purpose |
|------|---------|
| `pdfplumber` | PDF text extraction |
| `sentence-transformers` | Embedding + similarity scoring |
| `transformers` (`distilbart-cnn`) | Lightweight summarization |
| `json` | Output formatting |
| `os`, `datetime`, `pathlib` | File management and timestamping |

---

## 🗂️ Project Structure

```plaintext
├── input/
│   ├── Collection 1/
│   │   ├── PDFs/
│   │   └── input.json
│   ├── Collection 2/
│   └── Collection 3/
│
├── output/
│   └── Collection X/
│       └── output.json
│
├── round1b_main.py         # Main entry point
├── pdf_parse.py            # PDF parsing logic
├── nlp_utils.py            # NLP functions: embedding, summarization
├── generate_output.py      # Output formatting logic
├── README.md               # You're here
```

## 🗂️ Folder Structure

Each `Collection` folder in `input/` contains:

- `PDFs/` — a folder containing the document PDFs  
- `input.json` — defines the **persona** and **job-to-be-done**

Each run of the script creates:

- `output.json` inside the same `Collection` directory in the `output/` folder

🔧 **Note:** In `round1b_main.py`, you just need to change the collection name for:
 
 ```python
 INPUT_DIR ="input/Collection 2"
 pdf_dir = "input/Collection 2/PDFs"
 ```
 and simply run the script with:
 
 ```bash
 python round1b_main.py
 ```

---

## 🚀 Installation & Setup

## Manual Installation

### 1. Clone the Repository

```bash[
git clone https://github.com/sparsh2347/Adobe-India-Hacakthon-Round1B
cd Adobe-India-Hacakthon-Round1B
```
### 2. Set Up environment

```bash
pip install -r requirements.txt
```
**NOTE**: Ensure you have downloaded model weights into the .cache/ or hub/ directory for offline use.

### 3. Run the Script

 ```bash
python round1b_main.py
```

## 🐳 Docker Installation

### 🔧 Prerequisites

Ensure Docker is installed and running on your system:

- 🔗 [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Windows/Mac)
- 🐧 On Linux, install via your package manager:

```bash
sudo apt install docker.io
```

- You can verify your Docker installation using:
 ```bash
    docker --version
 ```

### Pull Prebuilt Docker Image
You can use our prebuilt image directly from Docker Hub:

```bash
docker pull cocane/adobe-round-1
```

### Run with docker

```bash
docker run cocane/adobe-round-1
```

**NOTE**:  Place your PDFs in the input/ folder. The structured JSON will be saved to output/.

## 📦 Dependencies

### ✅ Minimal Python Dependencies (already installed in container)

- `pdfplumber==0.10.2`  
- `pdfminer.six==20221105`  
- `Pillow==11.1.0`  
- `transformers==4.31.0`  
- `sentence-transformers==2.2.2`  
- `torch==2.1.2+cpu`  
- `scikit-learn`, `numpy`, `tqdm`, `regex`

---

### 🔧 System Dependencies (pre-installed in Docker)

The `Dockerfile` installs all essential libraries:

- `poppler-utils` – PDF parsing backend  
- `ghostscript`, `libjpeg`, `libpng`, `freetype` – for image processing  
- `libgl1`, `libtiff-dev`, `libopenjp2-7` – for broader image decoding support  
- `ffmpeg`, `curl`, `tcl/tk`, etc. – general compatibility for document/media formats  

---

💡 **Note:** All dependencies are bundled within the Docker container — no manual system-level setup is needed when using Docker.

## Sample Output Format (per collection)

```json
{
  "metadata": {
    "input_documents": [
      "Learn Acrobat - Create and Convert_1.pdf",
      "Learn Acrobat - Create and Convert_2.pdf",
      "Learn Acrobat - Edit_1.pdf",
      "Learn Acrobat - Edit_2.pdf",
      "Learn Acrobat - Export_1.pdf",
      "Learn Acrobat - Export_2.pdf",
      "Learn Acrobat - Fill and Sign.pdf",
      "Learn Acrobat - Generative AI_1.pdf",
      "Learn Acrobat - Generative AI_2.pdf",
      "Learn Acrobat - Request e-signatures_1.pdf",
      "Learn Acrobat - Request e-signatures_2.pdf",
      "Learn Acrobat - Share_1.pdf",
      "Learn Acrobat - Share_2.pdf",
      "Test Your Acrobat Exporting Skills.pdf",
      "The Ultimate PDF Sharing Checklist.pdf"
    ],
    "persona": "HR professional",
    "job_to_be_done": "Create and manage fillable forms for onboarding and compliance.",
    "processing_timestamp": "2025-07-28T23:11:53.564837"
  },
  "extracted_sections": [
    {
      "document": "Learn Acrobat - Fill and Sign.pdf",
      "section_title": "Interactive forms: These contain fields ",
      "importance_rank": 1,
      "page_number": 2
    },
    {
      "document": "Learn Acrobat - Request e-signatures_2.pdf",
      "section_title": "the document to remain certified. For ex",
      "importance_rank": 2,
      "page_number": 6
    },
    {
      "document": "Learn Acrobat - Fill and Sign.pdf",
      "section_title": "interactive fillable forms. Or, they int",
      "importance_rank": 3,
      "page_number": 8
    }
  ],
  "subsection_analysis": [
    {
      "document": "Learn Acrobat - Fill and Sign.pdf",
      "refined_text": " Interactive forms: These contain fields that you can select and fill in . Use the interactive forms to test your knowledge of stories you saw on CNN iReport .",
      "page_number": 2
    },
    {
      "document": "Learn Acrobat - Request e-signatures_2.pdf",
      "refined_text": " A government agency creates a form with a form to remain certified . The form is required to be certified by a government agency to be a certified document .",
      "page_number": 6
    }
  ]
}
```

### 🔍 Key Components

- **`metadata`**: Captures input context like persona, job-to-be-done (JTBD), list of PDFs processed, and timestamp.
- **`extracted_sections`**: Top-ranked sections from across PDFs, relevant to the given persona's JTBD.
- **`subsection_analysis`**: Finer-grained extractions with context-specific summaries for each section.



## 📈 Future Scope

- 🧩 **Image-based PDF support** using OCR integration (e.g., Tesseract or Document AI)  
- 🧠 **Smaller/faster summarizers** using distilled LLMs or rule-based extraction  
- 👥 **Multi-persona comparisons** across documents  
- 🗃️ **User interface** (GUI or web app) for uploading documents and configuring personas

## Team Details
**Team Name:** Pixels<br>
**Team Leader:** Sparsh Sinha<br>
**Team Members:** Rahul Naskar, Ayush Kumar
