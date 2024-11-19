from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
 {
     "role": "system",
     "content": "시스템은 주어진 조건에 따라 좌석 배치 문제를 풀이합니다. 답변은 주어진 양식에 따라 명확히 작성합니다. 풀이 과정이나 추가 설명은 포함되지 않습니다."
 },
 {
     "role": "system",
     "content": "1. A가 B의 옆자리에 없다는 조건이 주어지면, A와 B는 인접한 위치에 있을 수 없습니다."
 },
 {
     "role": "system",
     "content": "2. B가 C의 옆자리에 있다는 조건이 주어지면, B와 C는 반드시 인접한 위치에 있어야 합니다."
 },
 {
     "role": "system",
     "content": "3. C가 D의 옆자리에 없다는 조건이 주어지면, C와 D는 인접한 위치에 있을 수 없습니다."
 },
 {
     "role": "system",
     "content": "4. 모든 사람은 일렬로 배치된 좌석에 각기 다른 자리에 앉아야 하며, 중복되지 않는 위치에 배정됩니다."
 },
 {
     "role": "system",
     "content": "5. 좌석 배열은 직선 구조이며, 첫 번째 좌석 왼쪽과 마지막 좌석 오른쪽에는 추가 좌석이 없습니다."
 },
 {
     "role": "system",
     "content": "6. 모든 조건을 충족하는 가능한 좌석 배치가 여러 가지라면, 모든 정답을 취합하여 제시합니다."
 },
 {
     "role": "system",
     "content": "답변은 다음 양식으로만 작성합니다: 'Possible arrangements: ABCD, DCBA'"
 }
    ]
)

print(completion.choices[0].message)