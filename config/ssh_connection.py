from pydantic import BaseModel, Field, SecretStr


class SSHConnection(BaseModel):
    """
    Manages SSH connections for tunneling database connections.

    Provides functionality to configure and manage an SSH tunnel to a remote
    server, facilitating secure access to a remote database. The purpose of
    this class is to abstract the SSH configuration requirements and enable
    seamless integration within applications requiring SSH tunneling.

    :ivar host_name: The hostname or IP address of the remote server.
    :type host_name: str
    :ivar port: SSH port of the remote server.
    :type port: int
    :ivar username: The username to use for authentication.
    :type username: str
    :ivar db_port: Remote PostgreSQL port for the SSH tunnel.
    :type db_port: int
    :ivar local_bind_port: Local port bound to the remote database.
    :type local_bind_port: int
    """
    # 🛡️ SSH Tunnel configuration
    host_name: str = Field(..., description="The hostname or IP address of the remote server.")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")

    username: str = Field(default="admin", description="The username to use for authentication.")
    db_port: int = Field(default=5432, ge=1, le=65535, description="Remote PostgresSQL port for SSH tunnel")

    # 🔀 Local port for SSH forwarding
    local_bind_port: int = Field(default=5433, ge=1, le=65535, description="Local port bound to the remote database")

