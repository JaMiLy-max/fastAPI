# 파일의 이름과 함수의 이름을 테스트로 시작하지 않으면 pytest가 인식하지 못한다.


# 제품코드
def add(a: int, b: int) -> int:
    return a + b


# 테스트코드
def test_simple() -> None:
    # boolean expression을 받아 검증한다.
    # assert True

    # Given: 무엇인가 주어졌을때
    # 버그는 "경계"를 조항합니다.
    # int의 경우에는 -1,0,1
    a, b = 1, 1

    # When : 테스트 대상이 되는 함수를 호출합니다.
    result = add(a, b)  # result의 타입은 int

    # Then:
    assert result == 2
    # assert 1+1 ==3,"계산이 틀렸습니다."
    if not result == 2:
        raise AssertionError
