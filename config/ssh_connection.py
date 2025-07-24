from pydantic import BaseModel, Field, SecretStr


class SSHConnection(BaseModel):
    """
    Provides configuration and management for an SSH connection.

    This class is designed to encapsulate the details required for an
    authenticated SSH connection to a remote server. It includes host
    information, authentication details, and port numbers. Instances
    of this class can be used to establish and manage secure SSH
    tunnels.

    :ivar host: The hostname or IP address of the remote server.
    :type host: str
    :ivar port: SSH port, default is 22. Must be between 1 and 65535.
    :type port: int
    :ivar username: The username to use for authentication, default
        is "admin".
    :type username: str
    :ivar password: The password to use for authentication, default
        is "admin".
    :type password: SecretStr
    """
    # 🛡️ SSH Tunnel configuration
    host: str = Field(..., description="The hostname or IP address of the remote server.")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")
    username: str = Field(default="admin", description="The username to use for authentication.")
    password: SecretStr = Field(default="admin", description="The password to use for authentication.")