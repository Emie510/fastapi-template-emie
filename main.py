import uvicorn
from typing import Union
from fastapi import Depends, FastAPI, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
from dotenv import load_dotenv
load_dotenv()

# load environment variables
if "PORT" not in os.environ.keys():
    port = 8000
else:
    port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="fastapi-template",
    description="Template repo for FastAPI.",
    version="0.0.1",
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)
key_query_scheme = APIKeyHeader(name="key")


def some_function():
    """some function that does something."""


def required_headers(
        username: str = Header(),
        password: str = Header()):
    """Headers required to use the API."""
    return username, password


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """Redirect base URL to docs."""
    return RedirectResponse(url='/docs')


class MyPayload(BaseModel):
    text_field: str
    integer_field: int | None = None


@app.post("/how cool is this?")
async def post_how_cool_this_is(answer_to_question, dependencies=Depends(required_headers)):
    """Provide your input on how cool this is?"""
    
    # do something with input_data
    new_string = answer_to_question.text_field + ". Indeed, I agree. Supercool."
    
    return JSONResponse(status_code=200, content={"message": "Success", "new_string": new_string})


@app.get("/get-something")
async def get_a_dataframe_with_multiples_of_this_number(id: int, api_key: str = Depends(key_query_scheme)):
    """GET Something."""
    
    # check API key
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(status_code=200, content={"message": f"this is the data of registration {id}"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)
