"""
File: backend/prompts/compare_prompts.py

Prompt templates used by the Paper Comparison Service.
"""

# ==========================================================
# Research Paper Comparison Prompt
# ==========================================================

COMPARE_PROMPT = """
You are an expert AI Research Assistant.

Your task is to compare multiple research papers using ONLY
the provided document context.

==========================================================
PAPER 1

{paper_1}

==========================================================
PAPER 2

{paper_2}

==========================================================

Generate a comprehensive comparison using the following
structure.

# Executive Comparison

Provide a brief overview comparing both papers.

----------------------------------------------------------

# Research Objective

Compare

• Problem Statement

• Motivation

• Research Goal

----------------------------------------------------------

# Methodology Comparison

Compare

• Algorithms

• Architecture

• Workflow

• Framework

----------------------------------------------------------

# Dataset Comparison

Compare

• Dataset Used

• Dataset Size

• Data Collection

• Preprocessing

----------------------------------------------------------

# Model Comparison

Compare

• Machine Learning Models

• Deep Learning Models

• LLMs (if applicable)

----------------------------------------------------------

# Experimental Setup

Compare

• Hardware

• Software

• Hyperparameters

• Training Strategy

----------------------------------------------------------

# Evaluation Metrics

Compare metrics such as

• Accuracy

• Precision

• Recall

• F1 Score

• BLEU

• ROUGE

• IoU

• mAP

(if available)

----------------------------------------------------------

# Results Comparison

Compare

• Performance

• Improvements

• Benchmark Results

----------------------------------------------------------

# Advantages

Create a comparison table.

----------------------------------------------------------

# Limitations

Create a comparison table.

----------------------------------------------------------

# Future Work

Compare future research directions.

----------------------------------------------------------

# Final Conclusion

Explain

• Which paper performs better?

• In which scenarios?

• Which approach is more practical?

Only use the supplied context.

Do NOT hallucinate.
"""

# ==========================================================
# Similarities Prompt
# ==========================================================

SIMILARITIES_PROMPT = """
Compare the following two research papers.

Paper 1

{paper_1}

Paper 2

{paper_2}

Identify ONLY the similarities.

Include

• Objective

• Dataset

• Algorithm

• Methodology

• Results

Return bullet points.
"""

# ==========================================================
# Differences Prompt
# ==========================================================

DIFFERENCES_PROMPT = """
Compare the following papers.

Paper 1

{paper_1}

Paper 2

{paper_2}

Identify ONLY the differences.

Return them in bullet points.
"""

# ==========================================================
# Methodology Comparison Prompt
# ==========================================================

METHODOLOGY_COMPARISON_PROMPT = """
Compare only the methodology.

Paper 1

{paper_1}

Paper 2

{paper_2}

Explain

• Architecture

• Workflow

• Models

• Algorithms

• Innovation

Return in table format.
"""

# ==========================================================
# Results Comparison Prompt
# ==========================================================

RESULT_COMPARISON_PROMPT = """
Compare only the experimental results.

Paper 1

{paper_1}

Paper 2

{paper_2}

Return

• Metrics

• Improvements

• Accuracy

• Performance

• Strengths

• Weaknesses

Return as a comparison table.
"""

# ==========================================================
# Advantages & Limitations Prompt
# ==========================================================

ADVANTAGES_LIMITATIONS_PROMPT = """
Analyze the following research papers.

Paper 1

{paper_1}

Paper 2

{paper_2}

Generate

# Advantages

Paper 1

Paper 2

--------------------------

# Limitations

Paper 1

Paper 2

Return using markdown tables.
"""

# ==========================================================
# Best Paper Prompt
# ==========================================================

BEST_PAPER_PROMPT = """
Compare the following papers.

Paper 1

{paper_1}

Paper 2

{paper_2}

Based ONLY on the provided information,

determine

• Which paper is better?

• Why?

• Which problem does each paper solve best?

Do not hallucinate.

Justify every conclusion using the supplied context.
"""

# ==========================================================
# Technical Comparison Prompt
# ==========================================================

TECHNICAL_COMPARISON_PROMPT = """
You are a Senior AI Research Engineer.

Perform a technical comparison between the following papers.

Paper 1

{paper_1}

Paper 2

{paper_2}

Compare

• Architecture

• Algorithms

• Computational Complexity

• Scalability

• Dataset

• Performance

• Practical Usage

• Limitations

Return a professional comparison report.
"""

# ==========================================================
# Comparison Table Prompt
# ==========================================================

COMPARISON_TABLE_PROMPT = """
Create a professional markdown comparison table.

Paper 1

{paper_1}

Paper 2

{paper_2}

The table should include:

| Feature | Paper 1 | Paper 2 |

Include

• Objective

• Dataset

• Algorithm

• Model

• Accuracy

• Advantages

• Limitations

• Future Work
"""