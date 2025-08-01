from pathlib import Path
from typing import Literal, Optional
from contextlib import contextmanager

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sshtunnel import SSHTunnelForwarder

from .database import DatabaseSettings
from .model_configuration import ModelConfiguration
from .ssh_connection import SSHConnection


class Settings(BaseSettings):
    # General Settings
    app_name: str = Field(default="Mi Proyecto", description="Nombre de la aplicación")
    version: str = Field(default="0.0.1", description="Versión")
    environment: Literal["development", "testing", "production"] = Field(
        default="development",
        description="Environment type",
    )
    debug: bool = Field(default=False)
    tunnel: Optional[SSHTunnelForwarder] = None

    # Module-specific configurations
    model: ModelConfiguration
    database: DatabaseSettings
    ssh_connection: SSHConnection

    # Pydantic Settings Model Configuration
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
        case_sensitive=False
    )

    @classmethod
    @field_validator("environment")
    def validate_environment(cls, env_type):
        allowed = ["development", "testing", "production"]
        if env_type.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return env_type.lower()

    @property
    def ssh_connection_string(self) -> str:
        if self.environment == "development":
            return f"postgresql+psycopg://{self.database.db_user}:{self.database.db_password}@{self.database.db_host}:{self.ssh_connection.local_bind_port}/{self.database.collection_name}"
        return f"sqlite:///test_{self.database.collection_name}.db"

    def start_ssh_tunnel(self):
        try:
            self.tunnel = SSHTunnelForwarder(
                ssh_address_or_host=(self.ssh_connection.host_name, self.ssh_connection.port),
                remote_bind_address=("127.0.0.1", self.ssh_connection.db_port),
                local_bind_address=("localhost", self.ssh_connection.local_bind_port),
                allow_agent=True,
            )
            self.tunnel.start()

            yield self.tunnel

        except Exception as e:
            print(f"✗ Error en túnel SSH: {e}")
            self.tunnel.stop()
            raise

    def shutdown_ssh_tunnel(self):
        if hasattr(self, 'tunnel') and self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            print("✓ Túnel SSH cerrado")

    @classmethod
    def from_env_file(cls, env_file: Path | None = None):
        """Factory method para crear Settings con archivo .env específico"""
        if env_file:
            return cls(_env_file=env_file)
        return cls()
