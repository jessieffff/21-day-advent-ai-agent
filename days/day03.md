# Day 3 – Using AI Assistants to Generate Product Requirement Documents

_Timebox: ~1 hour_

## Knowledge goals

- Understand the structure and components of effective Product Requirement Documents (PRDs)
- Learn how to prompt AI assistants to generate comprehensive PRDs
- Identify best practices for iterating and refining AI-generated requirements
- Recognize when to use AI assistance vs. manual requirement writing

## Learning materials (≈ 20–25 minutes)

- Read: [**What is a PRD? Product Requirements Document Template**](https://www.atlassian.com/agile/product-management/requirements) (foundational understanding of PRD structure)
- Read: [**The Anatomy of a Product Requirements Document**](https://www.productplan.com/glossary/product-requirements-document/) (key components and best practices)


## Activities (about 30 minutes)

### Step-by-step: Generate a PRD with AI Assistant

**Step 1: Define your product idea (5 minutes)**
- Choose a simple product or feature to document (e.g., "user authentication system", "email notification service", "dashboard analytics widget")
- Write down 3-5 key points about what it should do

**Step 2: Craft your initial prompt (5 minutes)**
- Structure your prompt to include:
  - Product/feature name and brief description
  - Target users and use cases
  - Key objectives and success metrics
  - Technical constraints (if any)
  - Desired PRD format/sections

Example prompt:
```
Create a Product Requirements Document for [FEATURE NAME]. 
Include these sections: Overview, Objectives, User Stories, 
Functional Requirements, Non-Functional Requirements, Success Metrics, 
and Out of Scope. The feature should [BRIEF DESCRIPTION]. 
Target users are [USER TYPE].
```

**Step 3: Generate and review (10 minutes)**
- Run your prompt with an AI assistant (ChatGPT, Claude, Copilot, etc.)
- Review the output for:
  - Completeness of sections
  - Clarity and specificity of requirements
  - Alignment with your original intent
  - Missing edge cases or considerations

**Step 4: Iterate and refine (10 minutes)**
- Ask follow-up questions to expand specific sections:
  - "Add more details about edge cases for user authentication"
  - "Generate 5 additional user stories for power users"
  - "What security considerations should be added?"
  - "Create acceptance criteria for each functional requirement"
- Combine the best parts of multiple iterations

**Step 5: Document your process**
- Save your final PRD
- Note what prompts worked best
- Capture lessons learned in `notes/day03_notes.md`

## Checklist

Use this checklist to ensure your AI-generated PRD is complete:

### PRD Structure
- [ ] **Product/Feature Overview** - Clear description of what is being built
- [ ] **Problem Statement** - The problem this solves for users
- [ ] **Target Users** - Who will use this feature
- [ ] **Goals & Objectives** - What success looks like
- [ ] **User Stories** - At least 3-5 user stories in "As a [user], I want [goal], so that [benefit]" format
- [ ] **Functional Requirements** - Specific, testable features (numbered list)
- [ ] **Non-Functional Requirements** - Performance, security, scalability requirements
- [ ] **Success Metrics** - Measurable KPIs to track
- [ ] **Out of Scope** - What is explicitly NOT included
- [ ] **Dependencies** - Related systems, teams, or technologies
- [ ] **Timeline/Milestones** - High-level phases or deadlines

### Quality Checks
- [ ] Requirements are specific and measurable (not vague)
- [ ] User stories follow proper format and have acceptance criteria
- [ ] Edge cases and error scenarios are addressed
- [ ] Security and privacy considerations are included
- [ ] Accessibility requirements are mentioned (if applicable)
- [ ] Technical constraints are documented
- [ ] Stakeholders and decision-makers are identified
- [ ] Open questions and assumptions are clearly marked

### AI Prompt Quality
- [ ] Initial prompt included context about the product/feature
- [ ] Specified desired sections and format
- [ ] Used follow-up prompts to refine specific areas
- [ ] Validated AI output against domain knowledge
- [ ] Edited and personalized the final document

## Knowledge check

- What are the essential sections of a Product Requirements Document?
- How do you structure an effective prompt to generate a PRD with AI?
- What are 3 things you should always verify in an AI-generated PRD?
- When should you use AI assistance vs. writing requirements manually?
- How can you iterate with an AI assistant to improve requirement specificity?

## Bonus challenges

- Generate PRDs for the same feature using different AI assistants and compare results
- Take an existing PRD and use AI to identify gaps or missing requirements
- Create a custom prompt template you can reuse for future PRD generation
- Use AI to generate test cases or acceptance criteria from your PRD

## Resources for next steps

- Save your best prompt templates for future use
- Create a library of example PRDs for different product types
- Explore tools that integrate AI assistance directly into product management workflows (e.g., Productboard, Aha!, Linear)
