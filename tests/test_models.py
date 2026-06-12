import pytest
from models import Question, User, QuizSession


class TestQuestion:
    def test_question_creation(self):
        """Test basic question creation"""
        q = Question(
            text="What is 2+2?",
            options=["3", "4", "5", "6"],
            correct_answer="4",
            difficulty="easy",
            category="Math"
        )
        assert q.text == "What is 2+2?"
        assert q.correct_answer == "4"
        assert q.difficulty == "easy"
        assert q.category == "Math"
        assert len(q.options) == 4
    
    def test_question_default_difficulty(self):
        """Test question creation with default difficulty"""
        q = Question(
            text="Test?",
            options=["A", "B", "C", "D"],
            correct_answer="A"
        )
        assert q.difficulty == "medium"
    
    def test_question_check_answer_correct(self):
        """Test checking correct answer"""
        q = Question(
            text="What is the capital of France?",
            options=["London", "Paris", "Berlin", "Madrid"],
            correct_answer="Paris"
        )
        assert q.check_answer("Paris") is True
        assert q.times_correct == 1
        assert q.times_asked == 1
    
    def test_question_check_answer_case_insensitive(self):
        """Test that answer checking is case insensitive"""
        q = Question(
            text="What is the capital of France?",
            options=["London", "Paris", "Berlin", "Madrid"],
            correct_answer="Paris"
        )
        assert q.check_answer("paris") is True
        assert q.check_answer("PARIS") is True
    
    def test_question_check_answer_incorrect(self):
        """Test checking incorrect answer"""
        q = Question(
            text="What is the capital of France?",
            options=["London", "Paris", "Berlin", "Madrid"],
            correct_answer="Paris"
        )
        assert q.check_answer("London") is False
        assert q.times_correct == 0
        assert q.times_asked == 1
    
    def test_question_get_points(self):
        """Test point calculation based on difficulty"""
        easy = Question("?", ["A", "B", "C", "D"], "A", difficulty="easy")
        medium = Question("?", ["A", "B", "C", "D"], "A", difficulty="medium")
        hard = Question("?", ["A", "B", "C", "D"], "A", difficulty="hard")
        
        assert easy.get_points() == 10
        assert medium.get_points() == 20
        assert hard.get_points() == 30
    
    def test_question_to_dict(self):
        """Test conversion to dictionary"""
        q = Question(
            text="Test?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            difficulty="easy",
            category="Test"
        )
        q_dict = q.to_dict()
        
        assert q_dict["text"] == "Test?"
        assert q_dict["correct_answer"] == "A"
        assert q_dict["difficulty"] == "easy"
        assert q_dict["category"] == "Test"
    
    def test_question_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "question_id": "q1",
            "text": "What is 2+2?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4",
            "difficulty": "easy",
            "category": "Math",
            "times_asked": 5,
            "times_correct": 4
        }
        q = Question.from_dict(data)
        
        assert q.question_id == "q1"
        assert q.text == "What is 2+2?"
        assert q.correct_answer == "4"
        assert q.times_asked == 5
        assert q.times_correct == 4


class TestUser:
    def test_user_creation(self):
        """Test basic user creation"""
        user = User("testuser", "test@example.com")
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.total_score == 0
        assert user.quizzes_taken == 0
        assert user.average_score == 0.0
    
    def test_user_add_quiz_result(self):
        """Test adding quiz results"""
        user = User("testuser", "test@example.com")
        
        user.add_quiz_result("quiz1", 50)
        user.add_quiz_result("quiz2", 75)
        
        assert user.total_score == 125
        assert user.quizzes_taken == 2
        assert user.average_score == 62.5
    
    def test_user_to_dict(self):
        """Test conversion to dictionary"""
        user = User("testuser", "test@example.com")
        user.add_quiz_result("quiz1", 50)
        
        user_dict = user.to_dict()
        
        assert user_dict["username"] == "testuser"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["total_score"] == 50
        assert user_dict["quizzes_taken"] == 1
    
    def test_user_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "user_id": "u1",
            "username": "testuser",
            "email": "test@example.com",
            "created_at": "2024-01-01T00:00:00",
            "quiz_history": [{"quiz_id": "q1", "score": 50}],
            "total_score": 50,
            "quizzes_taken": 1
        }
        user = User.from_dict(data)
        
        assert user.user_id == "u1"
        assert user.username == "testuser"
        assert user.total_score == 50
        assert user.quizzes_taken == 1


