from config import create_settings as s
from langchain_postgres.vectorstores import PGVector


class LangChainVectorDatabase:
    def __init__(self,model_embeddings,collection_name: str = None, ):
        self.settings = s()
        self.collection_name = collection_name
        self.embeddings = model_embeddings
        self.vector_store = None
    """
    PRIMERO --> Crear la base de datos se debe inicializar el modelo de embeddings  para soporte de vector
    con el comando CREATE EXTENSION IF NOT EXISTS vector; es un metodo privado que implemente esta funcionalidad
    antes de inicializar PGVector

    """

    @property
    def ssh_connection_string(self) -> str:
        if self.environment == "development":
            return f"postgresql+psycopg://{self.database.db_user}:{self.database.db_password}@{self.database.db_host}:{self.ssh_connection.local_bind_port}/{self.database.collection_name}"
        return f"sqlite:///test_{self.database.collection_name}.db"
    def __create_vector_db_if_not_exist(self):
        pass
    def initialize_vector_store(self, pre_delete_collection: bool = True):
        """
        Initializes the vector store using the provided configuration and connection
        parameters. The method sets up a PGVector instance for storing embeddings along
        with metadata. This setup allows for managing the collection of vectorized
        data optimized for semantic searching and retrieval.

        If `pre_delete_collection` is set to True, it will attempt to delete the
        existing collection before proceeding with initialization.

        :param pre_delete_collection: Boolean flag to determine if the existing
            collection should be deleted before initialization.
        :return: Returns the initialized PGVector instance if successful, or `False`
            in case of failure.
        """
        if not self.embeddings:
            raise ValueError("Debe inicializar embeddings primero")

        try:
            self.vector_store = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name if self.collection_name else self.settings.database.collection_name,
                connection=self.settings.ssh_connection_string,
                use_jsonb=pre_delete_collection,  # Usar JSONB para metadatos
                pre_delete_collection=pre_delete_collection
            )
            print(f"✓ Vector store inicializado: colección '{self.collection_name}'")
            return self.vector_store
        except Exception as e:
            print(f"✗ Error inicializando vector store: {e}")
            return False

