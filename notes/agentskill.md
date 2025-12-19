 ==================================================
Implementation Plan
Copilot Agent Skill: note-to-video-transcript
==================================================

Goal
----
Build a GitHub Copilot Agent Skill that transforms study notes
(Markdown or PDF) into a ready-to-record video transcript
(5–8 minutes, spoken language, structured sections).

This skill is added to an existing project repo under:
.github/skills/note-to-video-transcript/

It is designed to be reusable, testable, and easy to publish later.


--------------------------------------------------
1. Scope & Success Criteria
--------------------------------------------------

User Story
----------
As a learner, I want to turn my study notes (Markdown or PDF)
into a natural, spoken video transcript that I can read
directly while recording.

Primary Output
--------------
- transcript.md

Transcript Structure (required)
--------------------------------
- Title
- Hook (10–20 seconds)
- Intro (context + what viewers will learn)
- Main Sections (2–5 chapters)
- Recap (concise bullet summary)
- CTA (follow / like / comment prompt)

Acceptance Criteria
-------------------
- Coverage:
  Every major heading in the notes is covered or explicitly
  marked as omitted (with a reason).
- Length:
  Target duration achieved within ±15%
  (estimated via words-per-minute).
- Accuracy:
  No new facts introduced unless clearly labeled
  as assumptions or expansions.
- Tone:
  Spoken language, short sentences, smooth transitions.


--------------------------------------------------
2. Repository Layout
--------------------------------------------------

Add the following structure to the project repo:

.github/
  skills/
    note-to-video-transcript/
      SKILL.md
      README.md
      resources/
        transcript-template.md
        style-presets/
          neutral.md
          xiaohongshu.md
          professional.md
      scripts/
        extract_pdf_text.py
        normalize_notes.py
        build_transcript.py
      examples/
        input_note.md
        expected_transcript.md
      tests/
        test_golden_output.py

Design Principles
-----------------
- Skill is self-contained and portable
- No hard-coded assumptions about repo structure
- Scripts are generic utilities, not project-specific logic
- Easy to extract this folder into a standalone public repo later


--------------------------------------------------
3. SKILL.md (Core Skill Definition)
--------------------------------------------------

Purpose
-------
SKILL.md defines when Copilot should use the skill and
exactly how the workflow should be executed.

Required Frontmatter
--------------------
- name: note-to-video-transcript
- description:
  Explicitly mention:
  - study notes
  - markdown or pdf
  - video transcript
  - ready-to-record
  - 5–8 minute spoken script

Deterministic Workflow (must be documented)
-------------------------------------------
1. Identify input format (Markdown or PDF)
2. If PDF:
   - Run extract_pdf_text.py
3. Normalize content
   - Preserve headings, code blocks, definitions
   - Remove noise (TOC, footers, duplicated headers)
4. Build outline
   - Map headings to transcript sections
   - Allocate word budget per section
5. Generate transcript
   - Spoken tone
   - Short sentences
   - Explicit transitions
6. Quality pass
   - Coverage check
   - Length check
   - Repetition trimming
7. Write output
   - transcript.md
   - optional outline.md

Output Contract
---------------
Transcript must follow a fixed structure
(Title, Hook, Intro, Sections, Recap, CTA).

Include at least one concrete example
(Markdown input -> transcript output).


--------------------------------------------------
4. Script Implementations
--------------------------------------------------

4.1 extract_pdf_text.py
-----------------------
Purpose:
- Convert PDF notes into clean, readable text
- Output Markdown-like content

Requirements:
- Use pdfplumber or pypdf
- Preserve page breaks with separators
- Output to .tmp/extracted.md
- Warn if extracted text is too short or empty

4.2 normalize_notes.py
----------------------
Purpose:
- Normalize Markdown into a consistent content format

Responsibilities:
- Keep headings (#, ##, ###)
- Preserve code blocks
- Convert bullet points into speakable sentences (when needed)
- Remove navigation sections, reference-only footers
- Normalize whitespace

4.3 build_transcript.py
-----------------------
Purpose:
- Convert normalized notes into a spoken transcript

Inputs:
- --input <markdown file>
- --preset neutral | xiaohongshu | professional
- --minutes <float>

Outputs:
- transcript.md
- optional outline.md

Logic:
- Estimate word count from target minutes
- Allocate words per section
- Insert transitions and recap
- Apply style rules from preset


--------------------------------------------------
5. Resources & Style Presets
--------------------------------------------------

Transcript Template
-------------------
resources/transcript-template.md defines the fixed structure
used by all transcripts.

Style Presets
-------------
Each preset defines:
- Sentence length
- Tone and pacing
- Emoji usage (if any)
- CTA style
- Jargon tolerance

Presets:
- neutral
- xiaohongshu
- professional

Style logic is separate from transcript logic.


--------------------------------------------------
6. Testing & Evaluation
--------------------------------------------------

Golden File Testing
-------------------
- examples/input_note.md
- examples/expected_transcript.md

Test Behavior:
- Run normalization + transcript build
- Compare structure and content
- Allow minor whitespace differences

Quality Checks
--------------
- Coverage: all headings addressed
- Length: estimated duration within tolerance
- Repetition: detect excessive repeated phrases

Purpose:
- Prevent silent degradation as prompts/templates evolve


--------------------------------------------------
7. VS Code Usage
--------------------------------------------------

Requirements
------------
- VS Code Insiders
- Agent Skills enabled

Typical Prompts
---------------
- Convert notes/day10.md into a 6-minute video transcript.
- Convert notes/day10.pdf into a 5–6 minute spoken script
  using the neutral preset.

The skill should be auto-selected by Copilot
based on description and examples.


--------------------------------------------------
8. Future Enhancements (Post-MVP)
--------------------------------------------------

- Multi-output pack:
  - shotlist.md
  - caption.md
  - title_options.md

- Fidelity modes:
  - strict (no added content)
  - expanded (labeled assumptions)

- Long PDF chunking:
  - per-section extraction
  - hierarchical summarization

These upgrades should not require changes
to the core skill contract.


--------------------------------------------------
9. Implementation Milestones
--------------------------------------------------

Milestone 1:
- Folder + SKILL.md + template + example

Milestone 2:
- Markdown path fully working
- Golden test passing

Milestone 3:
- PDF extraction support added

Milestone 4:
- Multiple style presets finalized

==================================================
End of Implementation Plan
==================================================