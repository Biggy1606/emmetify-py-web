import emmet
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from emmetify import Emmetifier, emmetify_compact_html

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

emmetifier = Emmetifier()


class UrlPayload(BaseModel):
    url: str
    compact: bool = False


class HtmlPayload(BaseModel):
    html: str
    compact: bool = False


class EmmetPayload(BaseModel):
    emmet: str


@app.post("/api/v1/url")
def emmetify_url(payload: UrlPayload):
    try:
        response = requests.get(payload.url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html = response.text
        if payload.compact:
            emmet_string = emmetify_compact_html(html)
        else:
            emmet_string = emmetifier.emmetify(html)
        return {"emmet": emmet_string}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/html")
def emmetify_html(payload: HtmlPayload):
    try:
        if payload.compact:
            emmet_string = emmetify_compact_html(payload.html)
        else:
            emmet_string = emmetifier.emmetify(payload.html)
        return {"emmet": emmet_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/emmet")
def htmlify_emmet(payload: EmmetPayload):
    try:
        # Add a basic check for empty input
        if not payload.emmet.strip():
            raise ValueError("Emmet input cannot be empty.")
        html = emmet.expand(payload.emmet)
        pretty_html = BeautifulSoup(html, "lxml").prettify()
        return {"html": pretty_html}
    except ValueError as e:
        # Catch empty input error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Return a 400 error for invalid Emmet syntax
        raise HTTPException(status_code=400, detail=f"Invalid Emmet abbreviation: {e}")


@app.get("/")
def read_root():
    return {"message": "Emmetify API is running"}
