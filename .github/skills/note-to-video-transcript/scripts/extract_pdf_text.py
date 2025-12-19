#!/usr/bin/env python3
"""
Extract text from PDF files and convert to Markdown format.

This script uses pdfplumber to extract text from PDF documents,
preserving structure and readability for downstream processing.
"""

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed.")
    print("Install it with: pip install pdfplumber")
    sys.exit(1)


def extract_pdf_text(pdf_path: Path, output_path: Path) -> bool:
    """
    Extract text from a PDF file and save as Markdown.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output Markdown file
    
    Returns:
        True if extraction successful, False otherwise
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            if total_pages == 0:
                print(f"Warning: PDF has no pages: {pdf_path}")
                return False
            
            print(f"Processing {total_pages} pages from {pdf_path.name}...")
            
            # Extract text from all pages
            extracted_text = []
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                if text:
                    # Add page separator for multi-page PDFs
                    if i > 1:
                        extracted_text.append(f"\n\n---\n<!-- Page {i} -->\n\n")
                    extracted_text.append(text)
                else:
                    print(f"Warning: No text found on page {i}")
            
            # Combine all text
            full_text = "".join(extracted_text)
            
            # Validate extraction
            if len(full_text.strip()) < 100:
                print(f"Warning: Extracted text is very short ({len(full_text)} chars)")
                print("This PDF may contain scanned images rather than text.")
                print("Consider using OCR tools instead.")
                return False
            
            # Write to output file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(full_text, encoding="utf-8")
            
            print(f"✓ Extracted {len(full_text)} characters")
            print(f"✓ Saved to: {output_path}")
            return True
            
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files to Markdown format"
    )
    parser.add_argument(
        "pdf_file",
        type=str,
        help="Path to the PDF file to extract"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=".tmp/extracted.md",
        help="Output path for extracted text (default: .tmp/extracted.md)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed extraction information"
    )
    
    args = parser.parse_args()
    
    # Validate input
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: File does not exist: {pdf_path}")
        sys.exit(1)
    
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Warning: File does not have .pdf extension: {pdf_path}")
    
    # Extract text
    output_path = Path(args.output)
    success = extract_pdf_text(pdf_path, output_path)
    
    if not success:
        sys.exit(1)
    
    print("\nNext steps:")
    print(f"  python scripts/normalize_notes.py {output_path}")


if __name__ == "__main__":
    main()
