from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "영어를 한국어로 번역해줘. few shot 역할을 가진자가 몇가지 구체적인 지시를 줄게"
        },
        {
            "role": "system",
            "content": "1) 다음과 같이 번역하는거야. apple -> 사과"
        },
        {
            "role": "system",
            "content": "2) 양식은 다음과 같아. 영어: apple 한국어: 사과"
        },
        {
            "role": "system",
            "content": "예시 3) 문맥 상 모호한 것은 일반적인 단어로 번역해줘"
        },
        {
            "role": "system",
            "content": "예시 4) 번역은 직독직해에 가깝게 간결하게 해줘"
        },
        {
            "role": "system",
            "content": "예시 5) 외래어도 북한처럼 무조건 순 우리말로 표현해줘"
        },
        {
            "role": "user",
            "content": "내가 점심에 햄버거를 먹었어."
        }
    ]
)

print(completion.choices[0].message)