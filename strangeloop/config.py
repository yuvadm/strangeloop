"""
Configuration management for Strangeloop.
Uses XDG Base Directory Specification for storing configuration.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for Strangeloop."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_exists()
        self.config = self._load_config()
    
    def _get_config_dir(self) -> Path:
        """
        Get the configuration directory following XDG Base Directory Specification.
        
        Returns:
            Path to the configuration directory
        """
        # Use XDG_CONFIG_HOME if defined, otherwise fallback to ~/.config
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            base_dir = Path(xdg_config_home)
        else:
            base_dir = Path.home() / ".config"
        
        return base_dir / "strangeloop"
    
    def _ensure_config_exists(self) -> None:
        """Ensure the configuration directory and file exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            # Create default config
            default_config = {}
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=2)
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load the configuration from the config file.
        
        Returns:
            The configuration as a dictionary
        """
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Return empty config if file is invalid or doesn't exist
            return {}
    
    def _save_config(self) -> None:
        """Save the current configuration to the config file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: The configuration key
            value: The value to set
        """
        self.config[key] = value
        self._save_config()
    
    def delete(self, key: str) -> bool:
        """
        Delete a configuration value.
        
        Args:
            key: The configuration key
            
        Returns:
            True if key was deleted, False if it didn't exist
        """
        if key in self.config:
            del self.config[key]
            self._save_config()
            return True
        return False
    
    def list_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return dict(self.config)


# Singleton instance
_config_instance = None


def get_config() -> Config:
    """
    Get the singleton Config instance.
    
    Returns:
        The Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
