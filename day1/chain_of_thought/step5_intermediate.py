from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "시스템이 퀴즈를 풀겠습니다. 몇 명의 사람들과, 좌석 공간 크기가 제공됩니다. 각자의 자리 정보가 여러가지 제공됩니다. 풀이 과정은 절대로 말하지 않습니다."
        },
        {
            "role": "system",
            "content": "1. A의 다음에 B가 있다고 알려졌다면, A 오른쪽에는 반드시 B가 위치해야 합니다."
        },
        {
            "role": "system",
            "content": "2. A의 다음에 B가 없다고 알려졌다면, A 오른쪽에는 반드시 B가 없어야 합니다."
        },
        {
            "role": "system",
            "content": "3. 모든 사람은 모든 좌석 시트에 앉아야 하며, 각자가 서로 다른 좌석에 앉을 수 있도록 배치합니다.."
        },
        {
            "role": "system",
            "content": "4. 좌석은 일자의 배열이며, 첫자리의 이전좌석, 끝자리의 다음 좌석은 없습니다."
        },
        {
            "role": "system",
            "content": "5. 모든 조건을 고려했을때, 배정 가능한 경우의 수가 여러가지라면, 정답들을 취합합니다."
        },
        {
            "role": "system",
            "content": "대답은 반드시 다음 양식으로만 말합니다. 다른 말은 하지 않습니다: 'Possible arrangements: ABCD, DCBA'"
        },
        {
            "role": "user",
            "content": "Four people (A, B, C, D) are sitting in a row. We know that:"
        },
        {
            "role": "user",
            "content": "1. A is not next to B"
        },
        {
            "role": "user",
            "content": "2. B is next to C"
        },
        {
            "role": "user",
            "content": "3. C is not next to D."
        }
    ]
)

print(completion.choices[0].message)