import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# openai-key 설정
OPENAI_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL = "gpt-4-turbo"

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
    langchain_prompt = (
        "Prediction prompt: Consider the provided food list and provide a dietary report focusing on improving the user's digestive health. Your response should be tailored to the user's gastrointestinal concerns, especially irritable bowel syndrome (IBS), and include recommendations based on your expertise in nutrition. Ensure the dietary plan is comprehensive and promotes gastrointestinal well-being. Additionally, analyze the consumed foods for their FODMAP content and provide personalized dietary recommendations to alleviate symptoms of IBS.}"
    )
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer]

def create_diet_recommendation_prompt(prompt):
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 사용자가 일주일동안 다음과 같은 음식 리스트를 먹었는데, 이 음식 리스트를 기반으로 앞으로 사용자의 장건강 및 과민대장증후군을 개선해줄 수 있는 식단 하나를 추천해줘; 밥, 국, 반찬 등 고루고루 하나의 식단을 완성하여서 추천해줘; 근거는 간단하게 2줄정도로만 친근감 있는 말투로 영양사가 조언해주는 것처럼 작성해줘.\n\n"
    langchain_prompt = (
        "Diet recommendation prompt: Today's diet recommendation! After analyzing today's meals, it seems that {insert analysis of today's carbohydrate, protein, and sugar intake, e.g., 'the carbohydrate and sugar intake is high, while protein intake is insufficient.'} Additionally, {insert explanation whether the consumed foods are mainly high-FODMAP or low-FODMAP, e.g., 'there are many high-FODMAP foods consumed, indicating vulnerability to digestive health issues.'} Let me recommend a diet that can help improve your gastrointestinal health! [Diet Recommendation] {recommend a diet plan that can improve the user's digestive health and alleviate symptoms of irritable bowel syndrome (IBS); include one rice, one soup, one kimchi, and one side dish (e.g., 'barley rice, bean sprout soup, cabbage kimchi, stir-fried eggplant').}"
    )
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    formatted_answer = answer.replace("[식단 추천]", "\n[식단 추천]\n")

    return [formatted_answer] 

def create_food_choice_prompt(prompt):
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 포드맵은 장에서 흡수되지 않고 쉽게 발효되어 설사, 복통, 복부팽만을 유발하는 올리고당, 이당류, 단당류, 폴리올을 일컫는 말입니다. 사용자가 두 가지 음식을 제안하였을 때, 두 가지 음식의 포드맵 정보를 바탕으로 장건강 개선에 도움이 되는 음식을 선택해주고, 간단한 근거를 한두줄로 설명해줘;\n\n"
    langchain_prompt = (
        "Food choice prompt: The user has proposed two different foods. Based on the FODMAP information of these two foods, choose the one that would be more beneficial for improving digestive health. Also provide a brief explanation for your choice."
    )
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer]