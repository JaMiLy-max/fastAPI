# from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Depends
from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams

app = FastAPI()

UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.


# 1. 유저 생성 API 작성하기
@app.post("/users")
async def create_user(data: UserCreateRequest):
    user = UserModel.create(**data.model_dump())
    return user.id


# 2. 모든 유저 정보를 가져오는 API 작성하기
@app.get("/users")
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)  # 에러명시. 유저정보 빈 경우
    return result


# 3. 유저 정보를 가져오는 API 작성하기
@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)  # user_id에 해당하는 유저 객체가 없을 경우 404
    return user


# 4. 유저 정보를 부분 수정하는 API 작성하기
@app.patch("/users/{user_id}")
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user


# 5. 유저를 삭제하는 API 작성하기
@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)):  # FastAPI의  Path객체로 검증
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()

    return {"detail": f"User: {user_id}, Successfully Deleted."}


# 6. 유저를 검색하는 API 작성하기
@app.get("/users/search")
async def search_users(query_params: UserSearchParams = Depends()):
    valid_query = {key: value for key, value in query_params.model_dump(exclude_unset=True).items()}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
