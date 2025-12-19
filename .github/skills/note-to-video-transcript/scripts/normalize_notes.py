#!/usr/bin/env python3
"""
Normalize Markdown notes into a consistent format for transcript generation.

This script cleans and structures content while preserving headings,
code blocks, and key information.
"""

import argparse
import re
import sys
from pathlib import Path


def normalize_notes(input_text: str) -> str:
    """
    Normalize Markdown content for transcript processing.
    
    Args:
        input_text: Raw Markdown content
    
    Returns:
        Normalized Markdown text
    """
    lines = input_text.split("\n")
    normalized = []
    in_code_block = False
    skip_until_blank = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track code blocks (preserve them)
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            normalized.append(line)
            continue
        
        # Preserve code block content as-is
        if in_code_block:
            normalized.append(line)
            continue
        
        # Remove table of contents patterns
        if re.match(r"^#{1,6}\s*(table of contents|contents|toc)$", stripped, re.IGNORECASE):
            skip_until_blank = True
            continue
        
        # Skip TOC entries
        if skip_until_blank:
            if not stripped:
                skip_until_blank = False
            continue
        
        # Remove horizontal rules (keep page breaks from PDF)
        if stripped == "---" and i > 0:
            prev_line = lines[i-1].strip()
            if not prev_line.startswith("<!--"):
                continue
        
        # Remove reference-only links at end of document
        if stripped.startswith("[") and "]: " in stripped:
            continue
        
        # Remove empty headings
        if re.match(r"^#{1,6}\s*$", stripped):
            continue
        
        # Preserve headings
        if stripped.startswith("#"):
            # Ensure proper spacing around headings
            if normalized and normalized[-1].strip():
                normalized.append("")
            normalized.append(line)
            normalized.append("")
            continue
        
        # Skip multiple consecutive blank lines
        if not stripped:
            if not normalized or normalized[-1].strip():
                normalized.append("")
            continue
        
        # Convert bullet points to paragraphs when they're definition-like
        bullet_match = re.match(r"^[-*+]\s+(.+)$", stripped)
        if bullet_match:
            content = bullet_match.group(1)
            # Keep as bullet if short
            if len(content) < 100:
                normalized.append(line)
            else:
                # Convert long bullets to paragraphs
                normalized.append(content)
            continue
        
        # Preserve other content
        normalized.append(line)
    
    # Join and clean up extra whitespace
    result = "\n".join(normalized)
    
    # Remove more than 2 consecutive newlines
    result = re.sub(r"\n{3,}", "\n\n", result)
    
    # Clean up spaces before/after headings
    result = re.sub(r"\n+(#{1,6}[^\n]+)\n+", r"\n\n\1\n\n", result)
    
    return result.strip() + "\n"


def extract_metadata(text: str) -> dict:
    """
    Extract metadata from normalized notes.
    
    Returns dict with:
        - heading_count: number of headings
        - word_count: approximate words
        - has_code: whether code blocks present
    """
    headings = re.findall(r"^#{1,6}\s+.+$", text, re.MULTILINE)
    code_blocks = re.findall(r"```", text)
    
    # Remove code blocks and count words
    text_without_code = re.sub(r"```[\s\S]*?```", "", text)
    words = len(text_without_code.split())
    
    return {
        "heading_count": len(headings),
        "word_count": words,
        "has_code": len(code_blocks) >= 2,
        "headings": [h.strip("# ").strip() for h in headings]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Normalize Markdown notes for transcript generation"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the Markdown file to normalize"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=".tmp/normalized.md",
        help="Output path for normalized content (default: .tmp/normalized.md)"
    )
    parser.add_argument(
        "-m", "--metadata",
        action="store_true",
        help="Print metadata about the normalized content"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File does not exist: {input_path}")
        sys.exit(1)
    
    # Read and normalize
    print(f"Normalizing {input_path.name}...")
    
    try:
        input_text = input_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("Error: File encoding is not UTF-8")
        sys.exit(1)
    
    normalized_text = normalize_notes(input_text)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_text, encoding="utf-8")
    
    print(f"✓ Normalized content saved to: {output_path}")
    
    # Show metadata if requested
    if args.metadata:
        metadata = extract_metadata(normalized_text)
        print(f"\nMetadata:")
        print(f"  Headings: {metadata['heading_count']}")
        print(f"  Words: {metadata['word_count']}")
        print(f"  Has code blocks: {metadata['has_code']}")
        
        if metadata['headings']:
            print(f"\n  Heading structure:")
            for heading in metadata['headings']:
                print(f"    - {heading}")
    
    print("\nNext steps:")
    print(f"  python scripts/build_transcript.py --input {output_path} --minutes 6")


if __name__ == "__main__":
    main()
