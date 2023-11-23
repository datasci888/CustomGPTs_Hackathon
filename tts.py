from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import numpy as np
from datasets import load_dataset
import torch
import soundfile as sf


class TTS:
    def __init__(self) -> None:
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(self.embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    
    def helper(self,prompt,ini):
        """
        generate_tts function help to generate audio in continuos format Beacuse pretrained models can only generate 
        audio till 600 tokens .

        """
        inputs = self.processor(text=prompt, return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder)

        return np.concatenate((ini , speech.numpy()))
    
    def generate_tts(self,prompt):
        """
        tts means text to speech function which genrates and saves audio file .
        """
        inputs = self.processor(text=prompt[:50], return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder).numpy()

        for i in range(100,1000,50):
            speech = self.helper(prompt[i-50:i],speech)

        sf.write(f"speech_output.wav", speech, samplerate=16000)
        
        return f"speech_output.wav"


## uncomment following in case you wanna test 😀

# obj = TTS()

# obj.generate_tts("""
#     CustomGPT hackathon Intructions - Psychological assistant:

# Instructional Prompt for GPT-4 
# Act as a Psychotherapist:
# Welcome message:

# Welcome to your personalized therapy session. I'm here to listen, support, and guide you toward emotional well-being and personal growth. Feel free to request a psychotherapy script tailored to your specific needs which is downloaded as a pdf on request.
# * Engage in Active Listening: When a user inputs a message, analyze the content for emotional tone, key concerns, and underlying issues. Respond empathetically, showing understanding and validation of the user's feelings and experiences. 
# * User Profiling: Based on the user's input and additional context, create a psychological profile. This should include potential stressors, emotional states, and any patterns in thought or behavior that emerge from the conversation. 
# * Generate Psychotherapy Scripts: Use the user's profile and therapy goals to generate initial psychotherapy scripts. These should be tailored to the individual's needs, offering coping strategies, reflective questions, and therapeutic advice. 
# * Provide Real-Time Support: Offer immediate, personalized responses to the user's queries and concerns. Ensure that the chatbot's replies are relevant, supportive, and conducive to a therapeutic environment. 
# * Integrate with Mental Health Resources: Where appropriate, suggest additional mental health resources, such as articles, exercises, or external services, that can complement the therapy session. 
# * Analyze Therapy Session Transcripts: Post-session, analyze the transcript using AI to identify areas of improvement, both in the user's mental health journey and in the chatbot's responses. Use these insights to refine future interactions and interventions. 
# * Focus on Accessibility and Cost-Effectiveness: Ensure that
# """)