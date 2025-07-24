from pydantic import BaseModel, Field, SecretStr


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
    host: str = Field(..., description="The hostname or IP address of the remote server.", alias="SSH_HOST")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port", alias="SSH_PORT")
    # Use this if you haven't configured an SSH alias and need to connect using a username and password
    username: str = Field(default="admin", description="The username to use for authentication.")
    password: SecretStr = Field(default="admin", description="The password to use for authentication.")