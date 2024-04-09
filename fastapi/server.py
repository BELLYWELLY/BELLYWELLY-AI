from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request 
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os
import requests

app = FastAPI()

@app.post("/detection")
async def detect_objects(request: Request):
    try:
        # 요청 바디 파싱
        body = await request.json()
        image_url = body.get("imageUrl") # 카멜케이스로 수정

        # 이미지를 다운로드하여 저장할 디렉토리 생성
        os.makedirs('./input_dir', exist_ok=True)

        # 이미지 파일의 이름 설정
        filename = secure_filename("input_image.jpg")
        file_path = os.path.join('./input_dir', filename)

        # 이미지 다운로드
        response = requests.get(image_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # YOLO 모델 초기화
        model = YOLO('./demobest.pt')
        results = model.predict(file_path, save=True, imgsz=640, conf=0.3)

        # 객체 인식 결과 중 중복은 제거하고 유니크한 결과만 남기도록 코드 수정
        # output_labels = [model.names.get(box.cls.item()) for box in results[0].boxes]
        unique_labels = []
        for box in results[0].boxes:
            label = model.names.get(box.cls.item())
            if label not in unique_labels:
                unique_labels.append(label)

        return JSONResponse(content={"labels": unique_labels}, status_code=200)

    except Exception as e:
        # 오류 발생시 예외 처리
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)