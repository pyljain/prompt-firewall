from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline
from fastapi import FastAPI
from pydantic import BaseModel
import time

tokenizer = AutoTokenizer.from_pretrained("./deberta-v3-base-prompt-injection/onnx")
tokenizer.model_input_names = ["input_ids", "attention_mask"]
model = ORTModelForSequenceClassification.from_pretrained("./deberta-v3-base-prompt-injection/onnx", export=False)

classifier = pipeline(
  task="text-classification",
  model=model,
  tokenizer=tokenizer,
  truncation=True,
  max_length=512,
)

class CheckInput(BaseModel):
    text: str

class CheckOutput(BaseModel):
    label: str
    score: float

app = FastAPI()

@app.post("/check")
async def check(input: CheckInput) -> CheckOutput:
    start_time = time.perf_counter()
    result = classifier(input.text)[0]
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("Elapsed time: ", elapsed_time * 1000)
    return CheckOutput(label=result['label'], score=result['score'])


