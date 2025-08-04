import psycopg
from langchain_postgres.vectorstores import PGVector
from psycopg import OperationalError, Error as PsycopgError
from typing import Optional

from config import create_settings as s


class DatabaseManager:
    def __init__(self, model_embeddings=None, collection_name: str = None):
        self.settings = s()
        self.collection_name = collection_name or self.settings.database.collection_name
        self.embeddings = model_embeddings
        self.vector_store = None

    def _get_connection_params(self, db_name: Optional[str] = None) -> dict:
        return {
            'host': self.settings.database.db_host,
            'port': self.settings.ssh_connection.local_bind_port,
            'dbname': db_name or self.settings.database.db_name,
            'user': self.settings.database.db_user,
            'password': self.settings.database.db_password.get_secret_value(),
            'autocommit': True
        }

    def create_vector_db_if_not_exist(self):
        try:
            with psycopg.connect(**self._get_connection_params()) as conn:
                with conn.cursor() as cur:
                    from psycopg import sql
                    vector_stores_database = self.settings.database.collection_bb_name

                    cur.execute(
                        "SELECT 1 FROM pg_database WHERE datname = %s",
                        (vector_stores_database,)
                    )

                    if not cur.fetchone():
                        cur.execute(
                            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(vector_stores_database))
                        )
                        print(f"✔️ Base de datos '{vector_stores_database}' creada.")
                    else:
                        print(f"ℹ️ La base de datos '{vector_stores_database}' ya existe.")

        except OperationalError as oe:
            print("❌ No se pudo conectar para crear la base de datos:", oe)
            raise
        except PsycopgError as pe:
            print("❌ Error SQL creando la base de datos:", pe)
            raise

    def enable_pgvector_extension(self):
        try:
            with psycopg.connect(**self._get_connection_params(self.settings.database.collection_bb_name)) as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                    print(
                        f"🧠 Extensión 'vector' habilitada en la base de datos: {self.settings.database.collection_bb_name}")
        except OperationalError as oe:
            print("❌ No se pudo conectar para habilitar extensión:", oe)
            raise
        except PsycopgError as pe:
            print("❌ Error SQL habilitando extensión:", pe)
            raise

    def initialize_vector_store(self, pre_delete_collection: bool = True) -> Optional[PGVector]:
        """
        Initializes the vector store using the provided configuration and connection
        parameters. The method sets up a PGVector instance for storing embeddings along
        with metadata. This setup allows for managing the collection of vectorized
        data optimized for semantic searching and retrieval.

        If `pre_delete_collection` is set to True, it will attempt to delete the
        existing collection before proceeding with initialization.

        :param pre_delete_collection: Boolean flag to determine if the existing
            collection should be deleted before initialization.
        :return: Returns the initialized PGVector instance if successful, or None
            in case of failure.
        """
        if not self.embeddings:
            raise ValueError("Debe inicializar embeddings primero")

        try:
            connection_string = f"postgresql+psycopg://{self.settings.database.db_user}:{self.settings.database.db_password.get_secret_value()}@{self.settings.database.db_host}:{self.settings.ssh_connection.local_bind_port}/{self.settings.database.collection_bb_name}"

            self.vector_store = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name,
                connection=connection_string,
                use_jsonb=pre_delete_collection,
                pre_delete_collection=pre_delete_collection
            )
            print(f"✓ Vector store inicializado: colección {self.collection_name}")
            return self.vector_store
        except Exception as e:
            print(f"✗ Error inicializando vector store: {e}")
            return None
