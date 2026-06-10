"""User model - demonstrates encapsulation and OOP"""

import uuid
from datetime import datetime
from typing import Dict, Any, List


class User:
    """
    User class representing a quiz player.
    Demonstrates encapsulation with private attributes and properties.
    """
    
    def __init__(self, username: str, email: str, user_id: str = None):
        """
        Initialize a new User.
        
        Args:
            username: Unique username
            email: User's email address
            user_id: Optional UUID, generated if not provided
        """
        self._user_id = user_id or str(uuid.uuid4())
        self._username = username
        self._email = email
        self._created_at = datetime.now().isoformat()
        self._quiz_history = []  # List of quiz session IDs
        self._total_score = 0
        self._quizzes_taken = 0
        
    # Properties (encapsulation)
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        if value and len(value) >= 3:
            self._username = value
        else:
            raise ValueError("Username must be at least 3 characters")
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if "@" in value and "." in value:
            self._email = value
        else:
            raise ValueError("Invalid email format")
    
    @property
    def total_score(self) -> int:
        return self._total_score
    
    @property
    def average_score(self) -> float:
        if self._quizzes_taken == 0:
            return 0.0
        return self._total_score / self._quizzes_taken
    
    # Methods
    def add_quiz_result(self, quiz_session_id: str, score: int) -> None:
        """Add a quiz result to user's history"""
        self._quiz_history.append({
            "quiz_id": quiz_session_id,
            "score": score,
            "date": datetime.now().isoformat()
        })
        self._total_score += score
        self._quizzes_taken += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert User to dictionary for JSON serialization"""
        return {
            "user_id": self._user_id,
            "username": self._username,
            "email": self._email,
            "created_at": self._created_at,
            "quiz_history": self._quiz_history,
            "total_score": self._total_score,
            "quizzes_taken": self._quizzes_taken
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User from dictionary"""
        user = cls(
            username=data["username"],
            email=data["email"],
            user_id=data["user_id"]
        )
        user._created_at = data.get("created_at", datetime.now().isoformat())
        user._quiz_history = data.get("quiz_history", [])
        user._total_score = data.get("total_score", 0)
        user._quizzes_taken = data.get("quizzes_taken", 0)
        return user
    
    def __str__(self) -> str:
        return f"User({self._username}, Score: {self._total_score})"
    
    def __repr__(self) -> str:
        return f"User(user_id={self._user_id}, username={self._username})"