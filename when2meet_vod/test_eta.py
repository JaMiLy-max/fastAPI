from datetime import datetime, timedelta

"""
Mypy : 파이썬 타입 검사기
- 택배는 2영업일 이후에 도착합니다. 월요일부터 토요일까지가 영업일입니다.
- 단순화를 위해 “도서산간지역”은 고려하지 않습니다.
- 단순화를 위해 설날, 추석 등의 공휴일은 고려하지 않습니다.
    - https://www.data.go.kr/data/15012690/openapi.do
"""

# literal 을 쓰지 않고 상수를 쓰는 이유 : 배송에 걸리는 시간을 나만 알기때문에.
# magic number를 쓰지말자.
DELIVERY_DAYS = 2


def get_eta(purchase_date: datetime) -> datetime:
    # print(expected_day.strftime("%Y-%m-%d"))
    expected_date = purchase_date

    index = 0
    while index < DELIVERY_DAYS:
        # 날짜를 skip하는 조건 (토요일 다음날은 배송되지 않기에 skip 조건에 포함)
        if expected_date.weekday() < 6:
            expected_date += timedelta(days=1)
            index = index + 1

        if expected_date.weekday() == 6:
            # 공휴일은 그냥 +1
            expected_date += timedelta(days=1)

    return expected_date


def test_get_eta_2023_12_01() -> None:
    result = get_eta(datetime(2023, 12, 1))
    assert result == datetime(2023, 12, 4)


def test_get_eta_2024_12_31() -> None:
    """
    공휴일 정보가 없어서 1월 1일도 평일로 취급됩니다.
    """
    result = get_eta(datetime(2024, 12, 31))
    assert result == datetime(2025, 1, 2)


def test_get_eta_2024_02_28() -> None:
    result = get_eta(datetime(2024, 2, 28))
    assert result == datetime(2024, 3, 1)


if __name__ == "__main__":
    pass
