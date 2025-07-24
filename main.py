from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from moviepy import VideoFileClip
import os
import uuid

from starlette.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.post("/convert/")
async def convert_to_mp4(file: UploadFile = File(...)):

    input_filename = f"temp_{uuid.uuid4().hex}.mp4"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    output_filename = f"output_{uuid.uuid4().hex}.mp3"

    try:

        videoclip = VideoFileClip(input_filename)

        audioclip = videoclip.audio


        audioclip.write_audiofile(output_filename)

        audioclip.close()
        videoclip.close()

    finally:
        os.remove(input_filename)

    return FileResponse(output_filename, media_type="audio/mpeg", filename="extracted.mp3")


@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

