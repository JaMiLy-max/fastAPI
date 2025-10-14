# I : isort의 약자
# ruff check --select I --fix


def add(a: int, b: int) -> int:
    return a + b


# 이 부부은 테스트를 실행시에도 확인 할 수 없음. 테스트에 구멍남.
def mul(a: int, b: int) -> int:
    return a * b


def tetst_simple() -> None:
    print(add(2, 3))
    print(mul(2, 3))
