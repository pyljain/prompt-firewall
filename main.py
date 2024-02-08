from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline
from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from typing import List

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

conf_file = "./config.yaml"

# Create NLP engine based on configuration
provider = NlpEngineProvider(conf_file=conf_file)
nlp_engine = provider.create_engine()

# Pass the created NLP engine and supported_languages to the AnalyzerEngine
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine, 
    supported_languages=["en"]
)

class CheckInput(BaseModel):
    text: str

class CheckOutput(BaseModel):
    injection_status: str
    injection_score: float
    pii_detection: List

app = FastAPI()

@app.post("/check")
async def check(input: CheckInput) -> CheckOutput:
    start_time = time.perf_counter()
    # Assess if a prompt injection is detected 
    injection_result = classifier(input.text)[0]
     # Assess if PII is detected
    pii_result = analyzer.analyze(text=input.text, language="en")
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    # print time taken
    print("Elapsed time: ", elapsed_time * 1000)
    pii_entities = list(map(lambda x: x.entity_type, filter(lambda x: x.score > 0.75, pii_result)))

    # TODO: Models should run in parallel and not sequentially, chunking should be handled, GitLeaks should handle regex
    return CheckOutput(injection_status=injection_result['label'], injection_score=injection_result['score'], pii_detection=pii_entities)


