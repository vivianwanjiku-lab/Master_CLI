import pytest
from unittest.mock import patch, MagicMock
from cli import QuizCLI
from models import Question, User


class TestQuizCLI:
    @pytest.fixture
    def cli(self):
        """Create QuizCLI instance"""
        return QuizCLI()
    
    def test_cli_initialization(self, cli):
        """Test CLI initialization"""
        assert cli.parser is not None
        assert cli.file_handler is not None
    
    def test_parser_has_subcommands(self, cli):
        """Test parser has required subcommands"""
        # Parse help to verify subcommands exist
        with pytest.raises(SystemExit):
            cli.parser.parse_args(['--help'])
    
    def test_user_command_structure(self, cli):
        """Test user command argument parsing"""
        args = cli.parser.parse_args(['user', 'create', '-u', 'testuser', '-e', 'test@example.com'])
        
        assert args.command == 'user'
        assert args.action == 'create'
        assert args.username == 'testuser'
        assert args.email == 'test@example.com'
    
    def test_play_command_structure(self, cli):
        """Test play command argument parsing"""
        args = cli.parser.parse_args(['play', '-u', 'user123'])
        
        assert args.command == 'play'
        assert args.user == 'user123'
    
    def test_question_command_structure(self, cli):
        """Test question command argument parsing"""
        args = cli.parser.parse_args(['question', 'list'])
        
        assert args.command == 'question'
        assert args.action == 'list'
    
    def test_question_add_command_structure(self, cli):
        """Test question add command argument parsing"""
        args = cli.parser.parse_args([
            'question', 'add',
            '-t', 'What is 2+2?',
            '-o', 'A', 'B', 'C', 'D',
            '-a', 'D',
            '-d', 'easy'
        ])
        
        assert args.command == 'question'
        assert args.action == 'add'
        assert args.text == 'What is 2+2?'
        assert len(args.options) == 4
        assert args.answer == 'D'
        assert args.difficulty == 'easy'
    
    def test_scores_command_structure(self, cli):
        """Test scores command argument parsing"""
        args = cli.parser.parse_args(['scores', '--leaderboard'])
        
        assert args.command == 'scores'
        assert args.leaderboard is True
    
    @patch('cli.QuizCLI._handle_user')
    def test_run_user_command(self, mock_handler, cli):
        """Test running user command"""
        cli.run(['user', 'create', '-u', 'testuser', '-e', 'test@example.com'])
        
        mock_handler.assert_called_once()
    
    def test_ensure_sample_questions(self, cli):
        """Test that sample questions are created on initialization"""
        questions = cli.file_handler.load_data("questions")
        
        # Check that questions were created
        assert len(questions) > 0
        
        # Check that sample questions have required fields
        for qid, q in questions.items():
            assert 'text' in q
            assert 'options' in q
            assert 'correct_answer' in q
            assert 'difficulty' in q
            assert 'category' in q


class TestHandlePlay:
    @pytest.fixture
    def cli(self):
        """Create CLI instance with test data"""
        cli = QuizCLI()
        # Add a test user
        user = User("testuser", "test@example.com")
        users_data = cli.file_handler.load_data("users")
        users_data[user.user_id] = user.to_dict()
        cli.file_handler.save_data("users", users_data)
        return cli, user
    
    def test_handle_play_user_not_found(self, cli):
        """Test play command with non-existent user"""
        cli_obj, _ = cli
        
        args = MagicMock()
        args.user = "nonexistent_user"
        args.difficulty = None
        
        with patch('builtins.print') as mock_print:
            cli_obj._handle_play(args)
            
            # Check that error message was printed
            mock_print.assert_called()
            call_args = str(mock_print.call_args_list)
            assert "not found" in call_args.lower()


class TestHandleUser:
    @pytest.fixture
    def cli(self):
        """Create CLI instance"""
        return QuizCLI()
    
    @patch('builtins.print')
    def test_handle_user_create_valid(self, mock_print, cli):
        """Test creating a valid user"""
        args = MagicMock()
        args.action = 'create'
        args.username = 'newuser'
        args.email = 'new@example.com'
        
        cli._handle_user(args)
        
        # Check user was created
        users_data = cli.file_handler.load_data("users")
        assert len(users_data) > 0
    
    @patch('builtins.print')
    def test_handle_user_create_invalid_username(self, mock_print, cli):
        """Test creating user with invalid username"""
        args = MagicMock()
        args.action = 'create'
        args.username = 'ab'  # Too short
        args.email = 'test@example.com'
        
        cli._handle_user(args)
        
        # Check that error message was printed
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_user_create_invalid_email(self, mock_print, cli):
        """Test creating user with invalid email"""
        args = MagicMock()
        args.action = 'create'
        args.username = 'validuser'
        args.email = 'invalid-email'
        
        cli._handle_user(args)
        
        # Check that error message was printed
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_handle_user_list(self, mock_print, cli):
        """Test listing users"""
        # Add a test user
        user = User("testuser", "test@example.com")
        users_data = cli.file_handler.load_data("users")
        users_data[user.user_id] = user.to_dict()
        cli.file_handler.save_data("users", users_data)
        
        args = MagicMock()
        args.action = 'list'
        
        cli._handle_user(args)
        
        # Check that users were listed
        mock_print.assert_called()
