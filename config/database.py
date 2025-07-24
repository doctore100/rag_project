from typing import List

from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    """
    Handles database connection settings and configuration for both remote PostgresSQL and
    vector-based databases. Includes management of SSH tunneling and vector collection names
    for seamless integration.

    Designed to support secure connections to a remote PostgresSQL database, allowing optional
    local port forwarding via SSH. Also provides support for vector database configurations.

    :ivar remote_db_user: Remote PostgresSQL username.
    :type remote_db_user: String
    :ivar remote_db_password: Remote database password.
    :type remote_db_password: SecretStr
    :ivar remote_db_host: Remote database host.
    :type remote_db_host: String
    :ivar remote_db_port: Remote PostgresSQL port.
    :type remote_db_port: Integer
    :ivar local_bind_port: Local port bound to the remote database for SSH forwarding.
    :type local_bind_port: Integer
    :ivar vector_collection: Name(s) of the vector collections.
    :type vector_collection: List[float]
    :ivar remote_vector_collection_name: Remote database name.
    :type remote_vector_collection_name: String
    """
    # 🗄️ Remote PostgresSQL configuration
    remote_db_user: str = Field(default="postgres", description="Remote PostgresSQL username")
    remote_db_password: SecretStr = Field(..., description="Remote database password")
    remote_db_host: str = Field(default="localhost", description="Remote database host")
    remote_db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgresSQL port")

    # 🔀 Local port for SSH forwarding
    local_bind_port: int = Field(default=5433, ge=1, le=65535, description="Local port bound to the remote database")

    # 📦 Vector DB collections
    # Permite múltiples colecciones o un solo nombre
    vector_collection: List[float] = Field(default=[0.0], description="Name(s) of the vector collections")
    remote_vector_collection_name: str = Field(..., description="Remote database name")

    @property
    def vector_db_uri(self) -> str:
        """
        Construye la URI de conexión a la base de datos vectorial a través del túnel SSH.
        Se conecta al `localhost` localmente redirigido por el túnel a la base de datos remota.
        """
        return (
            f"PostgresSQL://{self.remote_db_user}:"
            f"{self.remote_db_password.get_secret_value()}@"
            f"{self.remote_db_host}:{self.local_bind_port}/"
            f"{self.remote_db_name}"
        )
