from flask import Flask, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont # 이미지 처리 라이브러리
import io
import base64
import random
import uuid
import hashlib

app = Flask(__name__)
CORS(app)  # 리액트와 통신 허용

def text_to_image_base64(text):
    """
    텍스트(숫자)를 입력받아 노이즈가 섞인 이미지(Base64)로 변환하는 함수
    """
    # 1. 흰색 배경(60x60) 생성
    img = Image.new('RGB', (60, 60), color='white')
    d = ImageDraw.Draw(img)
    
    # 2. 텍스트 그리기 (가운데 쯤에)
    d.text((25, 20), text, fill='black') 
    
    # 3. 노이즈(점) 찍기 (봇 방지용)
    for _ in range(15):
        x = random.randint(0, 60)
        y = random.randint(0, 60)
        d.point((x, y), fill='gray')
        
    # 4. 이미지를 문자열(Base64)로 변환
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{img_str}"

@app.route('/api/keypad', methods=['GET'])
def get_keypad():
    # 1. 고유 세션 ID 생성 (이번 판의 고유 번호)
    session_id = str(uuid.uuid4())
    
    # 2. 숫자 0~9와 빈칸 2개 준비 후 섞기
    nums = [str(i) for i in range(10)] + [' ', ' ']
    random.shuffle(nums)
    
    # 3. 프론트로 보낼 데이터 조립
    keypad_data = []
    
    for num in nums:
        # A. 이미지 생성 (사용자 눈에 보일 것)
        img_data = text_to_image_base64(num)
        
        # B. 해시 생성 (프론트엔드가 가질 값)
        # 공식: sha256( 세션ID + 숫자 )
        salt_value = session_id + num
        hash_value = hashlib.sha256(salt_value.encode()).hexdigest()
        
        # C. 리스트에 추가
        keypad_data.append({
            'image': img_data,
            'hash': hash_value
        })

    print(f"✅ 키패드 생성 완료! (세션: {session_id})")
    
    # 4. JSON으로 응답
    return jsonify({
        'session_id': session_id,
        'layout': keypad_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)