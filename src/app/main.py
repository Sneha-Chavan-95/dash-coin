from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi.responses import JSONResponse


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
    return JSONResponse(status_code = 200, content = "page_title": "Block")
	
@app.post("/register")
def register_new_user():
	status, users_dict = register_new_users()
	return JSONResponse(status_code = status, content = users_dict)

@app.get("/balance")
def get_balance():
	status, user_dict = get_user_balance(token)
	return JSONResponse(status_code= status, content = user_dict)

@app.get("/users/{token}")
def get_users():
	status, users_dict = get_all_users(token)
	return JSONResponse(status_code = status, content = users_dict)

@app.post("/send")
def send_credit(sender,receiver,amount,token):
	status,transaction = send_credit_user(sender: str = Body(default="", embed=True), receiver :str = Body(default="", embed=True),amount :float = Body(default=0.0, embed=True),token: str = Body(default="", embed=True))
	return JSONResponse(status_code = status, content = transaction)

@app.post("/")
def update_balance(user_name,amount,token):
	status,transaction = update_user_balance(user_name: str = Body(default="", embed=True),amount :float = Body(default=0.0, embed=True),token: str = Body(default="", embed=True))
	return JSONResponse(status_code = status, content = transaction)
	
@app.post("/")
def request_credit(sender,receiver,amount,token):
	status,transaction = request_credit_user(sender: str = Body(default="", embed=True), receiver :str = Body(default="", embed=True),amount :float = Body(default=0.0, embed=True),token: str = Body(default="", embed=True))
	return JSONResponse(status_code = status, content = transaction)
