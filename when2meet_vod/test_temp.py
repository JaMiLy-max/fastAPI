# 테스트도중한번이라도 실행된 제품코드 / 전체제품코드(4)

from .temp import add


def test_add() -> None:
    # Given
    a, b = 1, 1

    # When
    result = add(a, b)

    # Then
    assert result == 2


# 비동기 async 1개의 테스트가 이그노어드(무시) 당함.
# 파이테스트 에이싱크 아이오와 적절한 설정이 같이있지 않으면 비동기(async) test는 다 무시됨
async def test_abc() -> None:
    print("abc")
