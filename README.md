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

## Usage

### Graphical User Interface (GUI)
To launch the modern graphical interface, simply run the main script with no arguments:
```bash
python main.py
```
This will open a window where you can easily select your input files/folders and output destination.

### Command Line Interface (CLI)
You can also run the tool directly from the terminal for scripting or quick conversions:
```bash
python main.py <input_path> [-o <output_directory>]
```
- `<input_path>`: The path to a single PDF file or a folder containing PDFs.
- `-o, --output`: (Optional) The folder where markdown files will be saved. Defaults to `~/batch-pdf-to-md`.

**Example:**
```bash
python main.py ./my_pdfs -o ./converted_markdowns
```

