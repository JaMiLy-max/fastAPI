from fastapi import FastAPI

app = FastAPI()

#  mypy. -> [no-untyped-def] -> 함수의 반환값이 없어서. dict만 쓰면[type-arg] -> dict[str, str]
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def hello(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}

# static -> 정적 (실행하기 전에 결정)
# Dynamic -> (동적 실행 중에 결정_)
# mypy는 코드를 생행하지 않는다. 정적인 기능