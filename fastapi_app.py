from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyrebase

config = {
    "apiKey": "AIzaSyAO2raND0p6ihktnKZDJdrpKIRaTu7AbWk",
    "authDomain": "sample-app-run.firebaseapp.com",
    "databaseURL": "https://sample-app-run-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "sample-app-run",
    "storageBucket": "sample-app-run.appspot.com",
    "messagingSenderId": "41439708256",
    "appId": "1:41439708256:web:bf1b10874e294d6ab7af05",
    "measurementId": "G-2147657JDK"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = FastAPI()

class User(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: User):
    try:
        auth.create_user_with_email_and_password(user.email, user.password)
        return {"message": "Sign up successful! Please sign in."}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@app.post("/signin")
def signin(user: User):
    try:
        auth.sign_in_with_email_and_password(user.email, user.password)
        return {"message": f"Welcome, {user.email}!"}
    except Exception as ex:
        # Check for Firebase INVALID_LOGIN_CREDENTIALS
        if "INVALID_LOGIN_CREDENTIALS" in str(ex):
            raise HTTPException(status_code=400, detail="Invalid email or password.")
        raise HTTPException(status_code=400, detail="Sign in failed.")