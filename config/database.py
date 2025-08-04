from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    """
    Configuration settings for remote PostgreSQL and vector database collections.

    This class provides the configuration parameters required to define the
    properties for connecting to a remote PostgreSQL database and settings
    related to vector database collections. These configurations allow for
    managing and storing data in the context of a database-backed application.

    :ivar db_user: Username for connecting to the remote PostgreSQL database.
    :type db_user: str
    :ivar db_password: Password for connecting to the remote PostgreSQL database.
    :type db_password: SecretStr
    :ivar db_host: Hostname or IP address of the remote PostgreSQL database.
    :type db_host: str
    :ivar db_name: Name of the remote PostgreSQL database to connect to.
    :type db_name: str
    :ivar db_port: Port number to establish connection to the remote PostgreSQL
        database. Must range between 1 and 65535.
    :type db_port: int
    :ivar collection_name: Name of a specific collection in the vector database.
    :type collection_name: str
    :ivar collection_bb_name: Name of the database dedicated for storing vector
        embeddings.
    :type collection_bb_name: str
    """
    # 🗄️ Remote PostgresSQL configuration
    db_user: str = Field(default="", description="Remote PostgresSQL username")
    db_password: SecretStr = Field(..., description="Remote database password")
    db_host: str = Field(default="localhost", description="Remote database host")
    db_name: str = Field(default="", description="Remote database name")
    db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgresSQL port for SSH tunnel")

    # 📦 Vector DB collections
    # Permite múltiples colecciones o un solo nombre
    # vector_collection: List[float] = Field(default=[0.0], description="Name(s) of the vector collections")
    collection_name: str = Field(..., description="Remote collection name")
    collection_bb_name: str = Field(..., description="Name of database for storing vector embeddings")
