from elasticsearch import Elasticsearch

ELASTICSEARCH_HOST = "http://localhost:9200"
INDEX_NAME = "reviews"

# Elasticsearch 클라이언트 초기화
es = Elasticsearch(ELASTICSEARCH_HOST)

# Elasticsearch 인덱스 생성
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                "mappings": {
                    "properties": {
                        "res_id": {"type": "integer"},
                        "author": {"type": "text"},
                        "review": {"type": "text"}
                    }
                },
            },
        )
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Elasticsearch에 데이터 삽입
def insert_review(review: dict):
    es.index(index=INDEX_NAME, document=review)

# Elasticsearch에서 데이터 검색
def search_reviews(query: str):
    return es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "match": {
                    "review": query
                }
            }
        }
    )
