from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import asyncio
from prompt_injection import PromptInjectionDetector
from pii import PIIDetector
from gitleaks import GitLeaksDetector
from utils import in_thread

import time

app = FastAPI()

prompt_injection_detector = PromptInjectionDetector()
pii_detector = PIIDetector("./config.yaml")
git_leaks_detector = GitLeaksDetector()

class CheckInput(BaseModel):
    text: str

class CheckOutput(BaseModel):
    injection_status: str
    injection_score: float
    pii_detection: List
    git_leaks: List[str]

@app.post("/check")
async def check(input: CheckInput) -> CheckOutput:
    start_time = time.perf_counter()
    # Wait for all the parallel threads to complete
    results = await asyncio.gather(
        in_thread(prompt_injection_detector.classify, input.text), 
        in_thread(pii_detector.classify, text=input.text),
        in_thread(git_leaks_detector.classify, input.text),
    )
    injection_result = results[0]
    pii_result = results[1]
    git_leaks_result = results[2]
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    # print time taken
    print("Elapsed time: ", elapsed_time * 1000)
    pii_entities = list(map(lambda x: x.entity_type, filter(lambda x: x.score > 0.75, pii_result)))

    # TODO: Models should run in parallel and not sequentially, chunking should be handled, GitLeaks should handle regex
    return CheckOutput(
        injection_status=injection_result['label'], 
        injection_score=injection_result['score'], 
        pii_detection=pii_entities,
        git_leaks=git_leaks_result,
    )