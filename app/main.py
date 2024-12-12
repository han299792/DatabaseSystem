import warnings
from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch, exceptions

app = FastAPI()
es = Elasticsearch("http://localhost:9200")

def delete_index(index_name):
    if es.indices.exists(index=index_name):  # 인덱스가 존재하는 경우
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted.")
    else:
        print(f"Index '{index_name}' does not exist.")


def create_index(index_name):
    mapping = {
    "mappings": {
        "properties": {
            "res_id": { "type": "integer" },
            "author": { "type": "text" },
            "review": { "type": "text" }
        }
    }
}
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created with mapping.")
    
def insert_data(index_name, document_id, document):
    response = es.index(index=index_name, id=document_id, body=document)
    print(f"Document added: {response}")

if __name__ == "__main__":
    index_name = "my_index"
    
    delete_index(index_name)
    
    create_index(index_name)

    document = {
        "res_id": 1,
        "author": "운복15",
        "review": "이쁘고 맛있어요♥️\n둘이서 런치 코스 이것저것 금액 추가해서 35정도 나왔는데 가격이 비싸다고 느껴지지 않았어요\n서비스도 만족 맛도 만족\n가끔 가서 기분 전환하기 좋은 것 같아요 :)\n직원분들도 너무 친절하세요☺️"
  },
    insert_data(index_name, "1", document)