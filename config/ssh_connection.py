from contextlib import contextmanager

from pydantic import BaseModel, Field, SecretStr
from sshtunnel import SSHTunnelForwarder


class SSHConnection(BaseModel):
    """
    Represents an SSH connection configuration model.

    This class is used to define and validate the configurations required
    to establish an SSH connection to a remote server. The configuration
    includes details such as hostname, port, username, and password.

    :ivar host: The hostname or IP address of the remote server.
    :type host: String
    :ivar port: The SSH port number for the connection.
    :type port: Int
    :ivar username: The username to use for authentication.
    :type username: String
    :ivar password: The password to use for authentication. The password
        is stored as a secret for enhanced security.
    :type password: SecretStr
    """
    # 🛡️ SSH Tunnel configuration
    host_name: str = Field(..., description="The hostname or IP address of the remote server.")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")

    username: str = Field(default="admin", description="The username to use for authentication.")
    db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgresSQL port for SSH tunnel")

    # 🔀 Local port for SSH forwarding
    local_bind_port: int = Field(default=5433, ge=1, le=65535, description="Local port bound to the remote database")

