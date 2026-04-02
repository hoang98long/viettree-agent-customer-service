# viettree-agent-customer-service
viettree-agent-customer-service
![customer_service_agent](https://github.com/user-attachments/assets/1ab3664e-51bd-47a9-a091-2fd83172c230)

## run ollma:
```
ollama run [model]
```
## run API:
```
uvicorn main:app --reload
```
## Test
```
curl -X POST "http://127.0.0.1:8000/ask?question=Sản phẩm bảo hành bao lâu?"
```
