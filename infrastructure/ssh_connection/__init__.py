from config import create_settings as s
from sshtunnel import SSHTunnelForwarder
from typing import Optional

class SSHConnectionManager:
    def __init__(self):
        self.settings = s()
    tunnel: Optional[SSHTunnelForwarder] = None

    def start_ssh_tunnel(self):
        try:
            self.tunnel = SSHTunnelForwarder(
                ssh_address_or_host=(self.settings.ssh_connection.host_name, self.settings.ssh_connection.port),
                remote_bind_address=("127.0.0.1", self.settings.database.db_port),
                local_bind_address=("localhost", self.settings.ssh_connection.local_bind_port),
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