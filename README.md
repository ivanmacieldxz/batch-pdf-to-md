# Batch PDF to Markdown Converter

A tool to convert PDF files (single or batch) to Markdown format, preserving semantic structures like headings and tables. It features a CLI and a modern GUI.

## Features
- Convert single PDFs or entire directories.
- Maintains semantic contents (tables, titles).
- Output text normalisation (spaces, blank lines).
- **RAG-ready formatting**: Converts PDFs keeping semantic structure (tables) and replaces images with `[Imagen Omitida]` placeholders to avoid context pollution in text-based RAG pipelines.
- Modern clean Graphical User Interface (GUI).
- Command Line Interface (CLI).

## Setup Instructions

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/ivanmacieldxz/batch-pdf-to-md.git
   cd batch-pdf-to-md
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

