"""File to house all the `Helper` functions"""

# ! API helper functions
def get_all_users(token : str) -> tuple[int,list[str]] :
    if get_user_against_token(token):
        #Retrieve all users from Database
        return(200,[])
    return (403,[])

def send_credit_user(receiver : str, amount : float,token : str )-> tuple[int,dict]:
    sender= get_user_against_token(token)
    if sender and is_user_valid(receiver) and get_user_balance(token)>=amount:
        # Create transaction
        # Create block
        # Mine block
        return(200,{})
    return(405,{})

def register_new_users(email:str,name:str,password:str)->tuple[int,dict]:
    return(201,{})

def get_user_balance(token : str)-> tuple[int,float] :
    return(200,100.00)

def add_user_balance(amount : float, token : str)->  tuple[int,float]: 
    return(200,100.00)

def request_credit_user(sender : str, receiver : str, amount : float,token : str ) -> tuple[int,dict]:
    return(200,{})

def get_all_transactions(token:str) -> tuple[int, list[dict]]:
    return(200,[{}])

# ! Session management functions

def create_token() -> str:...

def get_user_against_token(token : str)-> str :...

def is_user_valid(email:str)->bool:...

def generate_otp(length:int = 4)->str :...

def generate_password_salt(password:str) -> str:...

def authenticate_user(email : str, password : str)-> bool :...

def notify_user(email:str,body:str)->bool:...