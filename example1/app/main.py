from fastapi import FastAPI, HTTPException
from redis import Redis

app = FastAPI()
redis = Redis(host="redis", port=6379, db=0)


@app.on_event("startup")
async def startup_event():
    redis.ping()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/set/{key}/{value}")
async def set_value(key: str, value: str):
    redis.set(key, value)
    return {"message": f"Value set for key: {key}"}


@app.get("/get/{key}")
async def get_value(key: str):
    value = redis.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value.decode("utf-8")}
