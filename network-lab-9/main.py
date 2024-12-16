import math
import uvicorn
from fastapi import FastAPI, Request, Response,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import xmltodict

app = FastAPI()

# Настроить CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.get("/")
async def func_get():
    response = {
        "Response": {
            "result": "УРАААААААААААААААААААА"
        }
    }
    response_xml = xmltodict.unparse(response, pretty=True)
    return Response(content=response_xml, media_type="application/xml")

@app.post("/")
async def func(request: Request):
    # Чтение тела запроса как XML
    body = await request.body()

    # Парсим XML в Python-словарь
    data = xmltodict.parse(body)

    # Извлекаем параметры из XML
    n1 = float(data["Params"]["n1"])
    operation = data["Params"]["operation"]
    n2 = float(data["Params"].get("n2", 0))  # n2 может быть необязательным

    # Логика операций
    if operation == "+":
        result = n1 + n2
    elif operation == "-":
        result = n1 - n2
    elif operation == "*":
        result = n1 * n2
    elif operation == "/":
        result = n1 / n2
    elif operation == "^":
        result = pow(n1, n2)
    elif operation == "'^":
        result = pow(n1, 1 / n2)
    elif operation == "sin":
        result = math.sin(math.radians(n1))
    elif operation == "cos":
        result = math.cos(math.radians(n1))
    elif operation == "tan":
        result = math.tan(math.radians(n1))
    elif operation == "ctg":
        result = 1 / math.tan(math.radians(n1))
    else:
        raise HTTPException(status_code=422, detail="Ошибка: неизвестная операция")

    # Формируем XML-ответ
    response = {
        "Response": {
            "result": result
        }
    }
    response_xml = xmltodict.unparse(response, pretty=True)
    return Response(content=response_xml, media_type="application/xml")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
