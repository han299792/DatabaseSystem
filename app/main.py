from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch, exceptions

app = FastAPI()

es = Elasticsearch("http://localhost:9200") 

data_path = "./reviews.json"

es.index(index="my_index", id=1, body=data_path)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI-Elasticsearch example!"}


@app.get("/search/")
async def search_documents(index: str, query: str):
    try:
        response = es.search(
            index=index,
            body={
                "query": {
                    "match": {
                        "content": query
                    }
                }
            }
        )
        hits = response.get("hits", {}).get("hits", [])
        return {"results": [hit["_source"] for hit in hits]}
    except exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail=f"Index '{index}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @app.post("/add-document/")
# async def add_document(index: str, document_id: str, content: dict):

#     try:
#         es.index(index=index, id=document_id, body=content)
#         return {"message": "Document added successfully", "index": index, "id": document_id}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))'


@app.delete("/delete-document/")
async def delete_document(index: str, document_id: str):

    try:
        es.delete(index=index, id=document_id)
        return {"message": "Document deleted successfully", "index": index, "id": document_id}
    except exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
