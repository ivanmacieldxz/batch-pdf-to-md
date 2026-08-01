import os
import re
import tempfile
import shutil
import pymupdf4llm

def normalize_markdown(text: str) -> str:
    """
    Normalizes text according to the requirements:
    - No more than 2 consecutive newlines.
    - No strange tabs.
    - No more than 1 space between words.
    """
    # Replace more than 2 consecutive newlines with exactly 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace tabs with a single space
    text = re.sub(r'\t+', ' ', text)
    
    # Replace multiple spaces between words with a single space.
    # We use a positive lookbehind (?<=\S) to ensure we don't collapse
    # leading spaces (indentation) which are critical for markdown lists/code blocks.
    text = re.sub(r'(?<=\S)[ ]{2,}', ' ', text)
    
    return text

def process_file(input_pdf_path: str, output_md_path: str, margins=(0, 0, 0, 0)):
    """
    Converts a single PDF to Markdown and applies normalizations and RAG rules.
    """
    # Create a temporary directory to dump images so pymupdf4llm can insert
    # markdown image tags natively where they belong in the text flow.
    temp_dir = tempfile.mkdtemp()
    try:
        # Extract markdown, generating image links
        md_text = pymupdf4llm.to_markdown(input_pdf_path, write_images=True, image_path=temp_dir, margins=margins)
        
        # Replace image markdown tags with the [Imagen Omitida] placeholder for RAG
        # This matches standard markdown images: ![alt](url)
        md_text = re.sub(r'!\[.*?\]\(.*?\)', '[Imagen Omitida]', md_text)
        
        # Apply space/newline normalization
        md_text = normalize_markdown(md_text)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
        
        # Write the final markdown
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(md_text)
            
    finally:
        # Clean up the temporary images
        shutil.rmtree(temp_dir)

def process_batch(input_path: str, output_dir: str = None, margins=(0, 0, 0, 0)):
    """
    Processes either a single PDF file or a directory of PDFs.
    """
    # Default to ~/batch-pdf-to-md if no output_dir is provided
    if not output_dir:
        output_dir = os.path.join(os.path.expanduser('~'), 'batch-pdf-to-md')
        
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle single file
    if os.path.isfile(input_path) and input_path.lower().endswith('.pdf'):
        basename = os.path.basename(input_path)
        md_filename = os.path.splitext(basename)[0] + '.md'
        output_md_path = os.path.join(output_dir, md_filename)
        process_file(input_path, output_md_path, margins)
        return
        
    # Handle directory
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    
                    # Preserve relative path structure in output folder
                    rel_path = os.path.relpath(root, input_path)
                    if rel_path == '.':
                        out_subdir = output_dir
                    else:
                        out_subdir = os.path.join(output_dir, rel_path)
                        
                    md_filename = os.path.splitext(file)[0] + '.md'
                    output_md_path = os.path.join(out_subdir, md_filename)
                    
                    process_file(pdf_path, output_md_path, margins)
