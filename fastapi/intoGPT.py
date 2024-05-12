import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# openai-key 설정
OPENAI_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL = "gpt-3.5-turbo"

# 프롬프트 작성 
def post_gpt(system_content, user_content, model_name):
    try:
        client = OpenAI(api_key=OPENAI_KEY)  # 클라이언트 인스턴스화
        # 'messages' 인자 구성
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        # 새로운 인터페이스 사용
        completion = client.chat.completions.create(  # 클래스 이름 변경
            model=model_name,
            messages=messages,  # 여기에 'messages' 인자를 제공
            max_tokens=3000,
            temperature=0.5
            # 'stop' 인자는 필요에 따라 설정
        )
        answer = completion.choices[0].message.content.strip()
        print("gpt 답변: " + answer)
        return answer
    except Exception as e:
        print(e)
        return None
    
def create_prediction_prompt(prompt):
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies. "
    pre_prompt = "한국어로 답변해줘; 해당 음식 리스트를 보고 장건강과 관련하여 사용자에게 장건강을 개선해주는 식단 보고서를 작성해줘;\n\n"
    langchain_prompt = "Prediction prompt: Consider the provided food list and provide a dietary report focusing on improving the user's digestive health. Your response should be tailored to the user's gastrointestinal concerns, especially irritable bowel syndrome (IBS), and include recommendations based on your expertise in nutrition. Ensure the dietary plan is comprehensive and promotes gastrointestinal well-being. Please provide your response in Korean."
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer]

def create_diet_recommendation_prompt(prompt):
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 사용자가 일주일동안 다음과 같은 음식 리스트를 먹었는데, 이 음식 리스트를 기반으로 앞으로 사용자의 장건강 및 과민대장증후군을 개선해줄 수 있는 식단 하나를 추천해줘; 밥, 국, 반찬 등 고루고루 하나의 식단을 완성하여서 추천해줘; 근거는 간단하게 2줄정도로만 친근감 있는 말투로 영양사가 조언해주는 것처럼 작성해줘.\n\n"
    langchain_prompt = "Diet recommendation prompt: Based on the provided food list, recommend a balanced diet plan to improve the user's gastrointestinal health and alleviate symptoms of irritable bowel syndrome (IBS) in the future. Your recommendations should cover a variety of food categories, including rice, soup, and side dishes, ensuring a well-rounded meal plan. Please provide your response in Korean and adopt a friendly tone similar to that of a nutritionist advising the user."
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer] 