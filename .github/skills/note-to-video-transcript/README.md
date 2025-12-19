# Note to Video Transcript Skill

A GitHub Copilot Agent Skill that transforms study notes (Markdown or PDF) into ready-to-record video transcripts with natural spoken language and structured sections.

## Quick Start

### Prerequisites

- VS Code Insiders with Agent Skills enabled
- Python 3.8+
- Required Python packages: `pdfplumber`, `pypdf`

### Installation

```bash
# Install Python dependencies
pip install pdfplumber pypdf
```

### Usage

Open VS Code and use natural language prompts:

```
Convert notes/day10.md into a 6-minute video transcript.
```

```
Convert notes/research.pdf into a 5-6 minute spoken script using the professional preset.
```

Copilot will automatically invoke this skill based on the description and examples in SKILL.md.

## Features

✅ **Multi-format Support**: Markdown and PDF input  
✅ **Spoken Language**: Natural, conversational tone  
✅ **Structured Output**: Hook, Intro, Sections, Recap, CTA  
✅ **Duration Control**: Target 5-8 minute videos  
✅ **Style Presets**: Neutral, Xiaohongshu, Professional  
✅ **Quality Checks**: Coverage, length, accuracy validation  

## File Structure

```
note-to-video-transcript/
├── SKILL.md                    # Core skill definition
├── README.md                   # This file
├── resources/
│   ├── transcript-template.md  # Output structure template
│   └── style-presets/
│       ├── neutral.md          # Balanced tone
│       ├── xiaohongshu.md      # Casual, friendly
│       └── professional.md     # Formal, authoritative
├── scripts/
│   ├── extract_pdf_text.py     # PDF to Markdown converter
│   ├── normalize_notes.py      # Content normalizer
│   └── build_transcript.py     # Transcript generator
├── examples/
│   ├── input_note.md           # Sample input
│   └── expected_transcript.md  # Sample output
└── tests/
    └── test_golden_output.py   # Golden file tests
```

## How It Works

1. **Input Detection**: Identify Markdown or PDF
2. **Content Extraction**: Convert PDF to text if needed
3. **Normalization**: Clean and structure content
4. **Outline Building**: Map headings to sections
5. **Transcript Generation**: Apply spoken tone and structure
6. **Quality Pass**: Validate coverage, length, accuracy
7. **Output**: Generate `transcript.md`

## Output Structure

Every transcript follows this format:

```markdown
# [Video Title]

## Hook (10-20 seconds)
Attention-grabbing opening...

## Intro
Context + learning outcomes...

## Section 1: [Topic]
Main content in spoken language...

## Section 2: [Topic]
More content...

## Recap
- Key point 1
- Key point 2
- Key point 3

## Call to Action
Follow/like/comment prompt...
```

## Style Presets

### Neutral (Default)
- Balanced, clear tone
- Medium sentence length
- General audience
- Minimal jargon

### Xiaohongshu
- Conversational, friendly
- Short sentences
- Personal pronouns
- Engaging hooks

### Professional
- Formal but accessible
- Technical terminology OK
- Industry-standard
- Authoritative

## Manual Usage (Scripts)

### Extract PDF Text

```bash
python scripts/extract_pdf_text.py notes/research.pdf
# Output: .tmp/extracted.md
```

### Normalize Content

```bash
python scripts/normalize_notes.py notes/day10.md
# Output: .tmp/normalized.md
```

### Build Transcript

```bash
python scripts/build_transcript.py \
  --input .tmp/normalized.md \
  --preset neutral \
  --minutes 6
# Output: transcript.md, outline.md
```

## Testing

Run golden file tests to ensure quality:

```bash
python tests/test_golden_output.py
```

This validates:
- Structure compliance
- Content coverage
- Length accuracy

## Configuration

Default settings (can be overridden):

- **Target Duration**: 6 minutes
- **Words per Minute**: 150 (spoken)
- **Style Preset**: neutral
- **Output Directory**: Current working directory

## Success Criteria

A quality transcript must have:

- ✅ All major headings covered (or omissions explained)
- ✅ Duration within ±15% of target
- ✅ No invented facts (accuracy preserved)
- ✅ Natural spoken tone
- ✅ Clear structure (Hook > Intro > Sections > Recap > CTA)

## Troubleshooting

**PDF extraction produces empty output**
- Check if PDF is text-based (not scanned images)
- Try converting PDF to text manually first

**Transcript is too long/short**
- Adjust `--minutes` parameter
- Review section allocation in outline
- Some content may be more verbose than expected

**Tone sounds robotic**
- Try different style presets
- Review and adjust preset configuration
- Some technical content requires manual refinement

## Contributing

This skill is designed to be:
- Self-contained and portable
- Easy to extract into a standalone repo
- Reusable across different projects

To modify:
1. Update templates in `resources/`
2. Adjust script logic in `scripts/`
3. Run tests to validate changes
4. Update examples as needed

## Roadmap

Future enhancements:
- Multi-output pack (shotlist, captions, titles)
- Fidelity modes (strict vs. expanded)
- Long PDF chunking
- Hierarchical summarization
- Custom voice/tone training

## License

See project LICENSE file.

## Support

For issues or questions:
1. Check examples in `examples/`
2. Review SKILL.md for workflow details
3. Run tests to validate setup
4. Check VS Code Agent Skills documentation
