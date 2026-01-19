import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests

# LM Studio server API
CHAT_URL = "http://localhost:1234/v1/chat/completions"

# --- Streamlit Layout ---
st.title("📄 Local PDF & Text Summarizer")
st.write("Summarize long text or PDFs using LM Studio models like Phi-3 or Gemma.")

summary_type = st.selectbox(
    "Choose Summary Length",
    ["Short", "Normal", "Long"]
)

uploaded_pdf = st.file_uploader("Upload PDF (optional)", type="pdf")
text_input = st.text_area("Or paste text here:", height=250)

if uploaded_pdf:
    st.success(f"📁 Uploaded PDF: {uploaded_pdf.name}")


# --- Text chunking function ---
def chunk_text(text, size=2500, overlap=250):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )
    return splitter.split_text(text)


# --- Summarizer function ---
def summarize_chunk(chunk, style):
    styles = {
        "Short": "Summarize in 4-5 bullet points.",
        "Normal": "Summarize in one medium paragraph.",
        "Long": "Summarize in detail with key points and insights."
    }

    response = requests.post(
        CHAT_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": "phi-3-mini-4k-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"{styles[style]}\n\nText:\n{chunk}"
                }
            ],
            "temperature": 0.2
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error: {response.text}"


# --- Summarize Action ---
if st.button("✨ Summarize Now"):
    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        full_text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                full_text += extracted
    else:
        full_text = text_input

    if not full_text.strip():
        st.warning("Please upload a PDF or enter text to summarize.")
    else:
        st.info("Splitting the content into parts...")
        chunks = chunk_text(full_text)
        st.success(f"📌 Text split into {len(chunks)} chunks")

        st.info("Generating summary...")
        final_summary = ""

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, chunk in enumerate(chunks):
            status_text.text(f"⏳ Summarizing chunk {i+1}/{len(chunks)}...")
            part = summarize_chunk(chunk, summary_type)
            final_summary += part + "\n\n"
            progress_bar.progress((i + 1) / len(chunks))

        status_text.text("✔ Summary completed!")
        progress_bar.progress(1.0)

        st.subheader("📝 Final Summary")
        st.write(final_summary)
