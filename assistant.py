from openai import OpenAI
from config import Config
from scripts import read_file
import time

client = OpenAI(api_key=Config.open_ai_key)

## 1. Read the instructions 

instructions = read_file(file_path="files/message.txt")

## 2. Creation of file objects for retrival
meditation_script_file = client.files.create(
  file=open("files/Meditation_Script.docx", "rb"),
  purpose='assistants'
)

thesis_file = client.files.create(
  file=open("files/Thesis_till_literature_review_.docx", "rb"),
  purpose='assistants'
)

## 3. Creation of assistant object

assistant = client.beta.assistants.create(
    name = "Emo",
    instructions = instructions,
    tools=[{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids= [
        meditation_script_file.id,
        thesis_file.id
    ]
)

## 4. Creation of thread

thread = client.beta.threads.create()

## Creation of function to and getting answers from LLM.

def call(message_content : str ):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content
    )

    runs = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    

    while True : 
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=runs.id
        )
        if run.status == "completed":
            break
            

    output = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return output.json()

