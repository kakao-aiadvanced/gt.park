# 1. 3개의 블로그 포스팅 본문을 Load하기 : WebBaseLoader 활용
# https://python.langchain.com/v0.2/docs/integrations/document_loaders/web_base/

import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

print("#1 start")
# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

# 2. 불러온 본문을 Split (Chunking) : recursive text splitter 활용 (아래 링크 참고)
print("#2 start")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)


# 3. Chunks 를 임베딩하여 Vector store 저장: openai 임베딩, chroma vectorstore 사용
# 이 때,
# embedding model 은 "text-embedding-3-small" 사용
# embedding: https://python.langchain.com/v0.2/docs/integrations/text_embedding/openai/
# vetor store: https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
# retriever search_type 은 'similarity', search_kwargs={'k': 6} 을 사용해주세요.
print("#3 start")
vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})


# 4. User query = ‘agent memory’ 를 받아 관련된 chunks를 retrieve
print("#4 start")
query = "agent memory"
retrieved_docs = retriever.invoke(query)
print(len(retrieved_docs))
print(retrieved_docs)


# 5. 5-1) 과 5-2) 를 참고하여, User query와 retrieved chunk 에 대해 relevance 가 있는지를 평가하는 시스템 프롬프트를 작성해보세요:
# retrieval 퀄리티를 LLM 이 스스로 평가하도록 하고, 관련이 있으면 {‘relevance’: ‘yes’} 관련이 없으면 {‘relevance’: ‘no’} 라고 출력하도록 함. ( JsonOutputParser() 를 활용 )
print("#5 start")

prompt = hub.pull("rlm/rag-prompt")
print("------prompt")
print(prompt)

llm = ChatOpenAI(model="gpt-4o-mini")

# prompt 포맷을 획득함
# https://smith.langchain.com/hub/rlm/rag-prompt?organizationId=69506e27-8483-4c2e-a84f-444f4f5e4a2f
prompt = prompt = hub.pull("rlm/rag-prompt")

parser = JsonOutputParser()
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

def createTestRelevanceQuestion(query):
    question = "query: " + query + "; query와 주어진 context를 보고, 문서의 연관성을 엄격히 본 다음 JSON 포맷으로 출력해주세요.  {\"query\", \"context\", \"relevance\": \"yes\" 또는 \"no\"}라고 대답해"
    print("query: " + (query))
    return question

results = rag_chain.invoke(createTestRelevanceQuestion("agent memory"))
# result = rag_chain.invoke("question과 answer를 다음과 같이 출력해주세요. {\"relevance\": \"yes\" 또는 \"no\"}라고 대답해")
print(results)



#6. 5 에서 모든 docs에 대해 'yes' 가 나와야 하는 케이스와 ‘no’ 가 나와야 하는 케이스를 작성해보세요.
print("#6 start")
expectYesQueries = ["agent memory", "prompt engineering", "adv-attack-llm"]
expectNoQueries = ["gt.park", "jin.jang", "jaden.dev", "bryan.ko"]

# 7. 5에서 케이스별로 의도한 결과 ('yes' 또는 'no' )와 일치하는 답변이 나오는지 확인해보세요.
#  정답대로 나오지 않는다면 문제를 찾아 디버깅해보세요.
# (Splitter, Chunk size, overlap, embedding model, vector store, retrieval 평가 시스템 프롬프트 등) 디버깅이 어려운 경우,  강사/조교에게 질문해주세요.
print("#7 start")
def testQueriesExpected(chain, queries, expect):
    for query in queries:
        ragChainResult = chain.invoke(createTestRelevanceQuestion(query))
        print(ragChainResult)
        if (ragChainResult["relevance"] != expect):
            return False
    return True

expectYesTestResult = testQueriesExpected(rag_chain, expectYesQueries, "yes")
expectNoTestResult = testQueriesExpected(rag_chain, expectNoQueries, "no")
print("Expect 'yes' all success: %s" % expectYesTestResult)
print("Expect 'no' all success: %s" % expectNoTestResult)

# 8. 6-7 의 평가에서 문제가 없다면, 5에서 작성한 코드의 실행 결과가 'yes' 인 경우,
# 4의 retrieved chunk 를 가지고 답변하는 chain 코드를 작성해주세요. (prompt | llm | parser 형태의 코드)
print("#8 start")
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
for chunk in qa_chain.stream("What is Task Decomposition?"):
    print(chunk, end="", flush=True)

# 9. 생성된 답안에 Hallucination 이 있는지 평가하는 시스템 프롬프트를 작성해보세요.
# LLM이 스스로 평가하도록 하고, hallucination 이 있으면 {‘hallucination’: ‘yes’} 없으면 {‘hallucination’: ‘no’} 라고 출력하도록 하세요.
print("#9 start")
qa_test_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | JsonOutputParser()
)

def createTestHallucinationQuestion(query):
    question = "query: " + query + "; query와 주어진 context를 보고, Answer 안에 Hallucination이 있는지 JSON 포맷으로 출력해주세요.  {\"query\", \"context\", \"hallucination\": \"yes\" 또는 \"no\"}라고 대답해"
    print("query: " + (query))
    return question

def testQaQueriesExpected(chain, queries, expect):
    for query in queries:
        ragChainResult = chain.invoke(createTestHallucinationQuestion(query))
        print(ragChainResult)
        if (ragChainResult["hallucination"] != expect):
            return False
    return True

expectNonHallucinationQueries = ["agent memory", "prompt engineering", "adv-attack-llm"]
results = testQaQueriesExpected(qa_test_chain, expectNonHallucinationQueries, "no")


#10. 9 에서 ‘yes’ 면 8 로 돌아가서 다시 생성, ‘no’ 면 답변 생성하고 유저에게 답변 생성에 사용된 출처와 함께 출력하도록 하세요. (최대 1번까지 다시 생성)
print("#10 start")
qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def createQaQuestion(query):
    question = "query: " + query + "; 대답할 Answer에 대해 미리 할루시네이션을 판단해보고, 할루시네이션이 있다면 1회 재생성한다음 Answer와 출저를 답변해줘"
    print("query: " + (query))
    return question

print(qa_chain.invoke(createQaQuestion("prompt engineering 이란? 한국어로 설명해줘")))