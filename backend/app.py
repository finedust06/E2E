from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
import uuid
import hashlib

app = Flask(__name__)
CORS(app)  # 리액트와 통신 허용

def text_to_image_base64(text):
    """ 텍스트(숫자)를 입력받아 노이즈가 섞인 이미지(Base64)로 변환 """
    img = Image.new('RGB', (60, 60), color='white')
    d = ImageDraw.Draw(img)
    
    # 텍스트 그리기 (가운데 쯤)
    d.text((25, 20), text, fill='black') 
    
    # 노이즈(점) 찍기
    for _ in range(15):
        x = random.randint(0, 60)
        y = random.randint(0, 60)
        d.point((x, y), fill='gray')
        
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

@app.route('/api/keypad', methods=['GET'])
def get_keypad():
    session_id = str(uuid.uuid4())
    
    # 숫자 0~9와 빈칸 2개
    nums = [str(i) for i in range(10)] + [' ', ' ']
    random.shuffle(nums)
    
    keypad_data = []
    for num in nums:
        if num == ' ':
            img_data = text_to_image_base64(" ")
            hash_value = "empty" # 빈칸은 해시값 대신 식별자
        else:
            img_data = text_to_image_base64(num)
            # 해시 생성: sha256( 세션ID + 숫자 )
            salt_value = session_id + num
            hash_value = hashlib.sha256(salt_value.encode()).hexdigest()
        
        keypad_data.append({
            'image': img_data,
            'hash': hash_value
        })

    print(f"✅ 키패드 생성 완료! (세션: {session_id})")
    return jsonify({'session_id': session_id, 'layout': keypad_data})

# ▼▼▼ [추가된 부분] 프론트에서 입력값을 받는 곳 ▼▼▼
@app.route('/api/submit', methods=['POST'])
def submit_password():
    data = request.json
    print("\n[📥 데이터 수신]")
    print(f" - 세션 ID: {data.get('session_id')}")
    print(f" - 입력된 해시값들: {data.get('input_hashes')}")
    
    # 여기서 나중에 '복호화' 로직을 수행하면 됩니다.
    
    return jsonify({"message": "비밀번호가 서버에 잘 도착했습니다!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)