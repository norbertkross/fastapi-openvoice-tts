import os
from typing import Union,Optional
from src.generate_audio import AudioGenerator

from fastapi import FastAPI,Response

from fastapi.responses import FileResponse,StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel,Field

app = FastAPI()


# Allow all origins for demonstration purposes
# You should restrict this in a production environment
origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioRequest(BaseModel):
    text: str
    voice: Optional[str] = Field('testimonial', description="The voioce tone from all the avalable voices [testimonial,female_1]")
    outputFormat: Optional[str] = Field('mp3', description="The generated audio encoding, supports 'raw' | 'mp3' | 'wav' | 'ogg' | 'flac' | 'mulaw'")
    speed: Optional[float] = Field(1.0, description="Playback rate of generated speech")


# Global variables to store the model and speaker IDs
target_se = None 
model = None 
source_se = None
speaker_id = None
tone_color_converter = None
target_se_default_male = None
target_se_default_female = None


# Dependency to initialize the TTS model and speaker IDs
def globalDataSetter():
    audioGenerator = AudioGenerator()
    target_se,tone_color_converter,target_se_default_male,target_se_default_female = audioGenerator.targetSEreference()
    model,source_se,speaker_id = audioGenerator.generatorModelsAndParamsInitializer()

    return target_se,model,source_se,speaker_id,tone_color_converter,target_se_default_male,target_se_default_female


@app.on_event("startup")
def startup_event():
    global target_se,model,source_se,speaker_id,tone_color_converter,target_se_default_male,target_se_default_female
    target_se,model,source_se,speaker_id,tone_color_converter,target_se_default_male,target_se_default_female = globalDataSetter()    
    print("startup call.... end!")


@app.get("/")
def read_root():
    return "HELLO WORLD"


@app.post("/generate")
async def generate(request: AudioRequest):
    audioGenerator = AudioGenerator()
    text = request.text
    # file_path = audioGenerator.generateAudio(text,target_se,model,source_se,speaker_id,tone_color_converter) 
   
    targetSEtoUse = audioGenerator.determineVoiceToUse(request.voice,target_se_default_male,target_se_default_female)

    file_path = await audioGenerator.generateAudio(text,targetSEtoUse,model,source_se,speaker_id,tone_color_converter,request.speed,request.outputFormat) 

    if not os.path.exists(file_path):
        print("File not found")
        return Response(content="File not found", status_code=404)

    async def file_streamer():
        try:
            async for chunk in audioGenerator.async_iterator(file_path):
                yield chunk
        finally:
            parts = file_path.split("output_v2_")
            pathToDelete = ''.join(parts)
            print(f'path res: {pathToDelete}')
            await audioGenerator.delete_file(pathToDelete)
            await audioGenerator.delete_file(file_path)

    # Return the audio file as a byte stream using StreamingResponse
    return StreamingResponse(content=file_streamer(), media_type=f'audio/{request.outputFormat}')    
     

