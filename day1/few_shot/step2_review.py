from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "너는 지금부터 긍정, 부정을 판단하는 영화 리뷰어야. 이제 몇가지 예시를 줄게"
        },
        {
            "role": "system",
            "content": "이건 정말 똥이야 -> 부정"
        },
        {
            "role": "system",
            "content": "재밌는데? -> 긍정"
        },
        {
            "role": "system",
            "content": "ㅋㅋㅋ -> 긍정"
        },
        {
            "role": "system",
            "content": "나만 당할 수 없지 ㅋㅋ -> 부정"
        },
        {
            "role": "system",
            "content": "오 대박 ㅋㅋ -> 긍정"
        },
        {
            "role": "user",
            "content": "The storyline was dull and uninspiring"
        }
    ]
)

print(completion.choices[0].message)