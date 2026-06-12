# 🎯 Quiz Game CLI

A professional command-line quiz game built with Python, featuring user management, custom questions, score tracking, and persistent storage.

## ✨ Features

- **User Management** - Create and manage multiple users
- **Custom Questions** - Add your own questions with 4 options
- **Multiple Difficulties** - Easy, Medium, and Hard levels
- **Score Tracking** - Persistent high scores and leaderboard
- **Statistics** - View user and global performance metrics

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/vivianwanjiku-lab/Master_cli.git
cd MASTER_CLI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests rich tabulate

# Run the game
python cli.py --help
```
## Game Flow 
# 1. Create a user
## python cli.py user create --username "QuizMaster" --email "master@quiz.com"
Output: ✅ User created! ID: abc-123-def

# 2. Add a custom question
## python cli.py question add \
    --text "What is the capital of Kenya?" \
    --options "Nairobi" "Mombasa" "Kisumu" "Nakuru" \
    --answer "Nairobi" \
    --difficulty medium

 Output: ✅ Question added! ID: q4

 3. Start a quiz
## python cli.py play --user abc-123-def --difficulty medium

 4. Answer questions interactively
 Question 1/5
## Category: Geography | Difficulty: MEDIUM
 What is the capital of Kenya?
  1. Nairobi
  2. Mombasa
  3. Kisumu
  4. Nakuru
# Your answer (1-4): 1
 ✅ Correct! +20 points

# 5. View results
🎉 Quiz Complete!
 # Score: 80/100
 # Percentage: 80.0%

# 6. Check leaderboard
## python cli.py scores --leaderboard

# Output:
🏆 LEADERBOARD 🏆
--------------------------------------------------
1. QuizMaster: 80 points (1 quizzes)
