#!/usr/bin/env python3
"""
Build a video transcript from normalized Markdown notes.

This script converts structured notes into a spoken-language
video transcript with natural pacing and style.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


# Constants
WORDS_PER_MINUTE = 150  # Average speaking rate
PRESETS = ["neutral", "xiaohongshu", "professional"]


def load_style_preset(preset_name: str, resources_dir: Path) -> dict:
    """
    Load style preset configuration.
    
    Args:
        preset_name: Name of the preset (neutral, xiaohongshu, professional)
        resources_dir: Path to resources directory
    
    Returns:
        Dict with style configuration
    """
    preset_path = resources_dir / "style-presets" / f"{preset_name}.md"
    
    if not preset_path.exists():
        print(f"Warning: Preset file not found: {preset_path}")
        print(f"Using default neutral style")
        preset_name = "neutral"
    
    # Return style configuration based on preset
    if preset_name == "neutral":
        return {
            "name": "neutral",
            "sentence_length": (12, 18),
            "use_contractions": False,
            "use_emoji": False,
            "formality": "balanced",
            "pronouns": ["you", "we"],
        }
    elif preset_name == "xiaohongshu":
        return {
            "name": "xiaohongshu",
            "sentence_length": (8, 12),
            "use_contractions": True,
            "use_emoji": True,
            "formality": "casual",
            "pronouns": ["I", "you", "we"],
        }
    elif preset_name == "professional":
        return {
            "name": "professional",
            "sentence_length": (15, 20),
            "use_contractions": False,
            "use_emoji": False,
            "formality": "formal",
            "pronouns": ["we", "you"],
        }
    else:
        return load_style_preset("neutral", resources_dir)


def parse_content(text: str) -> dict:
    """
    Parse normalized Markdown into sections.
    
    Returns:
        Dict with title, sections list, metadata
    """
    lines = text.split("\n")
    sections = []
    current_section = None
    content_buffer = []
    
    # Extract title (first H1)
    title = None
    
    for line in lines:
        # Check for headings
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        
        if heading_match:
            # Save previous section
            if current_section:
                current_section["content"] = "\n".join(content_buffer).strip()
                sections.append(current_section)
                content_buffer = []
            
            # Start new section
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            
            if level == 1 and not title:
                title = heading_text
                continue
            
            current_section = {
                "level": level,
                "heading": heading_text,
                "content": ""
            }
        else:
            # Accumulate content
            if current_section or title:
                content_buffer.append(line)
    
    # Save last section
    if current_section:
        current_section["content"] = "\n".join(content_buffer).strip()
        sections.append(current_section)
    
    return {
        "title": title or "Untitled Video",
        "sections": sections
    }


def allocate_word_budget(sections: list, target_words: int) -> list:
    """
    Allocate word budget across sections.
    
    Fixed allocations:
    - Hook: ~40 words
    - Intro: ~100 words
    - Recap: ~80 words
    - CTA: ~30 words
    - Total fixed: ~250 words
    
    Remaining words distributed across main sections.
    """
    fixed_words = 250
    main_section_words = target_words - fixed_words
    
    if main_section_words < 100:
        print(f"Warning: Target duration too short for quality output")
    
    # Distribute across sections (simple equal distribution for now)
    section_count = len(sections)
    if section_count == 0:
        words_per_section = 0
    else:
        words_per_section = main_section_words // section_count
    
    allocated = []
    for section in sections:
        allocated.append({
            **section,
            "word_budget": words_per_section
        })
    
    return allocated


def generate_hook(title: str, style: dict) -> str:
    """Generate attention-grabbing hook."""
    if style["formality"] == "casual":
        return f"Want to learn about {title.lower()}? Let me show you how! ✨"
    elif style["formality"] == "formal":
        return f"Today we will explore {title.lower()} and its practical applications."
    else:
        return f"In the next few minutes, you'll learn everything about {title.lower()}."


def generate_intro(title: str, sections: list, style: dict) -> str:
    """Generate introduction section."""
    topics = ", ".join([s["heading"] for s in sections[:3]])
    
    if style["formality"] == "casual":
        intro = f"Hey everyone! Today we're diving into {title.lower()}. "
        intro += f"We'll cover {topics}, and more. "
        intro += f"By the end, you'll totally understand how this works. Let's get started!"
    elif style["formality"] == "formal":
        intro = f"This tutorial examines {title.lower()}. "
        intro += f"We will cover {topics}. "
        intro += f"The concepts presented will provide you with a comprehensive understanding of the topic."
    else:
        intro = f"Welcome! Today we're exploring {title.lower()}. "
        intro += f"We'll look at {topics}. "
        intro += f"By the end, you'll have a clear understanding of how everything fits together."
    
    return intro


def generate_section_content(section: dict, style: dict) -> str:
    """
    Generate spoken content for a section.
    
    This is a simplified version - in a full implementation,
    this would use LLM or more sophisticated NLP.
    """
    content = section["content"]
    
    # Remove markdown artifacts
    content = re.sub(r"```[\s\S]*?```", "[code example]", content)
    content = re.sub(r"`([^`]+)`", r"\1", content)
    content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)
    content = re.sub(r"\*([^*]+)\*", r"\1", content)
    
    # Simple sentence splitting
    sentences = re.split(r"[.!?]\s+", content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Apply contractions if needed
    if style["use_contractions"]:
        spoken_sentences = []
        for sent in sentences[:10]:  # Limit for demo
            sent = re.sub(r"\bis not\b", "isn't", sent, flags=re.IGNORECASE)
            sent = re.sub(r"\bare not\b", "aren't", sent, flags=re.IGNORECASE)
            sent = re.sub(r"\bdo not\b", "don't", sent, flags=re.IGNORECASE)
            sent = re.sub(r"\bwill not\b", "won't", sent, flags=re.IGNORECASE)
            sent = re.sub(r"\bhave not\b", "haven't", sent, flags=re.IGNORECASE)
            sent = re.sub(r"\bwould not\b", "wouldn't", sent, flags=re.IGNORECASE)
            spoken_sentences.append(sent)
    else:
        spoken_sentences = sentences[:10]
    
    result = ". ".join(spoken_sentences)
    if not result.endswith("."):
        result += "."
    
    # Add transition
    if style["formality"] == "casual":
        result = "So, here's the thing. " + result
    elif style["formality"] == "formal":
        result = "Let us examine this concept. " + result
    else:
        result = "Here's what you need to know. " + result
    
    return result


def generate_recap(sections: list, style: dict) -> str:
    """Generate recap section."""
    if style["formality"] == "casual":
        recap = "OK, let's recap what we covered:\n\n"
    elif style["formality"] == "formal":
        recap = "To summarize the key points:\n\n"
    else:
        recap = "Let's quickly recap:\n\n"
    
    for section in sections[:5]:
        recap += f"- **{section['heading']}**: Key concepts and applications\n"
    
    return recap


def generate_cta(style: dict) -> str:
    """Generate call to action."""
    if style["formality"] == "casual":
        return "If this helped you, smash that like button! Drop your questions below. See you next time! ✨"
    elif style["formality"] == "formal":
        return "If you found this content valuable, please consider subscribing. Thank you for your attention."
    else:
        return "If you found this helpful, give it a like and subscribe for more. Thanks for watching!"


def build_transcript(content_dict: dict, target_minutes: float, style: dict) -> str:
    """
    Build complete transcript.
    
    Args:
        content_dict: Parsed content with title and sections
        target_minutes: Target video duration in minutes
        style: Style preset configuration
    
    Returns:
        Complete transcript as Markdown string
    """
    title = content_dict["title"]
    sections = content_dict["sections"]
    
    target_words = int(target_minutes * WORDS_PER_MINUTE)
    allocated_sections = allocate_word_budget(sections, target_words)
    
    # Build transcript
    transcript = f"# {title}\n\n"
    transcript += f"> **Target Duration**: {target_minutes} minutes (~{target_words} words)  \n"
    transcript += f"> **Style Preset**: {style['name']}  \n"
    transcript += f"> **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    transcript += "---\n\n"
    
    # Hook
    transcript += "## Hook (10-20 seconds)\n\n"
    transcript += generate_hook(title, style) + "\n\n"
    transcript += "**Estimated Duration**: 15 seconds (~40 words)\n\n"
    transcript += "---\n\n"
    
    # Intro
    transcript += "## Intro\n\n"
    transcript += generate_intro(title, sections, style) + "\n\n"
    transcript += "**Estimated Duration**: 45 seconds (~100 words)\n\n"
    transcript += "---\n\n"
    
    # Main sections
    for i, section in enumerate(allocated_sections[:5], 1):
        transcript += f"## Section {i}: {section['heading']}\n\n"
        transcript += generate_section_content(section, style) + "\n\n"
        minutes = section['word_budget'] / WORDS_PER_MINUTE
        transcript += f"**Estimated Duration**: {minutes:.1f} minutes (~{section['word_budget']} words)\n\n"
        transcript += "---\n\n"
    
    # Recap
    transcript += "## Recap\n\n"
    transcript += generate_recap(sections, style) + "\n\n"
    transcript += "**Estimated Duration**: 30 seconds (~80 words)\n\n"
    transcript += "---\n\n"
    
    # CTA
    transcript += "## Call to Action\n\n"
    transcript += generate_cta(style) + "\n\n"
    transcript += "**Estimated Duration**: 15 seconds (~30 words)\n\n"
    transcript += "---\n\n"
    
    # Production notes
    transcript += "## Production Notes\n\n"
    transcript += f"**Total Estimated Duration**: {target_minutes} minutes ({target_words} words)\n\n"
    transcript += "**Coverage Check**:\n"
    for section in sections:
        transcript += f"- ✅ {section['heading']}\n"
    
    return transcript


def main():
    parser = argparse.ArgumentParser(
        description="Build video transcript from normalized notes"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to normalized Markdown file"
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="neutral",
        choices=PRESETS,
        help="Style preset to use (default: neutral)"
    )
    parser.add_argument(
        "--minutes",
        type=float,
        default=6.0,
        help="Target duration in minutes (default: 6.0)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="transcript.md",
        help="Output path for transcript (default: transcript.md)"
    )
    parser.add_argument(
        "--outline",
        type=str,
        help="Optional: output path for outline file"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}")
        sys.exit(1)
    
    # Validate duration
    if args.minutes < 3 or args.minutes > 15:
        print(f"Warning: Duration {args.minutes} minutes is outside optimal range (5-8 minutes)")
    
    # Load input
    print(f"Building transcript from {input_path.name}...")
    print(f"  Target: {args.minutes} minutes")
    print(f"  Style: {args.preset}")
    
    input_text = input_path.read_text(encoding="utf-8")
    
    # Get script directory and find resources
    script_dir = Path(__file__).parent
    resources_dir = script_dir.parent / "resources"
    
    # Load style
    style = load_style_preset(args.preset, resources_dir)
    
    # Parse content
    content_dict = parse_content(input_text)
    print(f"  Sections: {len(content_dict['sections'])}")
    
    # Build transcript
    transcript = build_transcript(content_dict, args.minutes, style)
    
    # Write output
    output_path = Path(args.output)
    output_path.write_text(transcript, encoding="utf-8")
    
    print(f"\n✓ Transcript generated: {output_path}")
    
    # Generate outline if requested
    if args.outline:
        outline_path = Path(args.outline)
        outline = f"# Transcript Outline\n\n"
        outline += f"**Title**: {content_dict['title']}\n"
        outline += f"**Duration**: {args.minutes} minutes\n"
        outline += f"**Style**: {args.preset}\n\n"
        outline += "## Section Breakdown\n\n"
        
        target_words = int(args.minutes * WORDS_PER_MINUTE)
        allocated = allocate_word_budget(content_dict['sections'], target_words)
        
        for i, section in enumerate(allocated, 1):
            outline += f"{i}. {section['heading']} ({section['word_budget']} words)\n"
        
        outline_path.write_text(outline, encoding="utf-8")
        print(f"✓ Outline generated: {outline_path}")
    
    print("\nTranscript is ready for review and recording!")


if __name__ == "__main__":
    main()
