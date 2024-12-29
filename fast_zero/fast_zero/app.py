from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, todo, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Estelar'}
