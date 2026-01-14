# shared/config.py

"""
Configuration module for shared settings.
Includes configurations for PyBot, Pytasker, and other modules.
"""


class SharedConfig:
    """
    A class to manage shared configuration settings.
    Includes configurations for PyBot, Pytasker, and other modules.
    """

    def __init__(self):
        """
        Initialize the SharedConfig instance.
        """
        self.settings = {
            "BOT_NAME": "PynanceBot",
            "SECRET_KEY": None,
            "DATABASE_URL": None,
            "DEBUG": False,
        }

    def set_setting(self, key: str, value):
        """
        Set a configuration setting.

        Args:
            key (str): The key for the setting.
            value: The value to store for the setting.
        """
        self.settings[key] = value

    def get_setting(self, key: str):
        """
        Retrieve a configuration setting.

        Args:
            key (str): The key for the setting.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        return self.settings.get(key)

    def load_pybot_config(self):
        """
        Load PyBot-specific configurations.
        """
        import os

        from dotenv import load_dotenv

        load_dotenv()

        self.settings["BOT_NAME"] = os.getenv("BOT_NAME", "PynanceBot")
        self.settings["SECRET_KEY"] = os.getenv("SECRET_KEY")
        if not self.settings["SECRET_KEY"]:
            import secrets

            self.settings["SECRET_KEY"] = secrets.token_hex(32)
            print(
                f"WARNING: SECRET_KEY not set in environment. Using a temporary key: {self.settings['SECRET_KEY']}"
            )
            print(
                "Please set a secure SECRET_KEY in your environment variables for production."
            )

        self.settings["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() in (
            "true",
            "1",
            "yes",
        )
        if not self.settings["DEBUG"]:
            print("DEBUG mode is disabled. Set FLASK_DEBUG=true to enable.")

        self.settings["DATABASE_URL"] = os.getenv("DATABASE_URL")
        if not self.settings["DATABASE_URL"]:
            db_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "pynance_users.db"
            )
            self.settings["DATABASE_URL"] = f"sqlite:///{db_path}"
