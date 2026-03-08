from flask import Blueprint, jsonify, request
from service.keypad_service import generate_keypad, SESSION_KEYS
from util.crypto import decrypt_data

keypad_bp = Blueprint("keypad", __name__)

@keypad_bp.route("/api/keypad", methods=["GET"])
def get_keypad():
    data = generate_keypad()
    print(f"키패드 생성 완료 (세션: {data['session_id']})")
    return jsonify(data)

@keypad_bp.route("/api/submit", methods=["POST"])
def submit_password():

    data = request.json or {}

    session_id = data.get("session_id")
    encrypted_hashes = data.get("encrypted_hashes")

    print("\n[데이터 수신]")
    print("세션 ID:", session_id)

    private_key = SESSION_KEYS.get(session_id)

    decrypted_hashes = []

    for h in encrypted_hashes:
        decrypted = decrypt_data(private_key, h)
        decrypted_hashes.append(decrypted)

    print("복호화된 해시값:", decrypted_hashes)

    return jsonify({"message": "ok"})