"""QuizSession model - manages a quiz session"""

import uuid
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from models.question import Question


class QuizSession:
    """
    QuizSession class managing a complete quiz game.
    Demonstrates composition (has-a relationship with Question).
    """
    
    def __init__(
        self,
        user_id: str,
        questions: List[Question],
        difficulty: str = None,
        session_id: str = None
    ):
        """
        Initialize a new Quiz Session.
        
        Args:
            user_id: ID of user taking the quiz
            questions: List of Question objects
            difficulty: Filter by difficulty (optional)
            session_id: Optional UUID
        """
        self._session_id = session_id or str(uuid.uuid4())
        self._user_id = user_id
        self._difficulty = difficulty
        
        # Filter questions by difficulty if specified
        if difficulty:
            self._questions = [q for q in questions if q.difficulty == difficulty]
        else:
            self._questions = questions.copy()
        
        # Shuffle questions for variety
        random.shuffle(self._questions)
        
        self._current_question_index = 0
        self._score = 0
        self._answers = []  # List of (question_id, user_answer, is_correct)
        self._start_time = None
        self._end_time = None
        self._status = "not_started"  # not_started, in_progress, completed
        
    @property
    def session_id(self) -> str:
        return self._session_id
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def score(self) -> int:
        return self._score
    
    @property
    def total_possible_score(self) -> int:
        return sum(q.get_points() for q in self._questions)
    
    @property
    def percentage_score(self) -> float:
        if self.total_possible_score == 0:
            return 0.0
        return (self._score / self.total_possible_score) * 100
    
    @property
    def current_question(self) -> Optional[Question]:
        """Get the current question"""
        if self._current_question_index < len(self._questions):
            return self._questions[self._current_question_index]
        return None
    
    @property
    def is_complete(self) -> bool:
        """Check if quiz is complete"""
        return self._current_question_index >= len(self._questions)
    
    @property
    def progress(self) -> str:
        """Get progress as string"""
        return f"{self._current_question_index}/{len(self._questions)}"
    
    def start(self) -> None:
        """Start the quiz session"""
        self._start_time = datetime.now()
        self._status = "in_progress"
    
    def submit_answer(self, answer: str) -> bool:
        """
        Submit an answer for the current question.
        
        Args:
            answer: User's answer
            
        Returns:
            True if answer was correct, False otherwise
        """
        if self.is_complete:
            raise ValueError("Quiz is already complete")
        
        current_q = self.current_question
        if not current_q:
            raise ValueError("No current question")
        
        is_correct = current_q.check_answer(answer)
        
        if is_correct:
            points = current_q.get_points()
            self._score += points
        else:
            points = 0
        
        self._answers.append({
            "question_id": current_q.question_id,
            "user_answer": answer,
            "is_correct": is_correct,
            "points_awarded": points
        })
        
        self._current_question_index += 1
        
        return is_correct
    
    def finish(self) -> Dict[str, Any]:
        """Finish the quiz and return results"""
        self._end_time = datetime.now()
        self._status = "completed"
        
        duration = (self._end_time - self._start_time).total_seconds() if self._start_time else 0
        
        return {
            "session_id": self._session_id,
            "user_id": self._user_id,
            "score": self._score,
            "total_possible": self.total_possible_score,
            "percentage": self.percentage_score,
            "questions_answered": len(self._answers),
            "total_questions": len(self._questions),
            "correct_count": sum(1 for a in self._answers if a["is_correct"]),
            "duration_seconds": duration,
            "status": self._status
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert QuizSession to dictionary"""
        return {
            "session_id": self._session_id,
            "user_id": self._user_id,
            "difficulty": self._difficulty,
            "score": self._score,
            "answers": self._answers,
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "end_time": self._end_time.isoformat() if self._end_time else None,
            "status": self._status
        }
    
    def __str__(self) -> str:
        return f"QuizSession({self._session_id[:8]}..., Score: {self._score})"