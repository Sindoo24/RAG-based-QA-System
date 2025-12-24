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


<img width="1920" height="1032" alt="Screenshot 2025-12-24 155704" src="https://github.com/user-attachments/assets/9229c57e-1b03-4037-a38a-17320eab1abb" />

<img width="1920" height="1032" alt="Screenshot 2025-12-24 155515" src="https://github.com/user-attachments/assets/cbbffb10-9fe8-45c9-8a2c-7714f378b9ea" />

-Upload a PDF document via the sidebar

-Document is ingested and indexed once

-Ask questions in the chat interface

-View answers with citations

-Optionally summarize answers for quick insights

## 🚀 Installation

###  Clone the Repository

```bash
git clone https://github.com/Sindoo24/RAG-based-QA-System
cd  RAG-based-QA-System

###  Install Dependencies
Use pip to install all necessary libraries listed in the requirements file.

pip install -r requirements.txt


