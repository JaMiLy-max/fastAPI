from enum import Enum

from pydantic import BaseModel, conint


# gender 는 Enum 이며 ‘male’, ‘female’ 중에서만 선택가능 해야합니다.
class GenderEnum(str, Enum):
    male = "male"
    female = "female"


# FastAPI의 Pydantic 모델을 활용하여 저장할 데이터 검증을 수행
class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum


# FastAPI의 Pydantic 모델을 활용하여 수정할 데이터 검증을 수행
class UserUpdateRequest(BaseModel):
    username: str | None = None
    age: int | None = None


# FastAPI의 Pydantic 모델을 활용하여 검색할 데이터 검증을 수행
class UserSearchParams(BaseModel):
    # username, age, gender 이외의 쿼리 매개변수는 에러 반환
    model_config = {"extra": "forbid"}

    username: str | None = None
    age: conint(gt=0) | None = None  # age는 0보다 큰 값만 허용
    gender: GenderEnum | None = None
