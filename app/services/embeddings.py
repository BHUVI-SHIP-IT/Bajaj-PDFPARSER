from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"  # 384-dim
    )

