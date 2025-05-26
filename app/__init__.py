import os
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests 

STATIC_DIR = "app/static"
TEMPLATES_DIR = "app/templates"

app = FastAPI(title="Khuluma", description="Text-to-speech app", version="1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .config import Config

NARAKEET_API_URL = Config.NARAKEET_API_URL
NARAKEET_API_KEY = Config.NARAKEET_API_KEY

class ReqBody(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def index_view(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/v1/speak")
def speak_text(req: Request, data: ReqBody):  
    options = {
        'headers': {
            'Accept': 'application/octet-stream',
            'Content-Type': 'text/plain',
            'x-api-key': NARAKEET_API_KEY,
        },
        'data': data.text.encode('utf8')
    }
    
    try:
        response = requests.post(NARAKEET_API_URL, **options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    filename = f"{uuid.uuid4()}.m4a"
    filepath = os.path.join(STATIC_DIR, "audio" , filename)
    
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
    
    audio_url = f"{req.base_url}static/audio/{filename}" 
    
    return {"audio_url": audio_url}