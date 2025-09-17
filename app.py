import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import streamlit as st

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


OLLAMA_HOST = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.2:3b"

st.set_page_config(page_title="Financial Doc Q&A Assistant", layout="wide")
st.title(" Financial Document Q&A")

embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=OLLAMA_HOST)
Settings.embed_model = embed_model
llm = Ollama(model=CHAT_MODEL, base_url=OLLAMA_HOST, request_timeout=600)

if "query_engine" not in st.session_state:
    st.session_state.query_engine = None


with st.sidebar:
    st.markdown("### Upload a single file (PDF / Excel)")
    uf = st.file_uploader("Choose file", type=["pdf","xlsx","xls"], accept_multiple_files=False)

    if uf and st.button("Process file"):
        suffix = Path(uf.name).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uf.read())
            tmp_path = tmp.name

        docs = SimpleDirectoryReader(input_files=[tmp_path]).load_data()
        st.info(f"Loaded {len(docs)} document from {uf.name}")

        index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
        st.session_state.query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)
        st.success("Indexed in memory. Ask your question!")

st.subheader("Ask a question")
q = st.text_input("Question", value="What is the Pre-tax Profit in 2023?")
if st.button("Ask"):
    if st.session_state.query_engine is None:
        st.warning("Please upload & process a file first.")
    else:
        with st.spinner("Thinking locally with Ollama…"):
            resp = st.session_state.query_engine.query(q)

        st.markdown("**Answer**")
        st.write(str(resp))

        with st.expander("Sources used", expanded=False):
            try:
                for i, node in enumerate(resp.source_nodes, 1):
                    meta = node.metadata or {}
                    fname = meta.get("file_name") or meta.get("filename") or meta.get("file_path") or "unknown"
                    score = getattr(node, "score", None)
                    st.markdown(f"**[{i}]** file: {fname} · score: {score if score is not None else 'n/a'}")
                    st.write(node.text[:1200] + ("…" if len(node.text) > 1200 else ""))
            except Exception:
                st.info("No source nodes available.")
