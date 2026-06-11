import re
from typing import Tuple, List

class Validators:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        if not email:
            return False, "Email cannot be empty"
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        if not username:
            return False, "Username cannot be empty"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 20:
            return False, "Username must be at most 20 characters"
        pattern = r'^[a-zA-Z0-9_]+$'
        if re.match(pattern, username):
            return True, ""
        return False, "Username can only contain letters, numbers, and underscores"
    
    @staticmethod
    def validate_difficulty(difficulty: str) -> Tuple[bool, str]:
        valid = ["easy", "medium", "hard"]
        if difficulty.lower() in valid:
            return True, ""
        return False, f"Difficulty must be one of: {', '.join(valid)}"