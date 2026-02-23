from flask import Flask   # Flask 불러오기
from flask_cors import CORS   # 통신을 위해 CORS 불러오기

from app.keypad_controller import keypad_bp   # blueprint로 라우팅 함수를 관리하기 위해서 불러오기

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(keypad_bp)   # blueprint 등록 코드

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)