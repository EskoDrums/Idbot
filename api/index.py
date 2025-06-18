import os
from fastapi import FastAPI, HTTPException
from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError, UsernameInvalidError

app = FastAPI()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
client = TelegramClient("vercel", api_id, api_hash)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/resolve/")
async def resolve(q: str):
    try:
        if q.isdigit():
            user = await client.get_entity(int(q))
        else:
            user = await client.get_entity(q)
        return {"username": user.username, "user_id": user.id}
    except (ValueError, UsernameNotOccupiedError, UsernameInvalidError):
        raise HTTPException(status_code=404, detail="User not found or invalid")
