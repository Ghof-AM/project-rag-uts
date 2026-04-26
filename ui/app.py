import streamlit as st
from src.query import query_rag
from src.indexing import index_documents
from pathlib import Path

st.set_page_config(page_title="RAG UTS — From Scratch", page_icon="🔍", layout="wide")

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan")

    model_name = st.selectbox(
        "Model Ollama",
        ["llama3.1:8b", "qwen2.5:3b", "mistral:7b"],
        index=0
    )
    k = st.slider("Top-K dokumen relevan", min_value=3, max_value=10, value=5)

    st.divider()
    st.subheader("📁 Indexing Dokumen")
    chunk_size    = st.number_input("Chunk Size",    value=1000, step=100)
    chunk_overlap = st.number_input("Chunk Overlap", value=200,  step=50)

    if st.button("🔄 Jalankan Indexing", use_container_width=True):
        with st.spinner("Memproses dokumen..."):
            try:
                index_documents(int(chunk_size), int(chunk_overlap))
                st.success("✅ Indexing selesai!")
            except Exception as e:
                st.error(f"❌ {e}")

    # Cek status index
    index_exists = Path("faiss_index.index").exists()
    st.divider()
    if index_exists:
        st.success("✅ Index tersedia")
    else:
        st.warning("⚠️ Index belum dibuat")

# ── MAIN UI ──────────────────────────────────────────────────────────────────
st.title("RAG-System UTS")
st.caption("Semantic Search · BM25 Hybrid · Multi-turn Chat · Sumber Dokumen Lokal")

# Inisialisasi chat history
if "messages"    not in st.session_state:
    st.session_state.messages    = []
if "raw_history" not in st.session_state:
    st.session_state.raw_history = []  # untuk dikirim ke LLM

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"📄 Sumber: {', '.join(msg['sources'])}")

# Input pengguna
if prompt := st.chat_input("Tanyakan sesuatu tentang dokumen..."):
    if not Path("faiss_index.index").exists():
        st.error("❌ Jalankan Indexing dulu dari sidebar!")
        st.stop()

    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate jawaban
    with st.chat_message("assistant"):
        with st.spinner("Mencari di dokumen..."):
            result = query_rag(
                prompt,
                k=k,
                chat_history=st.session_state.raw_history,
                model_name=model_name
            )

        st.markdown(result["answer"])
        st.caption(f"📄 Sumber: {', '.join(result['sources'])}")

        with st.expander("🔍 Lihat chunks yang digunakan"):
            for i, (chunk, score) in enumerate(
                zip(result["chunks_used"], result["scores"]), 1
            ):
                st.markdown(f"**Chunk {i}** (skor: {score})")
                st.text(chunk)

    # Simpan ke history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })
    st.session_state.raw_history.append({"role": "user",      "content": prompt})
    st.session_state.raw_history.append({"role": "assistant", "content": result["answer"]})