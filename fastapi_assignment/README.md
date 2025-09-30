# 과제 진행 방법

- [FastAPI 공식문서](https://fastapi.tiangolo.com/ko/tutorial/)를 보고 학습을 먼저 진행합니다. (첫걸음 ~ 쿼리 매개 변수 모델까지)
- FastAPI 자습서를 따라 API 를 먼저 구성해봅니다.
- 이후 새로운 프로젝트 폴더에서 아래의 과제를 수행하여 Git을 이용하여 코드 기록을 관리하고, LMS에 Github Repository의 주소를 댓글로 입력합니다.

# 과제 풀이 준비사항

## 1. 과제 진행을 위한 FastAPI 프로젝트를 구성하세요.

```bash
fastapi_assignment/
│── app/
│   ├── models/ # 임시로 사용할 모델
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── movies.py
│   ├── schemas/  # Pydantic 데이터 검증 모델
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── movies.py
│   ├── __init__.py
├── main.py # FastAPI 앱 실행 파일
│── poetry.lock
│── pyproject.toml
│── README.md  # 프로젝트 설명 파일
```

## 2. 먼저 과제를 진행하기 전 다음 코드를 각각의 파일에 붙여넣어 주세요.

- 코드

```python
# app/models/users.py

import random

class UserModel:
    _data = []  # 전체 사용자 데이터를 저장하는 리스트
    _id_counter = 1  # ID 자동 증가를 위한 카운터

    def __init__(self, username, age, gender):
        self.id = UserModel._id_counter
        self.username = username
        self.age = age
        self.gender = gender

        # 클래스가 인스턴스화 될 때 _data에 추가하고 _id_counter를 증가시킴
        UserModel._data.append(self)
        UserModel._id_counter += 1

    @classmethod
    def create(cls, username, age, gender):
        """ 새로운 유저 추가 """
        return cls(username, age, gender)

    @classmethod
    def get(cls, **kwargs):
        """ 단일 객체를 반환 (없으면 None) """
        for user in cls._data:
            if all(getattr(user, key) == value for key, value in kwargs.items()):
                return user
        return None

    @classmethod
    def filter(cls, **kwargs):
        """ 조건에 맞는 객체 리스트 반환 """
        return [
            user
            for user in cls._data
            if all(getattr(user, key) == value for key, value in kwargs.items())
        ]

    def update(self, **kwargs):
        """ 객체의 필드 업데이트 """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)

    def delete(self):
        """현재 인스턴스를 _data 리스트에서 삭제"""
        if self in UserModel._data:
            UserModel._data.remove(self)

    @classmethod
    def all(cls):
        """ 모든 사용자 반환 """
        return cls._data

    @classmethod
    def create_dummy(cls):
        for i in range(1, 11):
            cls(username=f'dummy{i}', age=15 + i, gender=random.choice(['male', 'female']))

    def __repr__(self):
        return f"UserModel(id={self.id}, username='{self.username}', age={self.age}, gender='{self.gender}')"

    def __str__(self):
        return self.username
```

```python
# main.py

from typing import Annotated

from fastapi import FastAPI

from app.models.users import UserModel

app = FastAPI()

UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
```


# 과제

### 1. 유저 생성 API 작성하기

- **요구사항**

클라이언트가 **username, age, gender**를 **Request Body**로 전달하면,

1. **Pydantic 모델을 활용하여 데이터 유효성을 검증**하고,
2. 검증된 데이터를 사용하여 **UserModel의 인스턴스를 생성**한 뒤,
3. 생성된 유저의 **id**를 ****반환하는 **API 라우터 함수**를 작성하세요.
- **조건**
1. FastAPI의 **Pydantic 모델**을 활용하여 **데이터 검증**을 수행해야 합니다.
2. **username**은 **문자열(str), age**는 **정수(int), gender** 는 **Enum** 이며 **‘male’, ‘female’** 중에서만 **선택가능** 해야합니다.
- 예시 답안 코드

```python
# app/schemas/users.py

from enum import Enum

from pydantic import BaseModel

class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'

class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum
```

```python
# main.py
...

@app.post('/users')
async def create_user(data: UserCreateRequest):
    user = UserModel.create(**data.model_dump())
    return user.id

...
```


### 2. 모든 유저 정보를 가져오는 API 작성하기

- **요구사항:**

클라이언트가 `/users` 경로로 `GET` 요청을 보내면

1. **UserModel** 에 구현된 **`all()`** 메서드를 사용해서,
2. 모든 유저  정보를 ****반환하는 **API 라우터 함수**를 작성하세요.
- **조건**
1. 유저가 하나도 없는 경우 404 에러를 반환합니다.
2. 응답으로 반환하는 유저의 정보는 **id, username, age, gender** 입니다.
- 예시 답안 코드

```python
# main.py

@app.get('/users')
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result
```


### 3. 유저 정보를 가져오는 API 작성하기

- **요구사항:**

클라이언트가 **user_id**를 **경로 매개변수(Path Parameter)**로 전달하면,

1. 경로 매개변수로 넘겨받은 **user_id**가 양수인지 검증하고,
2. 검증된 **user_id**를 통해 **user_id**에 해당하는 **UserModel 객체를 가져온 뒤**,
3. **가져온 유저의 정보를 반환하는 API 라우터 함수**를 작성하세요.
- **조건**
1. FastAPI의  **Path객체를** 활용하여 경로 매개변수의 검증을 수행해야 합니다.
2. **user_id**에 해당하는 유저 객체가 없을 경우 **404 에러**를 반환합니다.
3. 응답으로 반환하는 유저의 정보는 **id, username, age, gender** 입니다.
- 예시 답안 코드

```python
# main.py

...

@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user

...
```


### 4. 유저 정보를 부분 수정하는 API 작성하기

- **요구사항:**

클라이언트가 **user_id**를 **경로 매개변수(Path Parameter)로 전달하고, username, age를** **Request Body**로 전달하면,

1. 경로 매개변수로 넘겨받은 **user_id**가 양수인지 검증합니다.
2. **Pydantic 모델을 활용하여 데이터 유효성을 검증**하고,
3. 경로 매개변수로 넘겨받은 **user_id** 이용해 **UserModel 객체를 가져온 뒤**,
4. **Request Body** 로 넘겨받은 username 또는 age에 따라 유저의 정보를 업데이트하고,
5. **업데이트된 유저의 정보(user_id, username, age, gender)를 모두 반환하는 API 라우터 함수**를 작성하세요.
- **조건**
1. FastAPI의 **Pydantic 모델**을 활용하여 데이터 검증을 수행해야 합니다.
2. FastAPI의  **Path객체를** 활용하여 경로 매개변수의 검증을 수행해야 합니다.
3. **user_id**에 해당하는 유저 객체가 없을 경우 **404 에러**를 반환합니다.
4. 응답으로 반환하는 유저의 정보는 **id, username, age, gender** 입니다.
- 예시 답안 코드

```python
# app/schemas/users.py

...

class UserUpdateRequest(BaseModel):
    username: str | None = None
    age: int | None = None

...
```

```python
# main.py
...

@app.patch('/users/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user

...
```


### 5. 유저를 삭제하는 API 작성하기

- **요구사항:**

클라이언트가 **user_id**를 **경로 매개변수(Path Parameter)**로 전달하면,

1. 경로 매개변수로 넘겨받은 **user_id** 양수인지 검증합니다.
2. 경로 매개변수로 넘겨받은 **user_id**를 이용해 **UserModel 객체를 가져온 뒤**,
3. 유저 모델의 delete 메서드를 이용하여 유저 객체를 삭제하고 응답을 **반환하는 API 라우터 함수**를 작성하세요.
- **조건**
1. FastAPI의 **Pydantic 모델**을 활용하여 데이터 검증을 수행해야 합니다.
2. FastAPI의  **Path객체를** 활용하여 경로 매개변수의 검증을 수행해야 합니다.
3. **user_id**에 해당하는 유저 객체가 없을 경우 **404 에러**를 반환합니다.
4. **응답형태는 `{’detail’:** f'User: {user_id}, Successfully Deleted.'}` 로 합니다.
- 예시 답안 코드

```python
# main.py

@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()

    return {'detail': f'User: {user_id}, Successfully Deleted.'}
```


### 6. 유저를 검색하는 API 작성하기

- **요구사항:**

클라이언트가 **username, age, gender**를 **쿼리 매개변수(Query Parameter)로** 전달하면,

1. **Pydantic 모델을 활용하여 쿼리 매개변수의 유효성을 검증**하고,
2. **쿼리 매개변수**로 넘겨받은 **username, age, gender**를 이용해 해당 정보와 일치하는 **UserModel 객체들을 가져온 뒤**,
3. **가져온 유저들의 정보(user_id, username, age, gender)를 모두 반환하는 API 라우터 함수**를 작성하세요.
- **조건**
1. FastAPI의 **Pydantic 모델과, Query 객체를** 활용하여 **쿼리 매개변수**의 **데이터 유효성 검증을 수행**해야 합니다.
1. age 는 0보다 큰 값만 허용합니다.
2. **username, age, gender** 이외의 쿼리 매개변수는 받지 않고 에러를 반환하도록 설정합니다.
3. 검색결과에 해당하는 유저 객체가 없을 경우 **404 에러**를 반환합니다.
4. 응답으로 반환하는 유저의 정보는 **id, username, age, gender** 입니다.
- 예시 답안 코드

```python
# app/schemas/users.py

...

class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: str | None = None
    age: conint(gt=0) | None = None
    gender: GenderEnum | None = None
...
```

```python
# main.py
...

@app.get('/users/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return 	filtered_users

...
```
<img width="1340" height="190" alt="스크린샷 2025-10-01 오전 8 00 17" src="https://github.com/user-attachments/assets/bcc5bf29-caaa-4bb3-a395-a97514b1f31a" />
