"""
File: backend/prompts/notes_prompts.py

Prompt templates used by the Study Notes Service.
"""

# ==========================================================
# Complete Study Notes Prompt
# ==========================================================

NOTES_PROMPT = """
You are an expert AI Tutor and Research Assistant.

Your task is to generate comprehensive study notes
using ONLY the provided document context.

==========================================================
DOCUMENT CONTEXT

{context}

==========================================================

Generate the following sections.

# Overview

Briefly explain the topic.

----------------------------------------------------------

# Important Concepts

Explain every important concept.

Use headings and bullet points.

----------------------------------------------------------

# Key Definitions

List important definitions.

----------------------------------------------------------

# Important Algorithms / Methods

For every algorithm include

• Purpose

• Workflow

• Advantages

• Limitations

----------------------------------------------------------

# Important Formulas

If formulas are available,
explain them.

----------------------------------------------------------

# Key Takeaways

Generate concise revision points.

----------------------------------------------------------

# Summary

Summarize the notes.

Do NOT hallucinate.

Only use the supplied context.
"""

# ==========================================================
# Short Notes Prompt
# ==========================================================

SHORT_NOTES_PROMPT = """
You are an AI Tutor.

Generate concise revision notes.

Context

{context}

Requirements

• Bullet points

• Easy to revise

• Maximum 2 pages

Use only the supplied context.
"""

# ==========================================================
# Detailed Notes Prompt
# ==========================================================

DETAILED_NOTES_PROMPT = """
Generate detailed study notes.

Context

{context}

Include

• Concepts

• Explanation

• Examples

• Applications

• Advantages

• Limitations

Return well-structured notes.

Only use the provided context.
"""

# ==========================================================
# Flashcards Prompt
# ==========================================================

FLASHCARD_PROMPT = """
Generate flashcards from the following document.

Context

{context}

Return in the following format.

Question:
...

Answer:
...

Generate at least 20 flashcards.

Only use the provided context.
"""

# ==========================================================
# Interview Questions Prompt
# ==========================================================

INTERVIEW_QUESTIONS_PROMPT = """
You are a Senior Technical Interviewer.

Using the following document,

Context

{context}

Generate interview questions.

Difficulty Levels

Easy

Medium

Hard

For every question provide

Question

Answer

Generate at least

10 Easy

10 Medium

10 Hard

Only use the supplied context.
"""

# ==========================================================
# Viva Questions Prompt
# ==========================================================

VIVA_PROMPT = """
Generate viva questions from the document.

Context

{context}

For each question provide

Question

Expected Answer

Generate at least 20 questions.
"""

# ==========================================================
# MCQ Prompt
# ==========================================================

MCQ_PROMPT = """
Generate multiple choice questions.

Context

{context}

For every MCQ provide

Question

Option A

Option B

Option C

Option D

Correct Answer

Explanation

Generate 20 MCQs.
"""

# ==========================================================
# Revision Notes Prompt
# ==========================================================

REVISION_PROMPT = """
Generate one-day revision notes.

Context

{context}

Include

• Most important concepts

• Definitions

• Algorithms

• Formulas

• Key takeaways

Keep the notes concise.

Only use the supplied context.
"""

# ==========================================================
# Cheat Sheet Prompt
# ==========================================================

CHEAT_SHEET_PROMPT = """
Generate a one-page cheat sheet.

Context

{context}

Include

• Keywords

• Definitions

• Algorithms

• Formulae

• Tips

Return concise bullet points.
"""

# ==========================================================
# Mind Map Prompt
# ==========================================================

MINDMAP_PROMPT = """
Generate a hierarchical text-based mind map.

Context

{context}

Example

Topic

├── Concept 1
│   ├── Subtopic
│   └── Subtopic
│
├── Concept 2
│
└── Concept 3

Return only the mind map.
"""

# ==========================================================
# Frequently Asked Questions Prompt
# ==========================================================

FAQ_PROMPT = """
Generate Frequently Asked Questions.

Context

{context}

For each FAQ provide

Question

Answer

Generate at least 15 FAQs.
"""

# ==========================================================
# Exam Preparation Prompt
# ==========================================================

EXAM_PREPARATION_PROMPT = """
You are an AI Exam Preparation Assistant.

Using the following document,

Context

{context}

Prepare exam notes including

• Important Topics

• Frequently Asked Questions

• Long Answer Questions

• Short Answer Questions

• Revision Tips

Only use the supplied context.
"""

# ==========================================================
# Concept Explanation Prompt
# ==========================================================

CONCEPT_EXPLANATION_PROMPT = """
Explain all important concepts from the document.

Context

{context}

For each concept include

• Definition

• Explanation

• Example

• Real-world Application

Only use the supplied context.
"""