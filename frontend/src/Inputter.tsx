import React, { useEffect, useState } from "react"
import "./Inputter.css"

const PASSWORD_MAX_LENGTH = 4
const API_BASE = "http://localhost:5000"

type KeypadCell = {
  image: string
  hash: string
}

export default function Inputter() {
  const [sessionId, setSessionId] = useState("")
  const [layout, setLayout] = useState<KeypadCell[]>([])
  const [inputHashes, setInputHashes] = useState<string[]>([])

  // 1) 페이지 켜지면 키패드 가져오기
  useEffect(() => {
    loadKeypad()
  }, [])

  async function loadKeypad() {
    try {
      const res = await fetch(`${API_BASE}/api/keypad`)
      const data = await res.json()

      setSessionId(data.session_id)
      setLayout(data.layout)
      setInputHashes([]) // 새 키패드면 입력 초기화
    } catch (e) {
      console.error(e)
      alert("키패드 로딩 실패! 백엔드 실행/주소 확인")
    }
  }

  // 2) 키 하나 클릭하면 해시 저장
  function onClickKey(cell: KeypadCell) {
    if (cell.hash === "empty") return
    if (inputHashes.length >= PASSWORD_MAX_LENGTH) return

    setInputHashes([...inputHashes, cell.hash])
  }

  function eraseOne() {
    setInputHashes(inputHashes.slice(0, inputHashes.length - 1))
  }

  function eraseAll() {
    setInputHashes([])
  }

  // 3) 서버로 제출
  async function submit() {
    if (!sessionId) return alert("세션이 없습니다. Reload Keypad 눌러주세요.")
    if (inputHashes.length === 0) return alert("비밀번호를 입력하세요!")

    const res = await fetch(`${API_BASE}/api/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        input_hashes: inputHashes,
      }),
    })

    const data = await res.json()
    alert(data.message ?? "서버 응답 받음")
  }

  return (
    <>
      {/* 입력 길이만 보여주기 */}
      <input
        className="password-container"
        type="password"
        value={"•".repeat(inputHashes.length)}
        readOnly
      />

      <div className="inputter__flex">
        {layout.map((cell, i) => (
          <button
            key={i}
            className="num-button__flex"
            onClick={() => onClickKey(cell)}
            disabled={cell.hash === "empty"}
            type="button"
          >
            <img src={cell.image} alt="key" />
          </button>
        ))}

        {/* 기능 버튼들 */}
        <button className="num-button__flex" onClick={eraseOne} type="button">
          ←
        </button>
      </div>

      <div>
        <button className="submit-button" onClick={submit} type="button">
          Submit
        </button>
        <button className="submit-button" onClick={loadKeypad} type="button">
          Reload Keypad
        </button>
      </div>
    </>
  )
}