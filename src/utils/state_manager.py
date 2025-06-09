import os
import pickle
from typing import Optional
from src.utils.models import FileSystemNode

class StateManager:
    STATE_FILE = os.path.expanduser("~/.inmemory_fs_state.pkl")

    @staticmethod
    def save_state(root_node: FileSystemNode) -> None:
        """Save filesystem state to disk"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(StateManager.STATE_FILE), exist_ok=True)
            with open(StateManager.STATE_FILE, 'wb') as f:
                pickle.dump(root_node, f)
        except Exception as e:
            raise Exception(f"Failed to save state: {str(e)}")

    @staticmethod
    def load_state() -> Optional[FileSystemNode]:
        """Load filesystem state from disk"""
        try:
            with open(StateManager.STATE_FILE, 'rb') as f:
                root = pickle.load(f)
            return root
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Failed to load state: {str(e)}") 