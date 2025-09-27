from flask import Flask, request, jsonify
from flask_cors import CORS # CORS 라이브러리 추가
import re

# Flask 앱 생성
app = Flask(__name__)
# 모든 도메인에서의 요청을 허용하도록 CORS 설정 (개발/테스트용)
CORS(app) 

# --- 데이터 익명화 함수 ---
def anonymize_text(text):
    # 이름 가명화 (홍길동 -> 홍*동)
    text = re.sub(r'([가-힣]{1})([가-힣]{1,2})([가-힣]{1})', r'\1*\3', text)
    # 주소 익명화 (서울특별시 강남구 테헤란로 123 -> 서울특별시 강남구)
    text = re.sub(r'([가-힣]+(시|군|구))\s+[가-힣0-9\s\-.]+', r'\1', text)
    # 주민등록번호 마스킹 (900101-1234567 -> 900101-*******)
    text = re.sub(r'(\d{6})[-]\d{7}', r'\1-*******', text)
    return text

# --- 피싱 메일 탐지 함수 (간단한 키워드 기반) ---
def detect_phishing(email_content):
    keywords = ["비밀번호", "계정", "로그인", "클릭", "은행", "업데이트", "즉시", "당첨"]
    score = 0
    for key in keywords:
        if key in email_content:
            score += 1
    return score >= 2 # 키워드가 2개 이상 포함되면 피싱으로 간주

# --- API 라우트 설정 ---
@app.route('/anonymize', methods=['POST'])
def handle_anonymize():
    data = request.json
    original_text = data.get('text', '')
    anonymized_text = anonymize_text(original_text)
    return jsonify({'anonymized_text': anonymized_text})

@app.route('/phishing-check', methods=['POST'])
def handle_phishing():
    data = request.json
    email_content = data.get('email', '')
    is_phishing = detect_phishing(email_content)
    return jsonify({'is_phishing': is_phishing})

# 서버 상태 확인용 루트
@app.route('/')
def health_check():
    return "AI 분석 서버가 정상적으로 작동 중입니다."

# gunicorn이 실행할 수 있도록 남겨둡니다.
# if __name__ == '__main__':
#    app.run()
