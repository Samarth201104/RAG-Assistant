"""
File: backend/prompts/summarize_prompts.py

Prompt templates used by the Summarization Service.
"""

# ==========================================================
# Research Paper Summary Prompt
# ==========================================================

SUMMARY_PROMPT = """
You are an expert Research Paper Summarization Assistant.

Your task is to summarize the provided research paper context.

===========================
DOCUMENT CONTEXT

{context}

===========================

Generate the response using the following sections.

# Executive Summary

Provide a concise overview of the entire paper in 150–250 words.

------------------------------------------------------------

# Research Objective

Explain:

• What problem does the paper solve?

• Why is the problem important?

------------------------------------------------------------

# Key Findings

List the important discoveries.

Use bullet points.

------------------------------------------------------------

# Methodology

Describe:

• Dataset

• Algorithms

• Models

• Experimental setup

• Evaluation metrics

------------------------------------------------------------

# Results

Summarize the important results reported in the paper.

------------------------------------------------------------

# Advantages

Mention the strengths of the proposed approach.

------------------------------------------------------------

# Limitations

Mention limitations discussed by the authors.

If none are explicitly stated, infer reasonable limitations.

------------------------------------------------------------

# Future Work

Mention future research directions.

------------------------------------------------------------

# Conclusion

Summarize the overall contribution of the paper.

Use professional language.

Do not hallucinate.

Use only the provided context.
"""

# ==========================================================
# Executive Summary Prompt
# ==========================================================

EXECUTIVE_SUMMARY_PROMPT = """
You are an AI Research Assistant.

Generate an executive summary from the following document.

Document Context

{context}

Requirements

• 150–250 words

• Professional language

• Mention the main contribution

• Mention important findings

Return only the executive summary.
"""

# ==========================================================
# Key Findings Prompt
# ==========================================================

KEY_FINDINGS_PROMPT = """
Extract the most important findings from the following document.

Context

{context}

Return 5-10 bullet points.

Only use information from the provided context.
"""

# ==========================================================
# Methodology Prompt
# ==========================================================

METHODOLOGY_PROMPT = """
Analyze the following research paper.

Context

{context}

Describe the methodology in detail.

Include

• Algorithms

• Models

• Dataset

• Training

• Evaluation

Do not invent information.
"""

# ==========================================================
# Limitations Prompt
# ==========================================================

LIMITATIONS_PROMPT = """
Read the following research paper context.

{context}

Identify the limitations.

If limitations are explicitly mentioned,
list them.

Otherwise infer only reasonable limitations
based on the context.

Return bullet points.
"""

# ==========================================================
# Future Work Prompt
# ==========================================================

FUTURE_WORK_PROMPT = """
Read the following research paper.

Context

{context}

Identify possible future work.

Use information from the paper.

If future work is not explicitly mentioned,
infer reasonable research directions.

Return bullet points.
"""

# ==========================================================
# Research Contribution Prompt
# ==========================================================

CONTRIBUTION_PROMPT = """
Analyze the following research paper.

Context

{context}

Answer:

• What is the novel contribution?

• Why is it important?

• How is it different from previous approaches?

Return concise paragraphs.
"""

# ==========================================================
# One-Line Summary Prompt
# ==========================================================

ONE_LINE_SUMMARY_PROMPT = """
Summarize the following research paper in exactly one sentence.

Context

{context}
"""

# ==========================================================
# Abstract Generation Prompt
# ==========================================================

ABSTRACT_PROMPT = """
Generate an abstract using the provided document.

Context

{context}

Length

150-250 words.

Maintain academic writing style.
"""

# ==========================================================
# TLDR Prompt
# ==========================================================

TLDR_PROMPT = """
Generate a TL;DR of the following paper.

Context

{context}

Maximum 50 words.

Only return the TL;DR.
"""