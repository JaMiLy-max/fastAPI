'''
Poetry는 파이썬 프로젝트를 위한 올인원 도구로, 프로젝트의 의존성 관리, 패키징, 배포를 간편하게 처리하는 역할을 합니다. pyproject.toml 파일 하나로 프로젝트 설정을 관리하고, 의존성 충돌 없이 패키지를 설치하며, 패키지를 빌드하고 PyPI 같은 저장소에 배포하는 등 복잡한 파이썬 프로젝트 관리 과정을 단순화하는 것이 핵심 역할입니다

'''

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