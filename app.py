import os
import numpy as np
import streamlit as st
from pypdf import PdfReader
from pymongo import MongoClient
import cohere
import google.generativeai as genai

# ── CONFIG ──────────────────────────────────────────────
USER           = os.getenv("USER", "Diego Medina")
CLUSTER_NAME   = "Cluster0"
MONGO_URI      = os.getenv("MONGO_URI",
    "mongodb+srv://rodie916:rodie916@cluster0.idqgg3d.mongodb.net/?retryWrites=true&w=majority")
DB_NAME        = "examenfinal"
COLLECTION     = "documentos"
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "pQBOWaV7omhaA2ghHqZuBytVeRCX48Nyzq5Ng1WQ")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6JsfQlSgr7Cdf8DlGzSMEvz9fmA7NT3PqU5Tq5LtJ9sLw")
EMBED_MODEL    = "embed-multilingual-v3.0"
CHAT_MODEL     = "gemini-1.5-flash"
TOP_K          = 3
# ────────────────────────────────────────────────────────

@st.cache_resource
def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION]

@st.cache_resource
def get_cohere_client():
    return cohere.Client(COHERE_API_KEY)

@st.cache_resource
def get_gemini_model():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(CHAT_MODEL)

def leer_pdf(archivo):
    lector = PdfReader(archivo)
    texto = ""
    for pagina in lector.pages:
        texto += (pagina.extract_text() or "") + "\n"
    return texto

def trocear(texto, tam=500):
    palabras = texto.split()
    chunks, actual = [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 <= tam:
            actual += " " + p
        else:
            chunks.append(actual.strip())
            actual = p
    if actual.strip():
        chunks.append(actual.strip())
    return [c for c in chunks if c]

def embed(textos, tipo):
    co = get_cohere_client()
    resp = co.embed(texts=textos, model=EMBED_MODEL, input_type=tipo)
    return resp.embeddings

def coseno(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

# ── INTERFAZ ─────────────────────────────────────────────
st.title("Buscador de PDFs - Diego Medina")
st.caption(f"Usuario: {USER}  ·  Clúster: {CLUSTER_NAME}")

col = get_mongo_collection()
tab_carga, tab_chat = st.tabs(["Cargar PDF", "Chatbot"])

with tab_carga:
    st.subheader("Sube un PDF")
    pdf = st.file_uploader("Selecciona un PDF", type="pdf")
    if pdf and st.button("Procesar y guardar"):
        with st.spinner("Procesando..."):
            texto   = leer_pdf(pdf)
            chunks  = trocear(texto)
            vectores = embed(chunks, tipo="search_document")
            docs = [
                {"user": USER, "archivo": pdf.name, "texto": c, "embedding": v}
                for c, v in zip(chunks, vectores)
            ]
            col.delete_many({"archivo": pdf.name})
            col.insert_many(docs)
        st.success(f"Guardados {len(docs)} fragmentos de '{pdf.name}' en MongoDB.")

with tab_chat:
    st.subheader("Pregunta sobre el PDF")
    pregunta = st.text_input("Tu pregunta:")
    if pregunta and st.button("Preguntar"):
        with st.spinner("Buscando respuesta..."):
            v_preg = embed([pregunta], tipo="search_query")[0]
            candidatos = list(col.find({"user": USER}))
            if not candidatos:
                st.warning("Primero carga un PDF.")
                st.stop()
            ranking = sorted(
                candidatos,
                key=lambda d: coseno(v_preg, d["embedding"]),
                reverse=True
            )[:TOP_K]
            contexto = "\n---\n".join(d["texto"] for d in ranking)
            prompt = (
                "Responde usando SOLO este contexto.\n\n"
                f"CONTEXTO:\n{contexto}\n\n"
                f"PREGUNTA: {pregunta}\n\nRESPUESTA:"
            )
            respuesta = get_gemini_model().generate_content(prompt).text
        st.markdown("**Respuesta:**")
        st.write(respuesta)
        with st.expander("Ver contexto"):
            st.write(contexto)
