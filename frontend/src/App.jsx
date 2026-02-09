import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [keypadData, setKeypadData] = useState([]);
  const [sessionId, setSessionId] = useState("");
  
  // ★ 추가된 부분 1: 입력한 해시값들을 저장할 배열
  const [inputHashes, setInputHashes] = useState([]); 

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/keypad')
      .then(response => {
        setKeypadData(response.data.layout);
        setSessionId(response.data.session_id);
      })
      .catch(error => alert("서버 연결 실패"));
  }, []);

  // ★ 추가된 부분 2: 클릭 시 alert 대신 배열에 저장
  const handleClick = (hashValue) => {
    setInputHashes(prev => [...prev, hashValue]);
    console.log("현재 입력값:", [...inputHashes, hashValue]); // 확인용 로그
  };

  // ★ 추가된 부분 3: 다 입력했으면 콘솔에 출력 (나중에 전송할 곳)
  const handleSubmit = () => {
    alert("입력 완료");
    console.log("전송할 데이터:", {
        session_id: sessionId,
        input_hashes: inputHashes
    });
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'Arial' }}>
      <h1>E2E 키패드</h1>
      
      {/* 입력 상태 표시 (심플하게) */}
      <h3>입력된 개수: {inputHashes.length}개</h3>

      <div style={{ 
        display: 'grid', gridTemplateColumns: 'repeat(3, 100px)', gap: '10px', 
        justifyContent: 'center', margin: '30px auto'
      }}>
        {keypadData.map((item, index) => (
          <div key={index} 
            onClick={() => handleClick(item.hash)} 
            style={{ width: '100px', height: '100px', border: '1px solid #ccc', cursor: 'pointer' }}
          >
            <img src={item.image} alt="key" style={{ width: '100%', height: '100%' }} />
          </div>
        ))}
      </div>

      <button onClick={() => setInputHashes([])}>지우기</button>
      <button onClick={handleSubmit} style={{ marginLeft: '10px' }}>입력 완료</button>
    </div>
  );
}

export default App;