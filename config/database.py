from typing import List

from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    """
    Manages database configuration settings required to connect to a remote PostgreSQL server and organize vector
    collections.

    This class defines several fields to configure the details needed to connect to a remote PostgreSQL database, such as
    username, password, host, database name, and port. In addition, it allows specifying details regarding vector collections
    in the database.

    :ivar db_user: Remote PostgresSQL username.
    :type db_user: Str
    :ivar db_password: Remote database password.
    :type db_password: SecretStr
    :ivar db_host: Remote database host.
    :type db_host: Str
    :ivar db_name: Remote database name.
    :type db_name: str
    :ivar vector_collection: Name(s) of the vector collections.
    :type vector_collection: List[float]
    :ivar collection_name: Remote database name.
    :type collection_name: str
    :ivar db_port: Remote PostgresSQL port for an SSH tunnel. Must be between 1 and 65535.
    :type db_port: int
    """
    # 🗄️ Remote PostgresSQL configuration
    db_user: str = Field(default="postgres", description="Remote PostgresSQL username")
    db_password: SecretStr = Field(..., description="Remote database password")
    db_host: str = Field(default="localhost", description="Remote database host")
    db_name:str = Field(default="postgres", description="Remote database name")


    # 📦 Vector DB collections
    # Permite múltiples colecciones o un solo nombre
    collection_name: str = Field(..., description="Remote database name")
    db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgresSQL port for SSH tunnel")


