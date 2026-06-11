import uuid
from typing import Dict, Any, List

class Question:
    def __init__(self, text: str, options: List[str], correct_answer: str, 
                 difficulty: str = "medium", category: str = "General", question_id: str = None):
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
        return self._options.copy()
    
    @property
    def difficulty(self) -> str:
        return self._difficulty
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def correct_answer(self) -> str:
        return self._correct_answer
    
    @property
    def times_asked(self) -> int:
        return self._times_asked
    
    @property
    def times_correct(self) -> int:
        return self._times_correct
    
    def check_answer(self, answer: str) -> bool:
        self._times_asked += 1
        is_correct = answer.strip().lower() == self._correct_answer.strip().lower()
        if is_correct:
            self._times_correct += 1
        return is_correct
    
    def get_points(self) -> int:
        points_map = {"easy": 10, "medium": 20, "hard": 30}
        return points_map.get(self._difficulty, 10)
    
    def to_dict(self) -> Dict[str, Any]:
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
        return f"Question({self._text[:50]}...)"