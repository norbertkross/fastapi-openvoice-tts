import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_v2'

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

reference_speaker = 'resources/testimonial.mp3' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

from melo.api import TTS

texts = {
    'EN_NEWEST': "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
}


src_path = f'{output_dir}/tmp.wav'

# Speed is adjustable
speed = 1.0

print("Hello")

for language, text in texts.items():
    model = TTS(language=language, device=device)
    speaker_ids = model.hps.data.spk2id
    
    for speaker_key in speaker_ids.keys():
        speaker_id = speaker_ids[speaker_key]
        speaker_key = speaker_key.lower().replace('_', '-')
        
        source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        model.tts_to_file(text, speaker_id, src_path, speed=speed)
        save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

        # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=save_path,
            message=encode_message)




    # def generateAudioOriginal(self,text): #target_se,device

    #     ckpt_converter = 'checkpoints_v2/converter'
    #     device = "cuda:0" if torch.cuda.is_available() else "cpu"
    #     output_dir = 'outputs_v2'

    #     tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    #     tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    #     os.makedirs(output_dir, exist_ok=True)

    #     reference_speaker = 'resources/testimonial.mp3' # This is the voice you want to clone
    #     # reference_speaker = 'resources/female_1.mp3' # This is the voice you want to clone
    #     target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

    #     from melo.api import TTS

    #     texts = {
    #         'EN_NEWEST': text, # "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
    #     }

    #     # output_dir = 'outputs_v2'
    #     src_path = f'{output_dir}/tmp.wav'

    #     # Speed is adjustable
    #     speed = 1.0

    #     # print("Hello")

    #     for language, text in texts.items():
    #         # print("l={} t={}".format(language,text)) --->  EN_NEWEST , text
    #         model = TTS(language=language, device=device)
    #         speaker_ids = model.hps.data.spk2id
            
    #         for speaker_key in speaker_ids.keys():
    #             speaker_id = speaker_ids[speaker_key]
    #             speaker_key = speaker_key.lower().replace('_', '-')

    #             print("speaker key")
    #             print(speaker_key) # en-newest
    #             print("speaker id")
    #             print(speaker_id) # 0 (int)
                
    #             source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
    #             model.tts_to_file(text, speaker_id, src_path, speed=speed)
    #             save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

    #             # Run the tone color converter
    #             encode_message = "@MyShell"
    #             tone_color_converter.convert(
    #                 audio_src_path=src_path, 
    #                 src_se=source_se, 
    #                 tgt_se=target_se, 
    #                 output_path=save_path,
    #                 message=encode_message)
        
    #     return save_path            