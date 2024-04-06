from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os

app = FastAPI()

@app.post("/detection")
async def detect_objects(file: UploadFile = File(...)):
    
    # 이미지를 저장할 디렉토리 생성
    os.makedirs('./input_dir', exist_ok=True)

    # 이미지 파일의 경로 설정
    filename = secure_filename(file.filename)
    file_path = os.path.join('./input_dir', filename)

    # 이미지 파일 저장
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # YOLO 모델 초기화
    model = YOLO('./runs/detect/train/weights/best2.pt')
    results = model.predict(file_path, save=True, imgsz=640, conf=0.3)

    # 객체 인식 결과를 리스트로 저장
    output_labels = [model.names.get(box.cls.item()) for box in results[0].boxes]

    return JSONResponse(content={"labels": output_labels}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)