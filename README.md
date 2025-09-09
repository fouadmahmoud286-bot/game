#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
لعبة سرعة القرارات - لعبة ذكاء وتركيز لتنمية سرعة البديهة
تشغيل اللعبة: python speed_decisions_game.py
ثم افتح المتصفح على: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify
import random
import webbrowser
import threading
import time

app = Flask(__name__)

# مجموعة الأسئلة المتنوعة
QUESTION_BANK = [
    # أسئلة رياضيات
    {"question": "5 + 3 = 8", "answer": True},
    {"question": "10 - 4 = 7", "answer": False},
    {"question": "2 × 6 = 12", "answer": True},
    {"question": "15 ÷ 3 = 5", "answer": True},
    {"question": "7 + 8 = 16", "answer": False},
    {"question": "9 × 2 = 18", "answer": True},
    {"question": "20 - 7 = 12", "answer": False},
    {"question": "4 × 4 = 16", "answer": True},
    {"question": "18 ÷ 6 = 3", "answer": True},
    {"question": "11 + 9 = 21", "answer": False},
    
    # معلومات عامة
    {"question": "القاهرة عاصمة مصر", "answer": True},
    {"question": "في السنة 13 شهر", "answer": False},
    {"question": "الأسد ملك الغابة", "answer": True},
    {"question": "الشمس تشرق من الغرب", "answer": False},
    {"question": "الماء يغلي عند 100 درجة مئوية", "answer": True},
    {"question": "في الأسبوع 8 أيام", "answer": False},
    {"question": "البحر الأحمر في مصر", "answer": True},
    {"question": "الفيل أصغر من النملة", "answer": False},
    {"question": "النيل أطول أنهار العالم", "answer": True},
    {"question": "القمر يضيء بنوره الذاتي", "answer": False},
    
    # أسئلة منطق
    {"question": "إذا كان اليوم الثلاثاء، فغداً الأربعاء", "answer": True},
    {"question": "كل الطيور تطير", "answer": False},
    {"question": "الثلج بارد", "answer": True},
    {"question": "النار تحرق", "answer": True},
    {"question": "السمك يعيش في الصحراء", "answer": False},
    {"question": "الليل يأتي بعد النهار", "answer": True},
    {"question": "الشتاء أبرد من الصيف", "answer": True},
    {"question": "الجليد أسخن من الماء المغلي", "answer": False},
    {"question": "الإنسان يحتاج للهواء ليعيش", "answer": True},
    {"question": "الأشجار تنمو تحت الأرض", "answer": False}
]

