import flet
from flet import *
import httpx

API_URL = "http://127.0.0.1:8000"

def main(page: Page):
    page.title = "Firebase Auth Demo (via FastAPI)"
    page.bgcolor = "#FFFFFF"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    email = TextField(label="Email", width=300, color="black")  # Set text color to black
    password = TextField(label="Password", password=True, can_reveal_password=True, width=300, color="black")  # Set text color to black
    message = Text("", color="red", size=14)

    async def signup(e):
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(f"{API_URL}/signup", json={"email": email.value, "password": password.value})
                if resp.status_code == 200:
                    message.value = resp.json()["message"]
                    message.color = "green"
                else:
                    message.value = "Sign up failed: " + resp.json()["detail"]
                    message.color = "red"
            except Exception as ex:
                message.value = "Sign up failed: " + str(ex)
                message.color = "red"
            page.update()

    async def signin(e):
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(f"{API_URL}/signin", json={"email": email.value, "password": password.value})
                if resp.status_code == 200:
                    message.value = resp.json()["message"]
                    message.color = "green"
                else:
                    message.value = "Sign in failed: " + resp.json()["detail"]
                    message.color = "red"
            except Exception as ex:
                message.value = "Sign in failed: " + str(ex)
                message.color = "red"
            page.update()

    page.add(
        Column(
            [
                Text("Firebase User Sign Up / Sign In", size=22, weight="bold", color="black"),
                email,
                password,
                Row([
                    ElevatedButton("Sign Up", on_click=signup),
                    ElevatedButton("Sign In", on_click=signin),
                ], alignment="center"),
                Text(value=message.value, color="black", size=14, ref=message)
            ],
            horizontal_alignment="center",
            alignment="center",
        )
    )

if __name__ == "__main__":
    flet.app(target=main)
