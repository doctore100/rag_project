from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import create_settings
from infrastructure import DatabaseManager, SSHConnectionManager

settings = create_settings()


def main():
    # leer el documento
    file_path_doc = "nke_10k_2023.pdf"
    loader = PyPDFLoader(file_path_doc)
    documents = loader.load()  # esto es una lista de páginas del documento
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    # chunks = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model=settings.model.embedding_name, api_key=settings.model.api_key)
    #
    manage_db = DatabaseManager(embeddings)

    tunnel = SSHConnectionManager()
    try:
        tunnel_generator = tunnel.start_ssh_tunnel()
        tunnel = next(tunnel_generator)
        if tunnel.is_active:
            print("Tunnel is active")
            # manage_db.create_vector_db_if_not_exist()
            # manage_db.enable_pgvector_extension()
            vector_store = manage_db.initialize_vector_store()

            # Aquí puedes seguir usando vector_store
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always try to clean up the tunnel
        if tunnel and hasattr(settings, 'shutdown_ssh_tunnel'):
            settings.shutdown_ssh_tunnel()


if __name__ == "__main__":
    main()