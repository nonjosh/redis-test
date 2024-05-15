import os

from fastapi import FastAPI, HTTPException
from aioredis import Redis
import aioredis


class MyFastAPI(FastAPI):
    redis: Redis


app = MyFastAPI()


@app.on_event("startup")
async def startup_event():
    app.redis = await aioredis.create_redis_pool(os.environ["REDIS_URL"])


@app.on_event("shutdown")
async def shutdown_event():
    app.redis.close()
    await app.redis.wait_closed()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/set/{key}/{value}")
async def set_value(key: str, value: str):
    await app.redis.set(key, value)
    return {"message": f"Value set for key: {key}"}


@app.get("/get/{key}")
async def get_value(key: str):
    value = await app.redis.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}
