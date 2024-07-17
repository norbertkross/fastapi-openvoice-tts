import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS
import uuid
import aiofiles
import asyncio


class AudioGenerator:
    def __init__(self):
        pass


    def determineVoiceToUse(self,voicetype,target_se_default_male,target_se_default_female):

        if voicetype == "testimonial":
            return target_se_default_male
        elif voicetype == "default_male":
            return target_se_default_male
        elif voicetype == "default_female":
            return target_se_default_female            
        else:
            return target_se_default_male
            


    def targetSEreference(self):
        ckpt_converter = 'checkpoints_v2/converter'
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        output_dir = 'outputs_v2'

        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        os.makedirs(output_dir, exist_ok=True)

        reference_speaker = 'resources/testimonial.mp3' # This is the voice you want to clone
        reference_speaker_male_default = 'resources/testimonial.mp3' 
        reference_speaker_female_default = 'resources/female_1.mp3' 

        target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)
        target_se_default_male, audio_name1 = se_extractor.get_se(reference_speaker_male_default, tone_color_converter, vad=False)
        target_se_default_female, audio_name2 = se_extractor.get_se(reference_speaker_female_default, tone_color_converter, vad=False)

        return target_se,tone_color_converter,target_se_default_male,target_se_default_female
        

    def generatorModelsAndParamsInitializer(self):
        language = "EN_NEWEST"
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model = TTS(language=language, device=device)
        speaker_ids = model.hps.data.spk2id

        speaker_key = "en-newest"
        speaker_id  = 0
        
        source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        
        return model,source_se,speaker_id
        

    async def async_iterator(self, file_path):
        async with aiofiles.open(file_path, "rb") as audio_file:
            while True:
                chunk = await audio_file.read(1024)  # Adjust chunk size as needed
                if not chunk:
                    break
                yield chunk


    async def delete_file(self,file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted")                


    async def generateAudio(self,text,target_se,model,source_se,speaker_id,tone_color_converter,speed,outputFormat):

        texts = {
            'EN_NEWEST': text, # The newest English base speaker model
        }

        output_dir = 'outputs_v2'

        speaker_key = "en-newest"

        gen_file_name = uuid.uuid4()

        # src_path = f'{output_dir}/tmp.wav'
        src_path = f'{output_dir}/{gen_file_name}.{outputFormat}'

        # Speed is adjustable
        # speed = 1.0
   
        # model.tts_to_file(text, speaker_id, src_path, speed=speed)

        # # save_path = f'{output_dir}/output_v2_{speaker_key}.wav'
        # save_path = f'{output_dir}/output_v2_{gen_file_name}.{outputFormat}'

        # # Run the tone color converter
        # encode_message = "@MyShell"
        # tone_color_converter.convert(
        #     audio_src_path=src_path, 
        #     src_se=source_se, 
        #     tgt_se=target_se, 
        #     output_path=save_path,
        #     message=encode_message)

        # Generate audio and save to file
        await self.tts_to_file_async(model, text, speaker_id, src_path, speed)

        save_path = f'{output_dir}/output_v2_{gen_file_name}.{outputFormat}'

        # Run the tone color converter
        # await self.convert_audio_async(tone_color_converter, src_path, source_se, target_se, save_path)
        
        # Run the tone color converter
        save_path = src_path
        # encode_message = "@MyShell"
        # tone_color_converter.convert(
        #     audio_src_path=src_path, 
        #     src_se=source_se, 
        #     tgt_se=target_se, 
        #     output_path=save_path,
        #     message=encode_message)
        
        return save_path


    async def tts_to_file_async(self, model, text, speaker_id, src_path, speed):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, model.tts_to_file, text, speaker_id, src_path, speed)

    async def convert_audio_async(self, tone_color_converter, src_path, source_se, target_se, save_path):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, tone_color_converter.convert, src_path, source_se, target_se, save_path, "@MyShell")

    