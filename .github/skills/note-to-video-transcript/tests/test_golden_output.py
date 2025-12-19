#!/usr/bin/env python3
"""
Golden file testing for transcript generation.

This script validates that the transcript generation workflow
produces expected output structure and content coverage.
"""

import re
import sys
from pathlib import Path


def validate_transcript_structure(transcript_text: str) -> list:
    """
    Validate that transcript follows required structure.
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check for required sections
    required_sections = [
        r"^#\s+.+$",  # Title
        r"^##\s+Hook",
        r"^##\s+Intro",
        r"^##\s+Section \d+:",
        r"^##\s+Recap",
        r"^##\s+Call to Action",
    ]
    
    for pattern in required_sections:
        if not re.search(pattern, transcript_text, re.MULTILINE):
            errors.append(f"Missing required section: {pattern}")
    
    # Check for metadata
    if "Target Duration" not in transcript_text:
        errors.append("Missing target duration metadata")
    
    if "Style Preset" not in transcript_text:
        errors.append("Missing style preset metadata")
    
    # Check for production notes
    if "Production Notes" not in transcript_text:
        errors.append("Missing production notes section")
    
    return errors


def validate_coverage(transcript_text: str, input_text: str) -> list:
    """
    Validate that major headings from input are covered.
    
    Returns:
        List of coverage warnings
    """
    warnings = []
    
    # Extract headings from input
    input_headings = re.findall(r"^##\s+(.+)$", input_text, re.MULTILINE)
    
    # Check if each heading is mentioned in transcript
    for heading in input_headings:
        # Clean heading for comparison
        clean_heading = heading.strip().lower()
        transcript_lower = transcript_text.lower()
        
        # Check if heading appears anywhere in transcript
        if clean_heading not in transcript_lower:
            # Also check for partial matches
            words = clean_heading.split()
            if len(words) > 1:
                key_word = max(words, key=len)  # Use longest word
                if key_word not in transcript_lower:
                    warnings.append(f"Heading possibly not covered: {heading}")
            else:
                warnings.append(f"Heading possibly not covered: {heading}")
    
    return warnings


def estimate_duration(transcript_text: str, words_per_minute: int = 150) -> float:
    """
    Estimate duration from transcript word count.
    
    Args:
        transcript_text: Full transcript
        words_per_minute: Speaking rate (default 150)
    
    Returns:
        Estimated duration in minutes
    """
    # Remove metadata and production notes
    main_content = re.sub(r"^>.*$", "", transcript_text, flags=re.MULTILINE)
    main_content = re.sub(r"\*\*Estimated Duration\*\*:.*$", "", main_content, flags=re.MULTILINE)
    
    # Count words
    words = len(main_content.split())
    
    return words / words_per_minute


def run_golden_test(input_file: Path, expected_file: Path, generated_file: Path) -> bool:
    """
    Run golden file test.
    
    Args:
        input_file: Original notes
        expected_file: Expected transcript structure
        generated_file: Generated transcript to validate
    
    Returns:
        True if tests pass, False otherwise
    """
    print("=" * 60)
    print("Golden File Test: Transcript Generation")
    print("=" * 60)
    
    # Read files
    if not input_file.exists():
        print(f"✗ Input file not found: {input_file}")
        return False
    
    if not expected_file.exists():
        print(f"✗ Expected file not found: {expected_file}")
        return False
    
    if not generated_file.exists():
        print(f"✗ Generated file not found: {generated_file}")
        print("  Run the transcript generation first:")
        print(f"  python scripts/build_transcript.py --input {input_file}")
        return False
    
    input_text = input_file.read_text(encoding="utf-8")
    expected_text = expected_file.read_text(encoding="utf-8")
    generated_text = generated_file.read_text(encoding="utf-8")
    
    # Run validations
    all_passed = True
    
    print("\n1. Structure Validation")
    print("-" * 60)
    errors = validate_transcript_structure(generated_text)
    if errors:
        all_passed = False
        print("✗ Structure validation failed:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ Structure validation passed")
    
    print("\n2. Coverage Validation")
    print("-" * 60)
    warnings = validate_coverage(generated_text, input_text)
    if warnings:
        print("⚠ Coverage warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("✓ Coverage validation passed")
    
    print("\n3. Duration Estimation")
    print("-" * 60)
    duration = estimate_duration(generated_text)
    print(f"Estimated duration: {duration:.1f} minutes")
    
    # Check if within tolerance (±15%)
    target_duration = 6.0  # Could be extracted from transcript
    tolerance = 0.15
    lower_bound = target_duration * (1 - tolerance)
    upper_bound = target_duration * (1 + tolerance)
    
    if lower_bound <= duration <= upper_bound:
        print(f"✓ Duration within target range ({lower_bound:.1f}-{upper_bound:.1f} min)")
    else:
        print(f"⚠ Duration outside target range ({lower_bound:.1f}-{upper_bound:.1f} min)")
    
    print("\n4. Expected Structure Comparison")
    print("-" * 60)
    
    # Compare section headings
    expected_sections = re.findall(r"^##\s+(.+)$", expected_text, re.MULTILINE)
    generated_sections = re.findall(r"^##\s+(.+)$", generated_text, re.MULTILINE)
    
    print(f"Expected sections: {len(expected_sections)}")
    print(f"Generated sections: {len(generated_sections)}")
    
    if set(expected_sections) == set(generated_sections):
        print("✓ Section headings match expected structure")
    else:
        print("⚠ Section headings differ from expected")
        missing = set(expected_sections) - set(generated_sections)
        extra = set(generated_sections) - set(expected_sections)
        if missing:
            print(f"  Missing: {missing}")
        if extra:
            print(f"  Extra: {extra}")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All critical tests passed!")
        print("=" * 60)
        return True
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return False


def main():
    # Set up paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    examples_dir = skill_dir / "examples"
    
    input_file = examples_dir / "input_note.md"
    expected_file = examples_dir / "expected_transcript.md"
    generated_file = Path("transcript.md")  # Default output location
    
    # Allow override via command line
    if len(sys.argv) > 1:
        generated_file = Path(sys.argv[1])
    
    # Run test
    success = run_golden_test(input_file, expected_file, generated_file)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
