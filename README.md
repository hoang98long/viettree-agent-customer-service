# viettree-agent-customer-service
viettree-agent-customer-service

## run ollma:
```
ollama run [model]
```
## run API:
```
uvicorn app:app --reload
```
## Test
```
curl -X POST "http://127.0.0.1:8000/ask?question=Sản phẩm bảo hành bao lâu?"
```
