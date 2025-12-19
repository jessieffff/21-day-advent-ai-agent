---
name: note-to-video-transcript
description: Transform study notes (Markdown or PDF) into a ready-to-record video transcript (5-8 minutes) with spoken language, natural pacing, and structured sections.
version: 1.0.0
author: GitHub Copilot Agent Skill
tags:
  - content-creation
  - video-production
  - transcript-generation
  - study-notes
  - spoken-script
---

# Note to Video Transcript

## Overview

This skill transforms study notes (Markdown or PDF format) into a ready-to-record video transcript. The output is a 5–8 minute spoken script with natural pacing, smooth transitions, and a clear structure suitable for educational video content.

## When to Use This Skill

Use this skill when:
- You have study notes in Markdown or PDF format
- You want to create a video script from written content
- You need a spoken-language transcript (not just reformatted text)
- Target video duration is 5–8 minutes
- Content should maintain educational fidelity while being conversational

## Input Requirements

**Supported Formats:**
- Markdown files (.md)
- PDF documents (.pdf)

**Content Expectations:**
- Structured with headings (# ## ###)
- Contains educational or explanatory content
- Includes concepts, definitions, or step-by-step explanations

## Output Contract

The skill produces `transcript.md` with the following structure:

1. **Title** - Clear, engaging video title
2. **Hook** (10–20 seconds) - Attention-grabbing opening
3. **Intro** - Context + what viewers will learn
4. **Main Sections** (2–5 chapters) - Core content broken into digestible parts
5. **Recap** - Concise bullet summary of key points
6. **CTA** - Call-to-action (follow/like/comment prompt)

**Quality Guarantees:**
- Coverage: All major headings addressed or explicitly marked as omitted
- Length: Target duration ±15% (estimated via words-per-minute)
- Accuracy: No new facts unless clearly labeled as expansions
- Tone: Spoken language, short sentences, smooth transitions

## Deterministic Workflow

### Step 1: Identify Input Format

Determine if input is Markdown or PDF.

### Step 2: Extract Content (PDF only)

If input is PDF:
- Run `scripts/extract_pdf_text.py`
- Convert PDF to Markdown-like text format
- Preserve structure and headings

### Step 3: Normalize Content

Run `scripts/normalize_notes.py` to:
- Preserve headings, code blocks, definitions
- Remove navigation sections, TOC, footers
- Normalize whitespace
- Convert bullet points to speakable sentences when needed

### Step 4: Build Outline

- Map input headings to transcript sections
- Allocate word budget per section based on target duration
- Ensure balanced coverage across topics
- Identify sections to expand or condense

### Step 5: Generate Transcript

Run `scripts/build_transcript.py` with:
- Input: normalized markdown
- Preset: neutral | xiaohongshu | professional
- Target duration: 5-8 minutes

The script will:
- Apply spoken tone transformation
- Create short, natural sentences
- Add explicit transitions between sections
- Insert hook, intro, recap, and CTA

### Step 6: Quality Pass

Perform automated checks:
- **Coverage Check**: Verify all major headings are addressed
- **Length Check**: Estimate duration (150 words/minute for spoken content)
- **Repetition Trimming**: Detect and remove excessive repeated phrases
- **Coherence**: Ensure smooth flow between sections

### Step 7: Write Output

Generate final files:
- `transcript.md` - Main deliverable
- `outline.md` (optional) - Section breakdown with word counts

## Example Usage

### Example 1: Markdown Input

**Input:** `notes/day10.md`
```markdown
# Understanding Agent Skills

## What are Agent Skills?

Agent skills extend GitHub Copilot's capabilities...

## Creating a Custom Skill

To create a skill, you need...

## Best Practices

Always include clear examples...
```

**User Prompt:**
```
Convert notes/day10.md into a 6-minute video transcript.
```

**Output:** `transcript.md`
```markdown
# Master Agent Skills in 6 Minutes

## Hook (15 sec)
Want to supercharge your GitHub Copilot? In the next six minutes, 
you'll learn how to create custom agent skills that do exactly 
what you need.

## Intro (30 sec)
Hey everyone! Today we're diving into GitHub Copilot Agent Skills. 
These are powerful extensions that let you teach Copilot new 
capabilities. By the end of this video, you'll understand what 
they are, how to build one, and the best practices to make them shine.

## Section 1: What are Agent Skills? (2 min)
Let's start with the basics. An agent skill is like giving Copilot 
a new superpower. Instead of just writing code, it can now perform 
specialized tasks...

[continues with natural spoken language]
```

### Example 2: PDF with Style Preset

**User Prompt:**
```
Convert notes/research.pdf into a 5–6 minute spoken script using 
the professional preset.
```

The skill will:
1. Extract text from PDF
2. Normalize content structure
3. Apply professional tone preset
4. Generate transcript targeting 5.5 minutes (825 words)

## Style Presets

### Neutral
- Balanced tone
- Medium sentence length (12-18 words)
- Minimal jargon
- General audience
- Simple transitions

### Xiaohongshu
- Conversational, friendly
- Short sentences (8-12 words)
- Emoji usage allowed
- Personal pronouns (we, you, I)
- Engaging hooks and CTAs

### Professional
- Formal but accessible
- Longer sentences (15-20 words)
- Technical terminology welcome
- Industry-standard transitions
- Authoritative tone

## Configuration Options

When invoking the skill, you can specify:

- **Target Duration**: 5-8 minutes (default: 6 minutes)
- **Style Preset**: neutral | xiaohongshu | professional (default: neutral)
- **Output Directory**: Where to save transcript.md (default: current directory)

## Success Criteria

A successful transcript must meet:

1. **Coverage**: Every major heading addressed or omission explained
2. **Length Accuracy**: Within ±15% of target duration
3. **Fact Accuracy**: No invented information (unless clearly marked)
4. **Spoken Quality**: Sounds natural when read aloud
5. **Structure Adherence**: Follows Title > Hook > Intro > Sections > Recap > CTA

## Limitations

- Optimal for 5-8 minute videos (shorter/longer may require manual adjustment)
- Best for educational/explanatory content (not suitable for narrative stories)
- Code-heavy content requires manual review for spoken clarity
- Image/diagram references need manual description

## Error Handling

The skill will warn if:
- Input file is empty or unreadable
- PDF extraction produces minimal text
- Estimated duration far exceeds target (>30% difference)
- Critical headings are missing

## Testing

Run golden file tests:
```bash
python tests/test_golden_output.py
```

This validates:
- Structure compliance
- Coverage completeness
- Length estimation accuracy

## Resources

- Template: `resources/transcript-template.md`
- Style presets: `resources/style-presets/*.md`
- Examples: `examples/`

## Future Enhancements

Planned additions:
- Multi-output pack (shotlist, captions, titles)
- Fidelity modes (strict vs. expanded)
- Long PDF chunking and hierarchical summarization
