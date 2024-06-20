import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

load_dotenv()

# openai-key 설정
OPENAI_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL = "gpt-4o"

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
        print(f"Error in post_gpt: {e}")
        return None

# 종합 보고서 생성 함수
def create_total_report(content: List[str], isLowFodmap: List[bool], defecation: List[int], stress: List[int]) -> str: # 레포트 - 음식/배변/스트레스 총평
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome (IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 다음 음식 리스트는 사용자가 일주일동안 먹은 식단이고, 그 식단의 음식에 대한 저포드맵 여부, 배변 점수, 스트레스 점수를 기반으로 사용자 개인별로 장건강을 개선하기 위한 종합 보고서를 작성해줘; 식단을 하나하나 분석하기 보다는 전반적인 식단과 배변, 스트레스의 연관성을 기반으로 작성해줘; '###'이나 '****'와 같은 굵게 표시하는 강조 표현 없이 작성해줘; 850byte 내로 작성해줘;\n\n"
    ex_prompt = "예시로는 다음과 같아; 이번 주 식단의 경우에는 식이섬유와 유익균을 공급하여 장건강을 개선시킬 수 있는 음식을 섭취하였습니다. ~~과 ~~은 고단백 식품으로 에너지를 제공하지만 ~~, ~~와 같은 고지방과 매운 음식은 소화에 부정적 영향을 끼칠 수 있어 주의가 필요합니다. 배변 점수 분석 결과 배변 빈도, 색깔, 긴박감, 형태를 고려할 때 50점 이하의 배변 점수는 규칙적인 배변 시간과 물 섭취 증가로 개선이 가능합니다. 스트레스 척도 분석을 통해 스트레스가 높을 때 배변 점수가 낮아지는 경향을 발견했으며 명상, 요가, 규칙적인 운동을 통해 스트레스 수준을 낮추는 것이 중요합니다. 이를 통해 과민대장증후군 개선과 전반적인 장건강 증진에 기여할 수 있습니다."
    food_str = ", ".join([f"{f} (저포드맵: {isLowFodmap[i]})" for i, f in enumerate(content)])
    defecation_str = ", ".join(map(str, defecation))
    stress_str = ", ".join(map(str, stress))

    user_content = (
        f"음식 리스트: {food_str}\n"
        f"배변 점수: {defecation_str}\n"
        f"스트레스 점수: {stress_str}\n"
        f"이 데이터를 기반으로 종합적인 보고서를 작성해줘."
    )

    answer = post_gpt(system_content, pre_prompt + ex_prompt + user_content, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return answer

# 종합 보고서 생성 함수
def create_total_report(content: List[str], isLowFodmap: List[bool], defecation: List[int], stress: List[int]) -> str:
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome (IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 다음 음식 리스트는 사용자가 일주일동안 먹은 식단이고, 그 식단의 음식에 대한 저포드맵 여부, 배변 점수, 스트레스 점수를 기반으로 사용자 개인별로 장건강을 개선하기 위한 종합 보고서를 작성해줘; 식단을 하나하나 분석하기 보다는 전반적인 식단과 배변, 스트레스의 연관성을 기반으로 작성해줘; '###'이나 '****'와 같은 굵게 표시하는 강조 표현 없이 작성해줘; 850byte 내로 작성해줘;\n\n"
    ex_prompt = "예시로는 다음과 같아; 이번 주 식단의 경우에는 식이섬유와 유익균을 공급하여 장건강을 개선시킬 수 있는 음식을 섭취하였습니다. ~~과 ~~은 고단백 식품으로 에너지를 제공하지만 ~~, ~~와 같은 고지방과 매운 음식은 소화에 부정적 영향을 끼칠 수 있어 주의가 필요합니다. 배변 점수 분석 결과 배변 빈도, 색깔, 긴박감, 형태를 고려할 때 50점 이하의 배변 점수는 규칙적인 배변 시간과 물 섭취 증가로 개선이 가능합니다. 스트레스 척도 분석을 통해 스트레스가 높을 때 배변 점수가 낮아지는 경향을 발견했으며 명상, 요가, 규칙적인 운동을 통해 스트레스 수준을 낮추는 것이 중요합니다. 이를 통해 과민대장증후군 개선과 전반적인 장건강 증진에 기여할 수 있습니다."
    food_str = ", ".join([f"{f} (저포드맵: {isLowFodmap[i]})" for i, f in enumerate(content)])
    defecation_str = ", ".join(map(str, defecation))
    stress_str = ", ".join(map(str, stress))

    user_content = (
        f"음식 리스트: {food_str}\n"
        f"배변 점수: {defecation_str}\n"
        f"스트레스 점수: {stress_str}\n"
        f"이 데이터를 기반으로 종합적인 보고서를 작성해줘."
    )

    answer = post_gpt(system_content, pre_prompt + ex_prompt + user_content, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return answer

def get_default_diet_recommendation(): # 채팅 - 기본 식단(default) 추천
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome (IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 일반적인 과민대장증후군(IBS)에 좋은 식단을 추천해줘; 밥, 국, 메인 메뉴(예를 들면, 고등어구이, 목살숙주볶음 등), 반찬(예를 들면, 시금치무침, 콩나물무침, 두부구이 등), 과일을 하나씩 골라서 하나의 식단을 완성하여 추천해줘; 근거는 간단하게 1줄로 영양사가 조언해주는 느낌으로 작성해줘; 강조 표현 없이 작성해줘; ';'표시 없이 깔끔하게 '음식: 설명' 이런식으로 작성해줘;\n\n"
    ex_prompt = "예시로는 다음과 같아; 현미밥 - 식이섬유가 풍부하여 장 건강에 도움을 줍니다 \n 미소 된장국 - 소화를 돕는 성분이 포함되어있습니다 \n 닭가슴살 구이 - 저지방 고단백 식품으로 장에 부담이 적고 소화가 잘 됩니다 \n 시금치무침 - 저포드맵 성분으로 과민대장증후군 증상을 완화합니다 \n 바나나 - 저포드맵 과일로 포만감이 좋고 소화가 잘 됩니다."
    langchain_prompt = (
        "Diet recommendation prompt: Based on general dietary guidelines for irritable bowel syndrome (IBS), recommend a balanced diet that includes one type of rice, one soup, one type of kimchi, and one side dish. Ensure the diet is low in high-FODMAP foods and promotes gastrointestinal health."
    )
    answer = post_gpt(system_content, pre_prompt + ex_prompt + langchain_prompt, GPT_MODEL)
    
    return answer

def create_diet_recommendation_prompt(prompt): # 채팅 - 식단 추천
    prompt_str = ", ".join(prompt) 
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 사용자가 일주일동안 다음과 같은 음식 리스트를 먹었는데, 이 음식 리스트를 기반으로 앞으로 사용자의 장건강 및 과민대장증후군을 개선해줄 수 있는 식단 하나를 추천해줘; 밥, 국, 메인 메뉴(예를 들면, 고등어구이, 목살숙주볶음 등), 반찬(예를 들면, 시금치무침, 콩나물무침, 두부구이 등), 과일을 하나씩 골라서 하나의 식단을 완성하여 추천해줘; 근거는 간단하게 1줄로 영양사가 조언해주는 느낌으로 작성해줘; 강조 표현 없이 작성해줘; ';'표시 없이 깔끔하게 '음식: 설명' 이런식으로 작성해줘;\n\n"
    ex_prompt = "예시로는 다음과 같아; 현미밥 - 식이섬유가 풍부하여 장 건강에 도움을 줍니다 \n 미소 된장국 - 소화를 돕는 성분이 포함되어있습니다 \n 닭가슴살 구이 - 저지방 고단백 식품으로 장에 부담이 적고 소화가 잘 됩니다 \n 시금치무침 - 저포드맵 성분으로 과민대장증후군 증상을 완화합니다 \n 바나나 - 저포드맵 과일로 포만감이 좋고 소화가 잘 됩니다."
    langchain_prompt = (
        "Diet recommendation prompt: Today's diet recommendation! After analyzing today's meals, it seems that {insert analysis of today's carbohydrate, protein, and sugar intake, e.g., 'the carbohydrate and sugar intake is high, while protein intake is insufficient.'} Additionally, {insert explanation whether the consumed foods are mainly high-FODMAP or low-FODMAP, e.g., 'there are many high-FODMAP foods consumed, indicating vulnerability to digestive health issues.'} Let me recommend a diet that can help improve your gastrointestinal health! [Diet Recommendation] {recommend a diet plan that can improve the user's digestive health and alleviate symptoms of irritable bowel syndrome (IBS); include one rice, one soup, one kimchi, and one side dish (e.g., 'barley rice, bean sprout soup, cabbage kimchi, stir-fried eggplant').}"
    )
    answer = post_gpt(system_content, pre_prompt + ex_prompt + langchain_prompt + prompt_str, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    formatted_answer = answer.replace("[식단 추천]", "\n[식단 추천]\n")

    return formatted_answer

def create_food_choice_prompt(prompt): # 채팅 - 음식 고르기
    prompt_str = ", ".join(prompt) 
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome(IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 포드맵은 장에서 흡수되지 않고 쉽게 발효되어 설사, 복통, 복부팽만을 유발하는 올리고당, 이당류, 단당류, 폴리올을 일컫는 말입니다. 사용자가 두 가지 음식을 제안하였을 때, 두 가지 음식의 포드맵 정보를 바탕으로 장건강 개선에 도움이 되는 음식을 선택해주고, 간단하게 근거를 한 줄로 설명해줘; 강조 표현 없이 작성해줘;\n\n"
    langchain_prompt = (
        "Food choice prompt: The user has proposed two different foods. Based on the FODMAP information of these two foods, choose the one that would be more beneficial for improving digestive health. Also provide a brief explanation for your choice."
    )
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt_str, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer]

def rank_foods_by_health(prompt: List[str]) -> Dict[str, Any]: # 레포트 - 장건강 관련 음식 순위 매기기
    prompt_str = ", ".join(prompt)
    system_content = "You are the foremost expert in nutrition on the planet, particularly in the field of irritable bowel syndrome (IBS), through relentless research, you've attained the top position in the realm of gastrointestinal studies."
    pre_prompt = "한국어로 답변해줘; 포드맵은 장에서 흡수되지 않고 쉽게 발효되어 설사, 복통, 복부팽만을 유발하는 올리고당, 이당류, 단당류, 폴리올을 일컫는 말입니다. 다음 음식 리스트를 바탕으로 장건강에 좋은 음식 5가지와 좋지 않은 음식 5가지를 순위별로 매겨주고, 각 음식이 왜 좋은지/좋지 않은지 간단하게 한 줄로 설명해줘. 만약 음식 리스트가 10개 미만이라면, 리스트의 절반만큼 Best와 Worst로 나누어 순위 매겨줘; 부연 설명 없이 순위와 음식 이름, 이에 대한 한 줄의 근거만 작성해줘; 강조 표현 없이 작성해줘; \n\n"
    langchain_prompt = "Food ranking prompt: Based on the provided list of foods, rank the top 5 foods that are best for digestive health and the top 5 foods that are worst for digestive health, considering their FODMAP content. Provide a brief explanation for why each food is good or bad for digestive health. If the list has fewer than 10 foods, rank half of them as best and the other half as worst;\n\n"
    ex_prompt = "Best:\n1. 바나나: 바나나는 저포드맵 음식으로, 과민대장증후군에 도움이 됩니다.\n2. 브로콜리: 브로콜리는 식이섬유가 풍부하여 장 건강에 유익합니다.\n3. 양배추: 양배추는 장을 진정시키고 염증을 줄이는 데 도움이 됩니다.\n4. 아몬드: 아몬드는 건강한 지방과 단백질이 많아 장 건강에 좋습니다.\n5. 사과: 사과는 섬유질이 풍부하여 소화를 돕습니다.\n\nWorst:\n1. 빵: 빵은 고포드맵 음식으로 장에 부담을 줄 수 있습니다.\n2. 우유: 우유는 유당을 포함하여 장에서 발효될 수 있습니다.\n3. 마늘: 마늘은 고포드맵 음식으로 과민대장증후군에 악영향을 미칠 수 있습니다."
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + ex_prompt + prompt_str, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    print("GPT 응답:", answer)  # GPT 응답 출력
    parsed_response = parse_gpt_response(answer)
    print("파싱된 응답:", parsed_response)  # 파싱된 응답 출력
    
    return parsed_response

# GPT 응답을 파싱하는 함수
def parse_gpt_response(response: str) -> Dict[str, Any]:
    best = []
    worst = []
    lines = response.split("\n")

    current_list = None
    for line in lines:
        line = line.strip()
        if line.startswith("Best"):
            current_list = best
        elif line.startswith("Worst"):
            current_list = worst
        elif line and current_list is not None:
            parts = line.split(":")
            if len(parts) == 2:
                name = parts[0].split(".")[1].strip()
                desc = parts[1].strip()
                current_list.append({"name": name, "desc": desc})
    
    return {
        "best": best,
        "worst": worst
    }

def create_defecation_report_prompt(defecation_scores: List[int]): # 레포트 - 배변
    prompt_str = ", ".join(map(str, defecation_scores))
    system_content = "You are the foremost expert in digestive health and gastrointestinal studies. Based on extensive research, you have attained the top position in the field."
    pre_prompt = "한국어로 답변해줘; 사용자의 일주일간 배변 점수를 보고 배변 점수에 대한 총평을 작성해줘; 사용자가 선택한 배변 빈도와 배변 색깔, 배변 긴박감 및 배변 형태도 배변 점수에 유의미한 영향을 끼친다는 점을 고려하여 배변 점수의 경향성을 중점적으로 반영하여 작성해줘; 모두에게 적용되는 너무 뻔한 내용 말고, 사용자의 점수를 보고 개인별로 도움이 될 수 있는 배변 조언을 해줘; 강조 표현 없이 작성해줘; 150자 정도로 핵심 위주로 작성해줘; \n\n"       
    answer = post_gpt(system_content, pre_prompt + prompt_str, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return answer

def create_stress_report_prompt(defecation_scores: List[int], stress_scores: List[int]): # 레포트 - 스트레스
    defecation_prompt_str = ", ".join(map(str, defecation_scores))
    stress_prompt_str = ", ".join(map(str, stress_scores))
    system_content = "You are the foremost expert in digestive health and stress management. Based on extensive research, you have attained the top position in these fields."
    pre_prompt = "한국어로 답변해줘; 사용자의 일주일간 스트레스 점수를 보고 스트레스 점수에 대한 총평을 작성해줘. 또한, 장 건강과 스트레스의 관계를 설명하고, 장 건강 개선에 있어서 스트레스를 줄이는 것의 중요성에 대해서 조언해줘; 강조 표현 없이 작성해줘; 150자 정도로 핵심 위주로 작성해줘; \n\n"
    combined_prompt = f"Defecation scores: {defecation_prompt_str}\nStress scores: {stress_prompt_str}"
    answer = post_gpt(system_content, pre_prompt + combined_prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return answer