class TestQuizSession:
    def test_quiz_session_creation(self):
        """Test basic quiz session creation"""
        questions = [
            Question("Q1?", ["A", "B", "C", "D"], "A"),
            Question("Q2?", ["A", "B", "C", "D"], "B"),
            Question("Q3?", ["A", "B", "C", "D"], "C")
        ]
        session = QuizSession("user1", questions)
        
        assert session.user_id == "user1"
        assert len(session._questions) == 3
        assert session.score == 0
        assert session.is_complete is False
    
    def test_quiz_session_current_question(self):
        """Test getting current question"""
        questions = [
            Question("Q1?", ["A", "B", "C", "D"], "A"),
            Question("Q2?", ["A", "B", "C", "D"], "B")
        ]
        session = QuizSession("user1", questions)
        
        current = session.current_question
        assert current is not None
        assert current.text in ["Q1?", "Q2?"]
    
    def test_quiz_session_no_questions_current_is_none(self):
        """Test that current_question is None when quiz is complete"""
        questions = [Question("Q1?", ["A", "B", "C", "D"], "A")]
        session = QuizSession("user1", questions)
        session.start()
        
        # Answer all questions
        session.submit_answer("A")
        
        assert session.is_complete is True
        assert session.current_question is None
    
    def test_quiz_session_submit_answer_correct(self):
        """Test submitting correct answer"""
        q = Question("Q1?", ["A", "B", "C", "D"], "A")
        session = QuizSession("user1", [q])
        session.start()
        
        is_correct = session.submit_answer("A")
        
        assert is_correct is True
        assert session.score == q.get_points()
    
    def test_quiz_session_submit_answer_incorrect(self):
        """Test submitting incorrect answer"""
        q = Question("Q1?", ["A", "B", "C", "D"], "A")
        session = QuizSession("user1", [q])
        session.start()
        
        is_correct = session.submit_answer("B")
        
        assert is_correct is False
        assert session.score == 0
    
    def test_quiz_session_progress(self):
        """Test quiz progress tracking"""
        questions = [
            Question("Q1?", ["A", "B", "C", "D"], "A"),
            Question("Q2?", ["A", "B", "C", "D"], "B")
        ]
        session = QuizSession("user1", questions)
        session.start()
        
        assert "0/2" in session.progress
        
        session.submit_answer("A")
        assert "1/2" in session.progress
    
    def test_quiz_session_finish(self):
        """Test finishing quiz"""
        questions = [
            Question("Q1?", ["A", "B", "C", "D"], "A"),
            Question("Q2?", ["A", "B", "C", "D"], "B")
        ]
        session = QuizSession("user1", questions)
        session.start()
        
        # Answer both questions correctly by getting the correct answer from current question
        q1 = session.current_question
        session.submit_answer(q1.correct_answer)
        
        q2 = session.current_question
        session.submit_answer(q2.correct_answer)
        
        results = session.finish()
        
        assert results["status"] == "completed"
        assert results["score"] > 0
        assert results["total_questions"] == 2
        assert results["correct_count"] == 2
    
    def test_quiz_session_difficulty_filter(self):
        """Test filtering questions by difficulty"""
        easy_q = Question("Easy?", ["A", "B", "C", "D"], "A", difficulty="easy")
        hard_q = Question("Hard?", ["A", "B", "C", "D"], "B", difficulty="hard")
        
        session = QuizSession("user1", [easy_q, hard_q], difficulty="easy")
        
        # All questions should be easy
        for q in session._questions:
            assert q.difficulty == "easy"
    
    def test_quiz_session_total_possible_score(self):
        """Test total possible score calculation"""
        easy_q = Question("Easy?", ["A", "B", "C", "D"], "A", difficulty="easy")
        hard_q = Question("Hard?", ["A", "B", "C", "D"], "B", difficulty="hard")
        
        session = QuizSession("user1", [easy_q, hard_q])
        
        expected = 10 + 30  # easy + hard
        assert session.total_possible_score == expected
    
    def test_quiz_session_percentage_score(self):
        """Test percentage score calculation"""
        q = Question("Q1?", ["A", "B", "C", "D"], "A", difficulty="medium")
        session = QuizSession("user1", [q])
        session.start()
        
        session.submit_answer("A")
        
        assert session.percentage_score == 100.0
