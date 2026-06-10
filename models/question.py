"""Question model - demonstrates inheritance potential"""

import uuid
from typing import Dict, Any, List, Optional


class Question:
    """
    Question class representing a single quiz question.
    Base class that could be extended for different question types.
    """
    
    def __init__(
        self,
        text: str,
        options: List[str],
        correct_answer: str,
        difficulty: str = "medium",
        category: str = "General",
        question_id: str = None
    ):
        """
        Initialize a new Question.
        
        Args:
            text: Question text
            options: List of 4 answer options
            correct_answer: The correct answer (must match one option)
            difficulty: easy, medium, or hard
            category: Question category
            question_id: Optional UUID
        """
        self._question_id = question_id or str(uuid.uuid4())
        self._text = text
        self._options = options
        self._correct_answer = correct_answer
        self._difficulty = difficulty
        self._category = category
        self._times_asked = 0
        self._times_correct = 0
        
    @property
    def question_id(self) -> str:
        return self._question_id
    
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def options(self) -> List[str]:
        return self._options.copy()  # Return copy to prevent modification
    
    @property
    def difficulty(self) -> str:
        return self._difficulty
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate for this question"""
        if self._times_asked == 0:
            return 0.0
        return (self._times_correct / self._times_asked) * 100
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if answer is correct and update stats.
        
        Args:
            answer: User's answer
            
        Returns:
            True if correct, False otherwise
        """
        self._times_asked += 1
        is_correct = answer.strip().lower() == self._correct_answer.strip().lower()
        if is_correct:
            self._times_correct += 1
        return is_correct
    
    def get_points(self) -> int:
        """Calculate points for this question based on difficulty"""
        points_map = {
            "easy": 10,
            "medium": 20,
            "hard": 30
        }
        return points_map.get(self._difficulty, 10)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Question to dictionary for JSON serialization"""
        return {
            "question_id": self._question_id,
            "text": self._text,
            "options": self._options,
            "correct_answer": self._correct_answer,
            "difficulty": self._difficulty,
            "category": self._category,
            "times_asked": self._times_asked,
            "times_correct": self._times_correct
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """Create Question from dictionary"""
        question = cls(
            text=data["text"],
            options=data["options"],
            correct_answer=data["correct_answer"],
            difficulty=data.get("difficulty", "medium"),
            category=data.get("category", "General"),
            question_id=data["question_id"]
        )
        question._times_asked = data.get("times_asked", 0)
        question._times_correct = data.get("times_correct", 0)
        return question
    
    def __str__(self) -> str:
        return f"Question({self._text[:50]}..., {self._difficulty})"
    
    def __repr__(self) -> str:
        return f"Question(question_id={self._question_id}, text={self._text[:30]})"


class TrueFalseQuestion(Question):
    """Inheritance example - True/False question type"""
    
    def __init__(self, text: str, correct_answer: bool, difficulty: str = "medium", category: str = "General"):
        options = ["True", "False"]
        answer = "True" if correct_answer else "False"
        super().__init__(text, options, answer, difficulty, category)
        self._type = "true_false"
    
    @property
    def question_type(self) -> str:
        return self._type


class MultipleChoiceQuestion(Question):
    """Inheritance example - Standard multiple choice"""
    
    def __init__(self, text: str, options: List[str], correct_answer: str, difficulty: str = "medium", category: str = "General"):
        super().__init__(text, options, correct_answer, difficulty, category)
        self._type = "multiple_choice"
    
    @property
    def question_type(self) -> str:
        return self._type