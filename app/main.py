from fastapi import FastAPI, Depends, HTTPException, status, Request, Header, Body
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import json
import os
import jwt
from simplejson import JSONDecodeError
from lib import logger as log
from converter import str_converter, name_provider

logger = log.get_logger()

apikey = os.getenv('API_KEY')
secretkey = os.getenv('SECRET_KEY')

JWT_SECRET_KEY = secretkey
ALGORITHM = "HS256"
app = FastAPI()

# Define the expected X-Parse-REST-API-Key header value
EXPECTED_PARSE_API_KEY = apikey

# Define a dependency to get the JWT key from the X-JWT-KEY header
def get_jwt_key(x_jwt_key: Optional[str] = Header(None)):
    if x_jwt_key is None:
        raise HTTPException(status_code=400, detail="ERROR X-JWT-KEY header")
    if x_jwt_key != JWT_SECRET_KEY:
        raise HTTPException(status_code=401, detail="ERROR X-JWT-KEY header")
    return x_jwt_key

# Define a dependency to check the X-Parse-REST-API-Key header
def parse_api_key_dependency(x_parse_rest_api_key: Optional[str] = Header(None)):
    if x_parse_rest_api_key is None:
        raise HTTPException(status_code=400, detail="ERROR X-Parse-REST-API-Key header")
    if x_parse_rest_api_key != EXPECTED_PARSE_API_KEY:
        raise HTTPException(status_code=401, detail="ERROR X-Parse-REST-API-Key header")
    return x_parse_rest_api_key

# Example endpoint that uses the X-JWT-KEY and X-Parse-REST-API-Key headers
@app.post("/devops",dependencies=[Depends(get_jwt_key),Depends(parse_api_key_dependency)])
async def my_endpoint(request: Request):
    try:
      value = await request.body()
      logger.info("this is the raw json value")
      json_value = str_converter(str(value))
      logger.info("The printing format")
      logger.info(json_value)
      name_def = name_provider(json_value)
      logger.info(name_def)
      return name_def
    except:
      return "error"

