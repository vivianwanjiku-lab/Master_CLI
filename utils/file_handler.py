import json
import os
from typing import Dict, Any, List, Optional

class FileHandler:
    DATA_DIR = "data"
    
    def __init__(self):
        self._ensure_data_dir()
        self._files = {
            "users": os.path.join(self.DATA_DIR, "users.json"),
            "quizzes": os.path.join(self.DATA_DIR, "quizzes.json"),
            "questions": os.path.join(self.DATA_DIR, "questions.json")
        }
        self._initialize_empty_files()
    
    def _ensure_data_dir(self) -> None:
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
    
    def _initialize_empty_files(self) -> None:
        for filepath in self._files.values():
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=4)
    
    def save_data(self, data_type: str, data: Dict[str, Any]) -> bool:
        if data_type not in self._files:
            return False
        try:
            with open(self._files[data_type], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving {data_type}: {e}")
            return False
    
    def load_data(self, data_type: str) -> Dict[str, Any]:
        if data_type not in self._files:
            return {}
        filepath = self._files[data_type]
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading {data_type}: {e}")
            return {}
    
    def save_item(self, data_type: str, item_id: str, item_data: Dict[str, Any]) -> bool:
        data = self.load_data(data_type)
        data[item_id] = item_data
        return self.save_data(data_type, data)
    
    def get_item(self, data_type: str, item_id: str) -> Optional[Dict[str, Any]]:
        data = self.load_data(data_type)
        return data.get(item_id)
    
    def delete_item(self, data_type: str, item_id: str) -> bool:
        data = self.load_data(data_type)
        if item_id in data:
            del data[item_id]
            return self.save_data(data_type, data)
        return False