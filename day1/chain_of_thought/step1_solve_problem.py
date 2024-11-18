from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "수학 문제를 풀어봅시다. 정답만 말하지 말고 step by step 으로 풀어봅시다. 모든 과정은 한국어로 표현합니다."
        },
        {
            "role": "system",
            "content": "1. 문제의 유형을 파악합니다. 문제에서 사용되는 연산자들의 특성을 이해하고 해설합니다."
        },
        {
            "role": "system",
            "content": "2. 주어진 피연산자들의 자릿수를 이해하고, 작은 문제로 분할합니다."
        },
        {
            "role": "system",
            "content": "3. 작은 문제들을 개별적으로 계산하고, 개별 과정을 기억합니다."
        },
        {
            "role": "system",
            "content": "4. 주어진 계산 과정을 모두 수행하고, 정답을 도출합니다."
        },
        {
            "role": "user",
            "content": "Solve the following problem step-by-step: 23 + 47"
        }
    ]
)

print(completion.choices[0].message)