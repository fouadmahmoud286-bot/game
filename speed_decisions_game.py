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
GAME_TEMPLATE = '''... (تم اختصار الكود هنا لأنه طويل جداً، ولكن هو نفس الكود اللي كتبته فوق بالكامل) ...'''

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
