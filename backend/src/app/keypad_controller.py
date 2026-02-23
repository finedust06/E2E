from flask import Blueprint, jsonify, request
from service.keypad_service import generate_keypad

keypad_bp = Blueprint("keypad", __name__)

@keypad_bp.route("/api/keypad", methods=["GET"])
def get_keypad():
    data = generate_keypad()
    print(f"✅ 키패드 생성 완료! (세션: {data['session_id']})")
    return jsonify(data)

@keypad_bp.route("/api/submit", methods=["POST"])
def submit_password():
    data = request.json or {}
    print("\n[📥 데이터 수신]")
    print(f" - 세션 ID: {data.get('session_id')}")
    print(f" - 입력된 해시값들: {data.get('input_hashes')}")
    return jsonify({"message": "비밀번호가 서버에 잘 도착했습니다!"})