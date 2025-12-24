# RAG-based-QA-System
Multi Modal RAG-Built using Streamlit, ChromaDB, and Qwen 4B (LM Studio).

A production-ready Multi-Modal Retrieval-Augmented Generation (RAG) system that enables question answering over complex documents such as financial and policy reports containing text, tables, and scanned images.

# Problem Statement

Real-world documents are rarely plain text. They often contain:

-Long narrative sections

-Structured tables

-Figures and scanned content

-Footnotes and metadata

Traditional QA systems struggle to reason over such heterogeneous information.
This project addresses the challenge by combining document parsing, semantic retrieval, and LLM-based generation into a unified, explainable pipeline.

# Workflow

-Upload a PDF document via the sidebar

-Document is ingested and indexed once

-Ask questions in the chat interface

-View answers with citations

-Optionally summarize answers for quick insights

