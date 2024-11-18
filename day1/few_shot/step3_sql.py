from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Convert the following natural language requests into SQL queries:"
        },
        {
            "role": "system",
            "content": "1. 연봉이 50000을 초과하는 사원: SELECT * FROM employees WHERE salary > 50000;"
        },
        {
            "role": "system",
            "content": "2. 재고가 없는 상품: SELECT * FROM products WHERE stock = 0;"
        },
        {
            "role": "system",
            "content": "3. 수학 점수가 90점을 초과하는 학생: SELECT name FROM students WHERE math_score > 90;"
        },
        {
            "role": "system",
            "content": "4. 최근 30일 간의 주문내역: SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);"
        },
        {
            "role": "system",
            "content": "도시별 총 고객 수: SELECT city, COUNT(*) FROM customers GROUP BY city;"
        },
        {
            "role": "user",
            "content": "Find the average salary of employees in the marketing department;"
        }
    ]
)

print(completion.choices[0].message)