import requests
import html
from typing import List, Dict, Any, Optional
from models import Question

class APIHandler:
    BASE_URL = "https://opentdb.com/api.php"
    
    @staticmethod
    def fetch_questions(amount: int = 15, category: Optional[int] = None, 
                       difficulty: Optional[str] = None) -> List[Question]:
        """
        Fetch trivia questions from Open Trivia Database API.
        
        Args:
            amount: Number of questions to fetch (1-50, default 15)
            category: Category ID (optional). See https://opentdb.com/api_category.php for IDs
            difficulty: Difficulty level - 'easy', 'medium', 'hard' (optional)
        
        Returns:
            List of Question objects
        """
        try:
            params = {"amount": min(amount, 50)}  # API max is 50
            
            if category:
                params["category"] = category
            if difficulty:
                params["difficulty"] = difficulty.lower()
            
            response = requests.get(APIHandler.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("response_code") != 0:
                print(f"API Error: response code {data.get('response_code')}")
                return []
            
            questions = []
            for idx, item in enumerate(data.get("results", [])):
                try:
                    question = APIHandler._parse_question(item, idx)
                    questions.append(question)
                except (KeyError, ValueError) as e:
                    print(f"Error parsing question: {e}")
                    continue
            
            return questions
        
        except requests.RequestException as e:
            print(f"Error fetching from API: {e}")
            return []
    
    @staticmethod
    def _parse_question(item: Dict[str, Any], index: int) -> Question:
        """Convert API response item to Question object."""
        # Decode HTML entities (API returns HTML-encoded text)
        question_text = html.unescape(item.get("question", ""))
        correct_answer = html.unescape(item.get("correct_answer", ""))
        incorrect_answers = [html.unescape(ans) for ans in item.get("incorrect_answers", [])]
        category = html.unescape(item.get("category", "General"))
        
        # Combine and shuffle options
        options = [correct_answer] + incorrect_answers
        # Simple shuffle using the index as seed for reproducibility
        import random
        random.seed(hash(question_text))
        random.shuffle(options)
        
        question = Question(
            text=question_text,
            options=options,
            correct_answer=correct_answer,
            difficulty=item.get("difficulty", "medium"),
            category=category,
            question_id=f"api_q{index}"
        )
        
        return question
    
    @staticmethod
    def get_categories() -> Dict[int, str]:
        """
        Fetch available categories from the API.
        
        Returns:
            Dictionary mapping category IDs to category names
        """
        try:
            response = requests.get("https://opentdb.com/api_category.php", timeout=10)
            response.raise_for_status()
            
            categories = {}
            for item in response.json().get("trivia_categories", []):
                categories[item["id"]] = item["name"]
            
            return categories
        except requests.RequestException as e:
            print(f"Error fetching categories: {e}")
            return {}
