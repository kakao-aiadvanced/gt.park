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

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)


# 3. Chunks 를 임베딩하여 Vector store 저장: openai 임베딩, chroma vectorstore 사용
# 이 때,
# embedding model 은 "text-embedding-3-small" 사용
# embedding: https://python.langchain.com/v0.2/docs/integrations/text_embedding/openai/
# vetor store: https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
# retriever search_type 은 'similarity', search_kwargs={'k': 6} 을 사용해주세요.

vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})


# 4. User query = ‘agent memory’ 를 받아 관련된 chunks를 retrieve
query = "agent memory"
retrieved_docs = retriever.invoke(query)
print(len(retrieved_docs))
print(retrieved_docs)


# 5. 5-1) 과 5-2) 를 참고하여, User query와 retrieved chunk 에 대해 relevance 가 있는지를 평가하는 시스템 프롬프트를 작성해보세요:
# retrieval 퀄리티를 LLM 이 스스로 평가하도록 하고, 관련이 있으면 {‘relevance’: ‘yes’} 관련이 없으면 {‘relevance’: ‘no’} 라고 출력하도록 함. ( JsonOutputParser() 를 활용 )


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

def createQuestion(query):
    question = "query: " + query + "; query와 주어진 context를 보고, 문서의 연관성을 엄격히 본 다음 JSON 포맷으로 출력해주세요.  {\"query\", \"context\", \"relevance\": \"yes\" 또는 \"no\"}라고 대답해"
    print("query: " + (query))
    return question

results = rag_chain.invoke(createQuestion("agent memory"))
# result = rag_chain.invoke("question과 answer를 다음과 같이 출력해주세요. {\"relevance\": \"yes\" 또는 \"no\"}라고 대답해")
print("-------------")
print(results)



#6. 5 에서 모든 docs에 대해 'yes' 가 나와야 하는 케이스와 ‘no’ 가 나와야 하는 케이스를 작성해보세요.
yesQueries = ["agent memory", "prompt engineering", "adv-attack-llm"]
for query in yesQueries:
    yesResults = rag_chain.invoke(createQuestion(query))
    print("---------yes results")
    print(yesResults)

noQueries = ["gt.park", "jin.jang", "jaden.dev", "bryan.ko"]
for query in noQueries:
    noResults = rag_chain.invoke(createQuestion(query))
    print("---------no results")
    print(noResults)
