import pytest
import os
import json
import tempfile
from utils import FileHandler, Validators


class TestValidators:
    def test_validate_email_valid(self):
        """Test valid email validation"""
        valid, msg = Validators.validate_email("test@example.com")
        assert valid is True
    
    def test_validate_email_invalid_format(self):
        """Test invalid email formats"""
        invalid_emails = [
            "test",
            "test@",
            "test@example",
            "@example.com"
        ]
        for email in invalid_emails:
            valid, msg = Validators.validate_email(email)
            assert valid is False
    
    def test_validate_email_empty(self):
        """Test empty email validation"""
        valid, msg = Validators.validate_email("")
        assert valid is False
        assert "empty" in msg.lower()
    
    def test_validate_username_valid(self):
        """Test valid username validation"""
        valid, msg = Validators.validate_username("testuser123")
        assert valid is True
    
    def test_validate_username_too_short(self):
        """Test username too short"""
        valid, msg = Validators.validate_username("ab")
        assert valid is False
        assert "at least 3" in msg.lower()
    
    def test_validate_username_too_long(self):
        """Test username too long"""
        valid, msg = Validators.validate_username("a" * 21)
        assert valid is False
        assert "at most 20" in msg.lower()
    
    def test_validate_username_invalid_characters(self):
        """Test username with invalid characters"""
        invalid_usernames = ["test-user", "test user", "test@user"]
        for username in invalid_usernames:
            valid, msg = Validators.validate_username(username)
            assert valid is False
    
    def test_validate_username_empty(self):
        """Test empty username validation"""
        valid, msg = Validators.validate_username("")
        assert valid is False
    
    def test_validate_difficulty_valid(self):
        """Test valid difficulty levels"""
        for diff in ["easy", "medium", "hard", "EASY", "MEDIUM", "HARD"]:
            valid, msg = Validators.validate_difficulty(diff)
            assert valid is True
    
    def test_validate_difficulty_invalid(self):
        """Test invalid difficulty level"""
        valid, msg = Validators.validate_difficulty("impossible")
        assert valid is False


class TestFileHandler:
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            old_data_dir = FileHandler.DATA_DIR
            FileHandler.DATA_DIR = tmpdir
            yield tmpdir
            FileHandler.DATA_DIR = old_data_dir
    
    def test_file_handler_initialization(self, temp_data_dir):
        """Test FileHandler initialization"""
        handler = FileHandler()
        
        assert os.path.exists(temp_data_dir)
        assert os.path.exists(os.path.join(temp_data_dir, "users.json"))
        assert os.path.exists(os.path.join(temp_data_dir, "questions.json"))
        assert os.path.exists(os.path.join(temp_data_dir, "quizzes.json"))
    
    def test_file_handler_save_and_load(self, temp_data_dir):
        """Test saving and loading data"""
        handler = FileHandler()
        
        test_data = {
            "key1": {"name": "Item 1", "value": 100},
            "key2": {"name": "Item 2", "value": 200}
        }
        
        assert handler.save_data("users", test_data) is True
        
        loaded_data = handler.load_data("users")
        assert loaded_data == test_data
    
    def test_file_handler_invalid_data_type(self, temp_data_dir):
        """Test invalid data type handling"""
        handler = FileHandler()
        
        loaded = handler.load_data("invalid_type")
        assert loaded == {}
    
    def test_file_handler_save_invalid_type(self, temp_data_dir):
        """Test saving with invalid data type"""
        handler = FileHandler()
        
        result = handler.save_data("invalid_type", {})
        assert result is False
    
    def test_file_handler_get_item(self, temp_data_dir):
        """Test getting individual item"""
        handler = FileHandler()
        
        test_data = {
            "user1": {"name": "User One"},
            "user2": {"name": "User Two"}
        }
        
        handler.save_data("users", test_data)
        
        item = handler.get_item("users", "user1")
        assert item == {"name": "User One"}
    
    def test_file_handler_get_item_not_found(self, temp_data_dir):
        """Test getting non-existent item"""
        handler = FileHandler()
        
        test_data = {"user1": {"name": "User One"}}
        handler.save_data("users", test_data)
        
        item = handler.get_item("users", "user_not_found")
        assert item is None
    
    def test_file_handler_empty_load(self, temp_data_dir):
        """Test loading empty data file"""
        handler = FileHandler()
        
        loaded = handler.load_data("users")
        assert loaded == {}
