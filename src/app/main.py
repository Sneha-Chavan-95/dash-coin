from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi.responses import JSONResponse
from helper.helper import (
    authenticate_user,
    clear_token,
    create_token,
    get_all_transactions,
    get_all_users,
    get_user_against_token,
    get_user_balance,
    register_new_user,
    request_credit_user,
    send_credit_user,
    add_user_balance,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"page_title": "Welcome to DASH Coin"})


@app.post("/register")
def register_user(email: str = Body(default="", embed=True), name: str = Body(default="", embed=True), password: str = Body(default="", embed=True)) -> JSONResponse:
    """API function

    Args:
        email (str, optional): _description_. Defaults to Body(default="", embed=True).
        name (str, optional): _description_. Defaults to Body(default="", embed=True).
        password (str, optional): _description_. Defaults to Body(default="", embed=True).

    Returns:
        JSONResponse: _description_
    """
    status, users_dict = register_new_user(email, name, password)
    return JSONResponse(status_code=status, content=users_dict)


@app.get("/balance/{token}")
def get_balance(token: str):
    status, user_dict = get_user_balance(token)
    return JSONResponse(status_code=status, content=user_dict)


@app.get("/users/{token}")
def all_users(token: str):
    status, users_dict = get_all_users(token)
    return JSONResponse(status_code=status, content=users_dict)


@app.post("/send")
def send_credit(receiver: str = Body(default="", embed=True), amount: float = Body(default=0.0, embed=True), token: str = Body(default="", embed=True)):
    status, transaction = send_credit_user(receiver, amount, token)
    return JSONResponse(status_code=status, content=transaction)


@app.post("/recharge")
def recharge(amount: float = Body(default=0.0, embed=True), token: str = Body(default="", embed=True)):
    status, transaction = add_user_balance(amount, token)
    return JSONResponse(status_code=status, content=transaction)


@app.post("/transactions")
def transactions(token: str = Body(default="", embed=True)):
    status, transaction = get_all_transactions(token)
    return JSONResponse(status_code=status, content=transaction)


@app.post("/authenticate")
def authenticate(email: str = Body(default="", embed=True), password: str = Body(default="", embed=True)):
    status, transaction = authenticate_user(email, password)
    return JSONResponse(status_code=status, content=transaction)


@app.post("/clear_token")
def clear(token: str = Body(default="", embed=True)):
    status, transaction = clear_token(token)
    return JSONResponse(status_code=status, content=transaction)


@app.post("/create_token")
def create(email: str = Body(default="", embed=True)):
    status, transaction = create_token(email)
    return JSONResponse(status_code=status, content=transaction)


@app.get("/get_username/{token}")
def get_username(token: str):
    status, transaction = get_user_against_token(token)
    return JSONResponse(status_code=status, content=transaction)
