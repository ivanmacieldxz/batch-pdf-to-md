import argparse
import sys
import os
from .converter import process_batch

def main():
    parser = argparse.ArgumentParser(
        description="Batch PDF to Markdown Converter with RAG-ready formatting."
    )
    
    parser.add_argument(
        'input', 
        nargs='?', 
        help="Path to the input PDF file or directory containing PDFs."
    )
    parser.add_argument(
        '-o', '--output', 
        help="Path to the output directory. Defaults to ~/batch-pdf-to-md",
        default=None
    )
    
    args = parser.parse_args()
    
    # If no input provided, we expect the user wanted the GUI or help.
    # Since this is the pure CLI script, we just show help if no args provided.
    if not args.input:
        parser.print_help()
        sys.exit(1)
        
    input_path = os.path.abspath(args.input)
    
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)
        
    print(f"Processing input: {input_path}")
    if args.output:
        print(f"Output directory: {args.output}")
    else:
        print(f"Output directory: Default (~/batch-pdf-to-md)")
        
    try:
        process_batch(input_path, args.output)
        print("Conversion completed successfully.")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