# قالب HTML للعبة
GAME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 لعبة سرعة القرارات 🚀</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .game-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            width: 90%;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .game-title {
            font-size: 2.5em;
            color: #4a5568;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .score-board {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .score, .timer {
            font-size: 1.5em;
            font-weight: bold;
            color: #2d3748;
        }

        .timer {
            color: #e53e3e;
            animation: pulse 1s infinite;
        }
        
        .timer.warning {
            color: #ff0000;
            animation: pulse 0.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        .question-container {
            background: linear-gradient(45deg, #a8edea, #fed6e3);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .question {
            font-size: 1.8em;
            color: #2d3748;
            font-weight: bold;
            line-height: 1.4;
        }

        .buttons-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 20px;
        }

        .answer-btn {
            padding: 20px 40px;
            font-size: 1.5em;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            transform: translateY(0);
        }

        .correct-btn {
            background: linear-gradient(45deg, #48bb78, #38a169);
            color: white;
        }

        .wrong-btn {
            background: linear-gradient(45deg, #f56565, #e53e3e);
            color: white;
        }

        .answer-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.3);
        }

        .answer-btn:active {
            transform: translateY(-2px);
        }

        .start-btn, .restart-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            font-size: 1.3em;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        .start-btn:hover, .restart-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.3);
        }

        .game-over {
            background: linear-gradient(45deg, #ffecd2, #fcb69f);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .final-score {
            font-size: 2em;
            color: #2d3748;
            margin-bottom: 20px;
            font-weight: bold;
        }

        .hidden {
            display: none;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            transition: width 0.1s linear;
            border-radius: 4px;
        }

        .celebration {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }

        .confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            background: #ff6b6b;
            animation: fall 3s linear infinite;
        }

        @keyframes fall {
            0% {
                transform: translateY(-100vh) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1 class="game-title">🧠 لعبة سرعة القرارات 🚀</h1>
        
        <div id="startScreen">
            <div class="question-container">
                <div class="question">
                    مرحباً بك في لعبة سرعة القرارات!<br>
                    اختبر سرعة بديهتك وقدرتك على اتخاذ القرارات السريعة<br>
                    لديك 3 ثوانٍ فقط للإجابة على كل سؤال
                </div>
            </div>
            <button class="start-btn" onclick="startGame()">🎮 ابدأ اللعبة</button>
        </div>

        <div id="gameScreen" class="hidden">
            <div class="score-board">
                <div class="score">النقاط: <span id="score">0</span></div>
                <div class="timer">الوقت: <span id="timer">3</span></div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar"></div>
            </div>
            
            <div class="question-container">
                <div class="question" id="question"></div>
            </div>
            
            <div class="buttons-container">
                <button class="answer-btn correct-btn" onclick="answerQuestion(true)">
                    ✅ صح
                </button>
                <button class="answer-btn wrong-btn" onclick="answerQuestion(false)">
                    ❌ غلط
                </button>
            </div>
        </div>

        <div id="gameOverScreen" class="hidden">
            <div class="game-over">
                <div class="final-score">🎉 انتهت اللعبة! 🎉</div>
                <div class="final-score">نقاطك النهائية: <span id="finalScore">0</span></div>
                <div id="scoreMessage" style="font-size: 1.2em; margin: 20px 0; color: #4a5568;"></div>
                <button class="restart-btn" onclick="restartGame()">🔄 العب مرة أخرى</button>
            </div>
        </div>

        <div class="celebration" id="celebration"></div>
    </div>

    <script>
        let currentScore = 0;
        let currentQuestion = 0;
        let timeLeft = 3;
        let gameTimer;
        let progressTimer;
        let questions = [];

        // تحميل الأسئلة من الخادم
        async function loadQuestions() {
            try {
                const response = await fetch('/api/questions');
                questions = await response.json();
            } catch (error) {
                console.error('خطأ في تحميل الأسئلة:', error);
                // استخدام أسئلة افتراضية في حالة الخطأ
                questions = [
                    { question: "5 + 3 = 8", answer: true },
                    { question: "10 - 4 = 7", answer: false },
                    { question: "القاهرة عاصمة مصر", answer: true },
                    { question: "الشمس تشرق من الغرب", answer: false }
                ];
            }
        }

        async function startGame() {
            document.getElementById('startScreen').classList.add('hidden');
            document.getElementById('gameScreen').classList.remove('hidden');
            document.getElementById('gameOverScreen').classList.add('hidden');
            
            currentScore = 0;
            currentQuestion = 0;
            
            await loadQuestions();
            
            updateScore();
            showNextQuestion();
        }

        function showNextQuestion() {
            if (currentQuestion >= questions.length) {
                loadQuestions().then(() => {
                    currentQuestion = 0;
                    displayQuestion();
                });
            } else {
                displayQuestion();
            }
        }

        function displayQuestion() {
            const questionElement = document.getElementById('question');
            if (questionElement && questions[currentQuestion]) {
                questionElement.textContent = questions[currentQuestion].question;
            }
            
            timeLeft = 3;
            updateTimer();
            startTimer();
        }

        function startTimer() {
            clearInterval(gameTimer);
            clearInterval(progressTimer);
            
            let progress = 100;
            const progressBar = document.getElementById('progressBar');
            const timerElement = document.getElementById('timer');
            
            if (progressBar) {
                progressBar.style.width = '100%';
            }
            
            progressTimer = setInterval(() => {
                progress -= (100 / 30);
                if (progressBar) {
                    progressBar.style.width = Math.max(0, progress) + '%';
                }
            }, 100);
            
            gameTimer = setInterval(() => {
                timeLeft--;
                updateTimer();
                
                if (timeLeft === 1 && timerElement) {
                    timerElement.classList.add('warning');
                } else if (timerElement) {
                    timerElement.classList.remove('warning');
                }
                
                if (timeLeft <= 0) {
                    clearInterval(gameTimer);
                    clearInterval(progressTimer);
                    gameOver();
                }
            }, 1000);
        }

        function updateTimer() {
            const timerElement = document.getElementById('timer');
            if (timerElement) {
                timerElement.textContent = Math.max(0, timeLeft);
            }
        }

        function updateScore() {
            const scoreElement = document.getElementById('score');
            if (scoreElement) {
                scoreElement.textContent = currentScore;
            }
        }

        function answerQuestion(userAnswer) {
            if (timeLeft <= 0) return;
            
            clearInterval(gameTimer);
            clearInterval(progressTimer);
            
            if (!questions[currentQuestion]) {
                gameOver();
                return;
            }
            
            const correctAnswer = questions[currentQuestion].answer;
            
            if (userAnswer === correctAnswer) {
                currentScore++;
                updateScore();
                createCelebration();
                currentQuestion++;
                
                setTimeout(() => {
                    showNextQuestion();
                }, 800);
            } else {
                gameOver();
            }
        }

        function createCelebration() {
            const celebration = document.getElementById('celebration');
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];
            
            for (let i = 0; i < 10; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                celebration.appendChild(confetti);
                
                setTimeout(() => {
                    confetti.remove();
                }, 3000);
            }
        }

        function gameOver() {
            clearInterval(gameTimer);
            clearInterval(progressTimer);
            
            const gameScreen = document.getElementById('gameScreen');
            const gameOverScreen = document.getElementById('gameOverScreen');
            const finalScoreElement = document.getElementById('finalScore');
            const scoreMessageElement = document.getElementById('scoreMessage');
            
            if (gameScreen) gameScreen.classList.add('hidden');
            if (gameOverScreen) gameOverScreen.classList.remove('hidden');
            if (finalScoreElement) finalScoreElement.textContent = currentScore;
            
            let message = '';
            if (currentScore >= 20) {
                message = '🏆 ممتاز! أنت عبقري حقيقي!';
            } else if (currentScore >= 15) {
                message = '🌟 رائع جداً! سرعة بديهة عالية!';
            } else if (currentScore >= 10) {
                message = '👏 جيد جداً! استمر في التدريب!';
            } else if (currentScore >= 5) {
                message = '👍 جيد! يمكنك تحسين أدائك!';
            } else {
                message = '💪 لا بأس، المحاولة القادمة ستكون أفضل!';
            }
            
            if (scoreMessageElement) {
                scoreMessageElement.textContent = message;
            }
        }

        function restartGame() {
            startGame();
        }

        // دعم لوحة المفاتيح
        document.addEventListener('keydown', function(event) {
            const gameScreen = document.getElementById('gameScreen');
            if (!gameScreen || gameScreen.classList.contains('hidden')) return;
            
            if (event.repeat) return;
            
            if (event.key === 'ArrowRight' || event.key === '1') {
                event.preventDefault();
                answerQuestion(true);
            } else if (event.key === 'ArrowLeft' || event.key === '0') {
                event.preventDefault();
                answerQuestion(false);
            }
        });
        
        document.addEventListener('DOMContentLoaded', function() {
            const startScreen = document.getElementById('startScreen');
            const gameScreen = document.getElementById('gameScreen');
            const gameOverScreen = document.getElementById('gameOverScreen');
            
            if (startScreen) startScreen.classList.remove('hidden');
            if (gameScreen) gameScreen.classList.add('hidden');
            if (gameOverScreen) gameOverScreen.classList.add('hidden');
        });
    </script>
</body>
</html>
'''

@app.route('/')
def game():
    """الصفحة الرئيسية للعبة"""
    return render_template_string(GAME_TEMPLATE)

@app.route('/api/questions')
def get_questions():
    """API للحصول على الأسئلة مخلوطة"""
    shuffled_questions = random.sample(QUESTION_BANK, len(QUESTION_BANK))
    return jsonify(shuffled_questions)

def open_browser():
    """فتح المتصفح تلقائياً بعد تشغيل الخادم"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("لعبة سرعة القرارات")
    print("=" * 50)
    print("بدء تشغيل اللعبة...")
    print("الرابط المحلي: http://localhost:5000")
    print("للوصول من الهاتف: http://192.168.1.12:5000")
    print("لإيقاف اللعبة: اضغط Ctrl+C")
    print("=" * 50)
    
    # فتح المتصفح تلقائياً
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل الخادم
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nتم إيقاف اللعبة. شكراً لك!")
    except Exception as e:
        print(f"خطأ في تشغيل اللعبة: {e}")
        print("تأكد من أن Flask مثبت: pip install flask")
