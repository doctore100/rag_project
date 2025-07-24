from typing import List

from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    """
    Configuration for database settings with functionalities for SSH tunneling and remote database connection.

    This class encapsulates all configurations related to establishing an SSH tunnel, connecting to
    a remote PostgreSQL database, and binding a local port for forwarding. It also manages vector database
    collection configurations and provides derived properties for database connectivity.

    :ivar ssh_host_name: SSH alias or hostname.
    :type ssh_host_name: str
    :ivar ssh_host_port: SSH port number, must be between 1 and 65535.
    :type ssh_host_port: int
    :ivar remote_db_user: Remote PostgreSQL username.
    :type remote_db_user: str
    :ivar remote_db_password: Remote database password.
    :type remote_db_password: SecretStr
    :ivar remote_db_name: Remote database name.
    :type remote_db_name: str
    :ivar remote_db_host: Remote database host.
    :type remote_db_host: str
    :ivar remote_db_port: Remote PostgreSQL port number, must be between 1 and 65535.
    :type remote_db_port: int
    :ivar local_bind_port: Local port for SSH forwarding, must be between 1 and 65535.
    :type local_bind_port: int
    :ivar vector_collection_names: Names of vector database collections.
    :type vector_collection_names: List[str]
    """

    # 🗄️ Remote PostgresSQL configuration
    remote_db_user: str = Field(default="postgres", description="Remote PostgreSQL username")
    remote_db_password: SecretStr = Field(..., description="Remote database password")
    remote_db_name: str = Field(..., description="Remote database name")
    remote_db_host: str = Field(default="localhost", description="Remote database host")
    remote_db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgreSQL port")

    # 🔀 Local port for SSH forwarding
    local_bind_port: int = Field(default=5433, ge=1, le=65535, description="Local port bound to the remote database")

    # 📦 Vector DB collections
    # Permite múltiples colecciones o un solo nombre
    vector_collection_names: List[str] = Field(..., description="Name(s) of the vector collections")

    @property
    def vector_db_uri(self) -> str:
        """
        Construye la URI de conexión a la base de datos vectorial a través del túnel SSH.
        Se conecta al `localhost` localmente redirigido por el túnel a la base de datos remota.
        """
        return (
            f"postgresql://{self.remote_db_user}:"
            f"{self.remote_db_password.get_secret_value()}@"
            f"{self.remote_db_host}:{self.local_bind_port}/"
            f"{self.remote_db_name}"
        )
