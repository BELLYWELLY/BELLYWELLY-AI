from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from typing import List, Optional
from pydantic import BaseModel
from intoGPT import create_total_report, create_diet_recommendation_prompt, create_food_choice_prompt, get_default_diet_recommendation, rank_foods_by_health, create_defecation_report_prompt, create_stress_report_prompt

import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

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

class RequestFoodReport(BaseModel):
    content: List[str] 

class RequestFoodReportRank(BaseModel):
    content: List[str] 

class FoodPrompt(BaseModel):
    content: Optional[List[str]]

class RequestDefecationReport(BaseModel):
    defecation: List[int]
    stress: List[int]

class RequestTotalReport(BaseModel):
    content: List[str]
    isLowFodmap: List[bool]
    defecation: List[int]
    stress: List[int]

@app.post("/report")
def report_total(data: RequestTotalReport): # 레포트 - 음식/배변/스트레스 총평
    try:
        if not data.content or not data.isLowFodmap or not data.defecation or not data.stress:
            raise HTTPException(status_code=400, detail="Request body is incomplete")

        content = create_total_report(data.content, data.isLowFodmap, data.defecation, data.stress)
        response_data = {
            "status": 200,
            "data": content
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": "An error occurred while processing the request."
        }
    return JSONResponse(content=response_data)

@app.post("/recommend") # 채팅 - 식단 추천
async def recommend_food(prompt: FoodPrompt):
    if prompt.content is None:
        content = get_default_diet_recommendation()
    else:
        try:
            content = create_diet_recommendation_prompt(prompt.content)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    response_data = {
        "status": 200,
        "data": content
    }
    
    return JSONResponse(content=response_data)

@app.post("/choice") # 채팅 - 음식 고르기
def choice_food(data: RequestFoodReport):
    try:
        if not data.content:
            raise HTTPException(status_code=400, detail="Request content is empty")

        content = create_food_choice_prompt(data.content)
        response_data = {
            "status": 200,
            "data": content
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": "An error occurred while processing the request."
        }
    return JSONResponse(content=response_data)

@app.post("/report/food") # 레포트 - 장건강 관련 음식 순위 매기기
def report_food(data: RequestFoodReportRank):
    try:
        if not data.food:
            raise HTTPException(status_code=400, detail="Request food is empty")
        
        content = rank_foods_by_health(data.food)
        response_data = {
            "status": 200,
            "data": content
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": "An error occurred while processing the request."
        }
    return JSONResponse(content=response_data)

@app.post("/report/defecation") # 레포트 - 배변
def report_defecation(data: RequestDefecationReport):
    try:
        if not data.defecation:
            raise HTTPException(status_code=400, detail="Request defecation data is empty")

        content = create_defecation_report_prompt(data.defecation)
        response_data = {
            "status": 200,
            "data": content
        }
    except ValueError as ve:
        response_data = {
            "status": 400,
            "data": str(ve)
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": f"An error occurred while processing the request: {str(e)}"
        }
    return JSONResponse(content=response_data)

@app.post("/report/stress")
def report_stress(data: RequestDefecationReport): # 레포트 - 스트레스
    try:
        if not data.defecation:
            raise HTTPException(status_code=400, detail="Request defecation data is empty")
        if not data.stress:
            raise HTTPException(status_code=400, detail="Request stress data is empty")

        content = create_stress_report_prompt(data.defecation, data.stress)
        response_data = {
            "status": 200,
            "data": content
        }
    except ValueError as ve:
        response_data = {
            "status": 400,
            "data": str(ve)
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": f"An error occurred while processing the request: {str(e)}"
        }
    return JSONResponse(content=response_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)