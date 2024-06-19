# BellyWelly-AI
![image](https://github.com/BellyWelly/BellyWelly-AI/assets/96541582/c87f227e-930c-406d-ba55-b52a610354af)
<br>

## 💡 프로젝트 개요
현대 사회에 불규칙적인 생활 패턴과 스트레스로 인해 장 건강에 큰 영향을 받는 사람들이 점차 증가하고 있습니다. 국내에서 연간 약 150만명의 과민대장증후군 환자가 발생했고, 이들은 일상 생활에 큰 불편을 겪고 있습니다.

대부분의 사람들은 자신의 장 건강 상태를 정확하게 알지 못하며, 자신에게 맞는 건강한 식습관과 생활 패턴을 구축하는 것에 어려움을 느끼고 있습니다. 하지만 이들의 문제를 해결할 수 있는 사용성 좋은 어플리케이션은 현재 부재합니다.

따라서, 사용자 개개인의 식습관, 배변 상태, 스트레스 지수 등을 효과적으로 기록하고 분석하여, 개인별 맞춤형 건강 관리 방안을 제공할 수 있는 서비스의 필요성이 점점 커지고 있기에, 과민대장증후군 개선을 위한 헬스케어 서비스를 제안합니다. 
<br>

## ⚙️ 서비스 아키텍쳐 
![image](https://github.com/BellyWelly/BellyWelly-AI/assets/96541582/263faceb-897e-4ebd-b394-9af55a8fb736)

AI 시스템은 **FastAPI**를 사용하여, 텐센트 클라우드에서 학습한 **YOLOv8** 모델과 **OpenAI API**를 서빙하며 이 시스템은 Docker 환경에서 실행됨. **OpenAI API**는 **CoT(Chain of Thought) 전략**과 **LangChain** 기술을 적용하여, LLM(Large Language Model)에 Query와 Prompt를 전달하고, LLM의 응답을 받음
<br>

## ⚙️ 사용한 오픈소스
- FastAPI는 Python 기반의 웹 프레임워크로, 빠르고 쉽게 API를 구축하며 비동기 I/O 지원, 데이터 유효성 검사, 자동 문서 생성
- PyTorch는 딥러닝 모델을 구축하고 학습 시키는데 사용함
- YOLO는 실시간 객체 탐지 알고리즘으로, 최신 버전인 YOLOv8을 통해 더 높은 정확도와 빠른 속도를 보이며 이미지에서 객체를 빠르고 정확하게 탐지함
- Ultralytics는 YOLOv8의 개발과 배포를 담당하며 YOLO 모델을 학습, 평가, 배포하는데 필요한 다양한 도구를 제공함
- CUDA는 NVIDIA의 GPU를 사용한 병렬 계산 플랫폼으로, NVIDIA의 최신 GPU 아키텍처를 지원하며 더 빠른 연산 성능과 효율적인 메모리 사용을 제공
- OpenCV(Open Source Computer Vision Library)는 실시간 컴퓨터 비전을 위한 라이브러리로 객체 탐지 작업을 수행함
- OpenAI는 GPT 모델과 상호작용할 수 있는 라이브러리로 프롬프트 생성 및 관련 로직을 포함
- pydantic는 데이터 검증 및 설정을 위한 데이터 클래스 라이브러리로 데이터 검증 및 스키마 정의에 사용함

## 📁 프로젝트 폴더 구조
```
📂 BellyWelly-AI
    └── BellyWelly-AI
        ├── fastapi
        │   ├── ultralytics 
        │   ├── runs
        │   ├── input_dir
        │   ├── demobest.pt
        │   ├── main.py
        │   ├── server.py
        │   └── intoGPT.py
        ├── requirements
        ├── Dockerfile
        └── test_image 
```

## 🔧 객체 탐지 모델 구현  
### 개발 환경 셋업 
> 클라우드 : Tencent Cloud <br>
> OS: Ubuntu Server 20.04 LTS 64bit (& Window 10) <br>
> GPU: Tesla T4, CUDA: 11.8, cuDNN: 8.7.0, PyTorch: 2.2.2+cu118 <br>

### 모델 훈련 및 가중치 생성 
- YOLOv8 모델을 Roboflow로 생성한 데이터셋을 활용하여 epochs=100으로 훈련
- 훈련된 모델로부터 가중치가 담긴 best.pt 파일 생성

### FastAPI를 통한 서버 구축
- 클라이언트로부터 받은 URL로 해당 이미지를 다운로드 하고, 파일 시스템에 저장
- 다운로드한 이미지를 YOLOv8 모델에 입력으로 제공하여 객체 탐지

### AI 모델 배포 
- 모델을 초기화하고, 객체 탐지하고 라벨을 리스트로 저장하여 JSON형식으로 반환
- Docker을 사용하여 서비스를 컨테이너화하여 배포하며 라벨을 반환
- 배포된 서비스는 https://model.bellywelly.kro.kr/detection 에서 접근 가능
<br>

## 🔧 설치 및 실행 방법

**(1) 레포지토리 클론** 
```
git clone https://github.com/BellyWelly/BellyWelly-AI.git
cd BellyWelly-AI
```

**(2) 필요한 Python 패키지 설치** 

BellyWelly 프로젝트를 실행하기 위해서는 requirement.txt 파일에 명시된 패키지를 설치해야 합니다. 
```
pip install -r requirements.txt
```

**(3) Docker 이미지 필드 및 컨테이너 실행** 
```
docker build -t bellywelly-ai .
docker run --gpus all -p 8000:8000 bellywelly-ai
```

**(4) URL을 통한 서버 접근**  
배포된 서비스 URL 주소: https://model.bellywelly.kro.kr/detection

**(5) 샘플 데이터를 이용하여 Request 요청**  
샘플 데이터는 프로젝트 폴더 내 `test_image 디렉토리`에 포함되어 있습니다.
다음과 같은 JSON 데이터를 https://model.bellywelly.kro.kr/detection 엔드포인트에 POST 요청으로 보냅니다.
```json
{
    "imageUrl": "https://m.62life.com/images/gdimg/p_1(411).jpg"
}
```

## 📊 YOLOv8 모델 성능 평가

**(1) 모델이 얼마나 정확하게 객체를 탐지하고 분류하는지에 대한 측정** 
![image](https://github.com/BellyWelly/BellyWelly-AI/assets/96541582/c68c3acf-4d5b-435e-b455-8a08e202e3f3)
- **Precision(모델이 올바르게 감지한 객체의 비율)**: 0.8699
- **Recall(모델이 실제 객체 중 올바르게 감지한 비율)**: 0.8519
- **mAP(Mean Average Precision, 다양한 임계값에서의 평균 정밀도)**: 0.8879

**(2) 모델 효율성 측정** 

객관적인 평가를 위해 데이터셋 분리, 평가 환경 통제, 반복 측정을 토대로 평가 진행하였습니다.
- 추론 시간: 이미지 한 장을 처리하는 데 걸리는 시간으로 평균 1.765s 시간 소요
- 메모리 사용량: 모델이 추론 시 사용하는 메모리 양으로 평균 253.2B 메모리 사용
<br>

## 📕 향후 과제 및 개선 방향
BellyWelly는 지속적인 기능 강화와 사용자 경험 개선을 목표로 하고 있습니다. AI 챗봇 기능을 사용자 맞춤형으로 정교화하고, 과민대장증후군 관리 솔루션을 더욱 효과적으로 제공하는 데 집중할 것입니다. 또한, 스마트 워치와 연동하여 사용자의 운동 기록 및 수면 기록 등을 주간 레포트에 반영함으로써 BellyWelly의 유용성을 더욱 향상할 것입니다.

지속적인 사용자 피드백을 반영하여 서비스 품질을 향상시키고, 고객의 니즈에 맞춘 서비스를 제공할 예정이며 나아가 BellyWelly는 추후 이미지 인식 기술과 챗봇 기술 등을 활용하여 타겟 시장을 확장할 계획입니다. 현재는 과민대장증후군 관리를 중심으로 서비스를 제공하고 있지만, 향후 당뇨, 만성 위염, 다이어트와 같이 다양한 이유로 생활 습관을 꾸준하게 관리해야 하는 사람들을 위한 기능을 추가하여 더욱 많은 사람들이 사용할 수 있는 서비스로 거듭날 것입니다.
<br>
