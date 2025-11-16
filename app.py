import time
import random
import numpy as np
# 'send_from_directory'를 임포트에 추가합니다.
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Flask 앱 초기화
app = Flask(__name__)

# -----------------------------------------------------------------
# ✨ CORS 설정 수정 ✨
# -----------------------------------------------------------------
# (기존) CORS(app) <-- 이 줄을 아래 코드로 대체합니다.

# VSCode Live Server의 기본 포트(5500, 5501 등)를 명시적으로 허용합니다.
# 본인의 Live Server 포트가 다르면 목록에 추가해주세요. (포트 확인은 VSCode 우측 하단)
allowed_origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501", # 5500 포트가 사용 중일 때 5501을 쓰기도 합니다.
    "http://localhost:5501"
]
# 특정 API 경로(/simulate)에 대해 위 origin들만 허용하도록 설정
CORS(app, resources={r"/simulate": {"origins": allowed_origins}})
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# ✨ index.html 파일을 서빙하는 라우트(경로) 추가 ✨
# -----------------------------------------------------------------
@app.route('/')
def serve_index():
    """
    웹사이트의 메인 페이지 (http://127.0.0.1:5000) 접속 시
    'index.html' 파일을 찾아서 보내줍니다.
    """
    # '.'는 현재 디렉토리를 의미합니다.
    return send_from_directory('.', 'index.html')
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# ✨ 사용자분의 실제 모델 코드가 들어갈 자리 ✨
# -----------------------------------------------------------------
def run_simulation(qubits, strength, model):
    """
    사용자(개발자)가 실제 모델로 대체해야 하는 가상 시뮬레이션 함수입니다.
    
    입력:
    - qubits (int): 큐비트 수
    - strength (float): 결합 강도
    - model (str): 선택된 모델 이름 (예: "GCN", "GAT")
    
    반환:
    - dict: 시뮬레이션 결과 (펄스 데이터 및 3가지 핵심 지표)
    """
    
    # [가상 로직 1: 최적 펄스 생성]
    # (실제로는 복잡한 연산 결과이겠지만, 여기서는 가상의 시계열 데이터를 생성합니다.)
    # 펄스 길이를 50 스텝으로 고정
    pulse_steps = 50
    # Numpy를 사용해 부드러운 펄스 모양(예: sin + noise)을 만듭니다.
    base_pulse = np.sin(np.linspace(0, np.pi * 2, pulse_steps)) * strength
    noise = np.random.randn(pulse_steps) * 0.1 * (qubits / 50)
    optimal_pulse = base_pulse + noise
    # JSON으로 보내기 위해 list로 변환
    optimal_pulse_data = list(optimal_pulse)


    # [가상 로직 2: 결과 지표 3가지 생성]
    # (V2에서 사용했던 로직을 서버로 이전)
    final_energy = 100.0
    learning_time = 5.0
    model_params = 10000

    if model == 'MLP':
        final_energy += 30.0
        learning_time += 5.0
        model_params = 50000
    elif model == 'MLP (Set)':
        final_energy += 15.0
        learning_time += 10.0
        model_params = 80000
    elif model == 'GCN':
        final_energy -= 10.0
        learning_time += 15.0
        model_params = 150000
    elif model == 'GAT':
        final_energy -= 15.0
        learning_time += 20.0
        model_params = 250000

    final_energy += (qubits * 0.5)
    learning_time += (qubits * 0.8)
    model_params += (model_params * (qubits / 10))
    final_energy -= (strength * 5)
    learning_time += (strength * 1.2)

    # 실제 모델이 계산하는 시간을 흉내
    time.sleep(1.5) 

    # 프론트엔드로 보낼 결과 데이터 패키징
    return {
        "optimalPulse": optimal_pulse_data,
        "finalEnergy": round(final_energy, 2),
        "learningTime": round(learning_time, 1),
        "modelParams": int(model_params)
    }
# -----------------------------------------------------------------
@app.route('/simulate', methods=['POST'])
def handle_simulation():
    """
    프론트엔드로부터 시뮬레이션 요청을 받는 API 엔드포인트
    """
    try:
        # 프론트엔드가 보낸 JSON 데이터 수신
        data = request.json
        
        qubits = int(data.get('qubits', 10))
        strength = float(data.get('strength', 1.0))
        model = data.get('model', 'GCN')

        # [핵심] 실제 (가상) 시뮬레이션 실행
        results = run_simulation(qubits, strength, model)

        # 결과를 JSON 형태로 프론트엔드에 반환
        return jsonify(results)

    except Exception as e:
        # 에러 발생 시
        print(f"Error during simulation: {e}")
        return jsonify({"error": str(e)}), 500


# 이 스크립트가 직접 실행될 때 (예: 'python app.py') 서버를 구동
if __name__ == '__main__':
    app.run(debug=True, port=5000)