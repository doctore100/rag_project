from typing import List

from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    """
    Configuration settings for a database connection.

    This class represents settings for connecting to a remote PostgreSQL database,
    with support for SSH forwarding and vector database collections. It allows the
    specification of database credentials, connection details, and relevant
    collection names for efficient database usage.

    :ivar db_user: Remote PostgreSQL username.
    :type db_user: str
    :ivar db_password: Remote database password.
    :type db_password: SecretStr
    :ivar db_host: Remote database host.
    :type db_host: str
    :ivar db_port: Remote PostgreSQL port.
    :type db_port: int
    :ivar local_bind_port: Local port bound to the remote database, for SSH
        forwarding.
    :type local_bind_port: int
    :ivar vector_collection: Name(s) of the vector collections.
    :type vector_collection: List[float]
    :ivar collection_name: Remote database name.
    :type collection_name: str
    """
    # 🗄️ Remote PostgresSQL configuration
    db_user: str = Field(default="postgres", description="Remote PostgresSQL username")
    db_password: SecretStr = Field(..., description="Remote database password")
    db_host: str = Field(default="localhost", description="Remote database host")
    db_name:str = Field(default="postgres", description="Remote database name")


    # 📦 Vector DB collections
    # Permite múltiples colecciones o un solo nombre
    vector_collection: List[float] = Field(default=[0.0], description="Name(s) of the vector collections")
    collection_name: str = Field(..., description="Remote database name")

