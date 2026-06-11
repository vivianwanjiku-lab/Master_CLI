#!/usr/bin/env python3
import argparse
import sys
from typing import List

from models import User, QuizSession, Question
from utils import FileHandler, Validators, APIHandler


class QuizCLI:
    def __init__(self):
        self.file_handler = FileHandler()
        self.parser = self._create_parser()
        self._ensure_sample_questions()
    
    def _ensure_sample_questions(self):
        questions_data = self.file_handler.load_data("questions")
        if not questions_data:
            sample_questions = {
                "q1": {
                    "question_id": "q1",
                    "text": "What is the capital of France?",
                    "options": ["London", "Berlin", "Paris", "Madrid"],
                    "correct_answer": "Paris",
                    "difficulty": "easy",
                    "category": "Geography",
                    "times_asked": 0,
                    "times_correct": 0
                },
                "q2": {
                    "question_id": "q2",
                    "text": "Which Python keyword is used to define a function?",
                    "options": ["function", "def", "define", "func"],
                    "correct_answer": "def",
                    "difficulty": "easy",
                    "category": "Programming",
                    "times_asked": 0,
                    "times_correct": 0
                },
                "q3": {
                    "question_id": "q3",
                    "text": "What does CPU stand for?",
                    "options": ["Computer Processing Unit", "Central Processing Unit", "Core Program Unit", "Computer Program Unit"],
                    "correct_answer": "Central Processing Unit",
                    "difficulty": "medium",
                    "category": "Computers",
                    "times_asked": 0,
                    "times_correct": 0
                }
            }
            self.file_handler.save_data("questions", sample_questions)
    
    def _create_parser(self):
        parser = argparse.ArgumentParser(prog="quiz", description="Quiz Game CLI")
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        
        # User commands
        user_parser = subparsers.add_parser("user", help="Manage users")
        user_subparsers = user_parser.add_subparsers(dest="action")
        
        user_create = user_subparsers.add_parser("create", help="Create user")
        user_create.add_argument("--username", "-u", required=True)
        user_create.add_argument("--email", "-e", required=True)
        
        user_list = user_subparsers.add_parser("list", help="List users")
        
        # Quiz command
        play_parser = subparsers.add_parser("play", help="Start quiz")
        play_parser.add_argument("--user", "-u", required=True, help="User ID")
        play_parser.add_argument("--difficulty", "-d", choices=["easy", "medium", "hard"])
        
        # Question commands
        question_parser = subparsers.add_parser("question", help="Manage questions")
        question_subparsers = question_parser.add_subparsers(dest="action")
        
        question_list = question_subparsers.add_parser("list", help="List questions")
        question_add = question_subparsers.add_parser("add", help="Add question")
        question_add.add_argument("--text", "-t", required=True)
        question_add.add_argument("--options", "-o", nargs=4, required=True)
        question_add.add_argument("--answer", "-a", required=True)
        question_add.add_argument("--difficulty", "-d", default="medium")
        
        question_fetch = question_subparsers.add_parser("fetch", help="Fetch questions from API")
        question_fetch.add_argument("--amount", "-n", type=int, default=15, help="Number of questions (1-50)")
        question_fetch.add_argument("--difficulty", "-d", choices=["easy", "medium", "hard"])
        question_fetch.add_argument("--category", "-c", type=int, help="Category ID")
        question_fetch.add_argument("--categories", action="store_true", help="List available categories")
        
        # Scores
        scores_parser = subparsers.add_parser("scores", help="View scores")
        scores_parser.add_argument("--leaderboard", "-l", action="store_true")
        
        return parser
    
    def run(self, args: List[str] = None):
        if args is None:
            args = sys.argv[1:]
        
        if not args:
            self.parser.print_help()
            return
        
        parsed_args = self.parser.parse_args(args)
        
        if parsed_args.command == "user":
            self._handle_user(parsed_args)
        elif parsed_args.command == "play":
            self._handle_play(parsed_args)
        elif parsed_args.command == "question":
            self._handle_question(parsed_args)
        elif parsed_args.command == "scores":
            self._handle_scores(parsed_args)
        else:
            self.parser.print_help()
    
    def _handle_user(self, args):
        if not args.action:
            print("Please specify: create or list")
            return
        
        if args.action == "create":
            valid, error = Validators.validate_username(args.username)
            if not valid:
                print(f"Error: {error}")
                return
            
            valid, error = Validators.validate_email(args.email)
            if not valid:
                print(f"Error: {error}")
                return
            
            user = User(args.username, args.email)
            users_data = self.file_handler.load_data("users")
            users_data[user.user_id] = user.to_dict()
            
            if self.file_handler.save_data("users", users_data):
                print(f"✅ User created! ID: {user.user_id}")
            else:
                print("❌ Failed to save user")
        
        elif args.action == "list":
            users_data = self.file_handler.load_data("users")
            if not users_data:
                print("No users found")
                return
            print("\nUsers:")
            print("-" * 50)
            for uid, user in users_data.items():
                print(f"ID: {uid[:8]}... | Name: {user['username']} | Email: {user['email']}")
    
    def _handle_play(self, args):
        user_data = self.file_handler.get_item("users", args.user)
        if not user_data:
            print(f"❌ User {args.user} not found")
            return
        
        questions_data = self.file_handler.load_data("questions")
        if not questions_data:
            print("No questions available")
            return
        
        questions = [Question.from_dict(q) for q in questions_data.values()]
        
        if args.difficulty:
            questions = [q for q in questions if q.difficulty == args.difficulty]
        
        if not questions:
            print(f"No questions found for difficulty: {args.difficulty}")
            return
        
        session = QuizSession(args.user, questions, args.difficulty)
        session.start()
        
        print(f"\n🎯 Starting quiz for {user_data['username']}")
        print(f"Questions: {len(questions)}")
        input("Press Enter to begin...")
        
        while not session.is_complete:
            q = session.current_question
            print(f"\nQuestion {session.progress}")
            print(f"Category: {q.category} | Difficulty: {q.difficulty.upper()}")
            print(f"\n{q.text}\n")
            
            for i, opt in enumerate(q.options, 1):
                print(f"  {i}. {opt}")
            
            answer = input("\nYour answer (1-4 or type the answer): ").strip()
            
            # Convert number to answer text
            if answer.isdigit() and 1 <= int(answer) <= 4:
                answer = q.options[int(answer) - 1]
            
            is_correct = session.submit_answer(answer)
            
            if is_correct:
                print(f"\n✅ Correct! +{q.get_points()} points")
            else:
                print(f"\n❌ Wrong! Answer: {q.correct_answer}")
            
            if not session.is_complete:
                input("\nPress Enter for next question...")
        
        results = session.finish()
        print("\n" + "=" * 40)
        print(f"🎉 Quiz Complete!")
        print(f"Score: {results['score']}/{results['total_possible']}")
        print(f"Percentage: {results['percentage']:.1f}%")
        print("=" * 40)
    
    def _handle_question(self, args):
        if not args.action:
            print("Please specify: list, add, or fetch")
            return
        
        if args.action == "list":
            questions_data = self.file_handler.load_data("questions")
            if not questions_data:
                print("No questions found")
                return
            print("\nQuestions:")
            print("-" * 60)
            for qid, q in questions_data.items():
                print(f"ID: {qid[:8]}... | {q['text'][:40]} | {q['difficulty']}")
        
        elif args.action == "add":
            question = Question(
                text=args.text,
                options=list(args.options),
                correct_answer=args.answer,
                difficulty=args.difficulty
            )
            questions_data = self.file_handler.load_data("questions")
            questions_data[question.question_id] = question.to_dict()
            
            if self.file_handler.save_data("questions", questions_data):
                print(f"✅ Question added! ID: {question.question_id}")
            else:
                print("❌ Failed to save question")
        
        elif args.action == "fetch":
            # Show categories
            if args.categories:
                categories = APIHandler.get_categories()
                if categories:
                    print("\n📚 Available Categories:")
                    print("-" * 50)
                    for cat_id, cat_name in sorted(categories.items()):
                        print(f"  {cat_id}: {cat_name}")
                else:
                    print("❌ Failed to fetch categories")
                return
            
            # Fetch questions from API
            print(f"📡 Fetching {args.amount} questions from Open Trivia Database...")
            questions = APIHandler.fetch_questions(
                amount=args.amount,
                difficulty=args.difficulty,
                category=args.category
            )
            
            if not questions:
                print("❌ Failed to fetch questions from API")
                return
            
            # Save to local storage
            questions_data = self.file_handler.load_data("questions")
            for q in questions:
                questions_data[q.question_id] = q.to_dict()
            
            if self.file_handler.save_data("questions", questions_data):
                print(f"✅ Successfully fetched and saved {len(questions)} questions!")
                print("\nSample question:")
                print(f"  {questions[0].text[:60]}...")
            else:
                print("❌ Failed to save questions")
    
    def _handle_scores(self, args):
        if args.leaderboard:
            users_data = self.file_handler.load_data("users")
            if not users_data:
                print("No scores yet")
                return
            
            sorted_users = sorted(users_data.values(), key=lambda x: x.get("total_score", 0), reverse=True)
            print("\n🏆 LEADERBOARD 🏆")
            print("-" * 50)
            for i, user in enumerate(sorted_users[:5], 1):
                print(f"{i}. {user['username']}: {user.get('total_score', 0)} points ({user.get('quizzes_taken', 0)} quizzes)")
        else:
            print("Use --leaderboard to see scores")


def main():
    cli = QuizCLI()
    cli.run()


if __name__ == "__main__":
    main()