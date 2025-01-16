from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from unsloth import FastLanguageModel
import torch
import uvicorn
max_seq_length = 2048
dtype = None
load_in_4bit = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',            # TODO уязвимость безопасности, в будущем указать разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="FWRust/text-sql-URFU-RTF-2C",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)
FastLanguageModel.for_inference(model)

alpaca_prompt = """You are a powerful text-to-SQL model. Your job is to answer questions about a database. You are given a question and context regarding one or more tables. You must output the SQL query that answers the question.

### Instruction:
{}

### Context:
{}

### Response:
{}"""


def pipe(prompt, context):
    inputs = tokenizer(
        [
            alpaca_prompt.format(
                prompt,  # instruction
                context,
                "",
            ),
        ], return_tensors="pt").to("cuda")

    outputs = model.generate(**inputs, max_new_tokens=64, use_cache=True)
    return (tokenizer.batch_decode(outputs))[0].split('### Response:', 1)[1][:-4]


class TextIn(BaseModel):
    prompt: str
    context: str


class TextOut(BaseModel):
    answer: str


@app.get("/info")
async def boot():
    return {'model_status':'ready', 'API_version': '1.0.0'}


@app.post('/request', response_model=TextOut)
async def request(payload: TextIn):
    answer = pipe(payload.prompt, payload.context)
    return {'answer': answer}

app.mount('/', StaticFiles(directory='static', html=True), name='static')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)