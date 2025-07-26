from pathlib import Path
from os import getenv
from .settings import Settings


def create_settings() -> Settings:
    """
    Creates and configures application settings based on the current environment.

    This function determines the root path of the project and reads the
    current environment type (e.g., "development", "production", or
    "testing") from the system's environment variables. Using this value,
    the corresponding `.env` file is selected and used to instantiate the
    Settings object. Additional validations and setup are performed
    depending on the environment (e.g., production validations, logging
    setup).

    :raises ValueError: If required production settings are not satisfied
        when in production mode.

    :return: The constructed Settings for the application.
    :rtype: Settings
    """

    # Project's root directory
    project_root = Path(__file__).resolve().parent

    # Get the ENVIRONMENT system variable directly (with fallback)
    env_value = getenv("ENVIRONMENT", "development").lower()

    #  Match the appropriate .env file
    env_file_map = {
        "development": project_root / ".env.development",
        "production": project_root / ".env.production",
        "testing": project_root / ".env.testing"
    }

    selected_env_file = env_file_map.get(env_value, None)

    # Instanciar Settings usando ese archivo
    environment_settings = Settings.from_env_file(selected_env_file.name) if selected_env_file else Settings.from_env_file()

    # Validaciones y setup
    if environment_settings.environment == "production":
        environment_settings.validate_required_for_production()

    return environment_settings
