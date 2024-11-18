from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "시스템이 퀴즈를 풀겠습니다. 모든 풀이과정은 한글로 대답합니다. 몇 명의 사람들과, 선호하는 컬러 집합이 제공됩니다. 이들은 모두 서로 다른 컬러를 선호합니다. 문제 풀이 과정은 다음과 같습니다."
        },
        {
            "role": "system",
            "content": "1. 누군가 특정 컬러를 선호한다면, 그 사람에게 우선 선호 컬러를 배정합니다."
        },
        {
            "role": "system",
            "content": "2. 누군가 특정 컬러를 선호하지않는다면, 그 사람에게는 해당 컬러를 배제합니다."
        },
        {
            "role": "system",
            "content": "3. 모든 정보를 취합하여, 서로 동일한 컬러가 중첩되지 않도록 각자의 선호 컬러를 대답합니다."
        },
        {
            "role": "user",
            "content": "Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that: 1. Alice does not like red. 2. Bob does not like blue. 3. Carol likes green."
        }
    ]
)

print(completion.choices[0].message)