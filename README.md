# 📝 LLM-Based Document & Text Summarization System

## 📌 Overview
This project is a local document and text summarization tool that allows users to upload PDF files or paste raw text and generate summaries using a large language model. The application is designed to handle long documents by splitting text into manageable chunks and summarizing them sequentially.

The focus of this project is on controlled LLM inference, document processing, and building a simple user-facing application for summarization tasks.

---

## 🛠 Tools & Technologies
- Python  
- Streamlit  
- LM Studio (local LLM inference)  
- PyPDF2  
- LangChain Text Splitters  
- Requests  

---

## ⚙️ How the System Works
1. The user uploads a PDF file or pastes text into the interface  
2. Text is extracted from the PDF (if provided)  
3. The text is split into overlapping chunks to preserve context  
4. Each chunk is summarized independently using a local LLM  
5. Users can choose the summary length (Short, Normal, Long)  
6. Individual summaries are combined into a final consolidated summary  

---

## 🔍 Key Features
- Supports both PDF uploads and raw text input  
- Chunk-based processing for long documents  
- User-controlled summary length  
- Local LLM inference using LM Studio  
- Clean and minimal Streamlit interface  

---

## 🚀 How to Run the Application

### Install Dependencies
```bash
pip install streamlit PyPDF2 requests langchain-text-splitters
