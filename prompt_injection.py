from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline


class PromptInjectionDetector():
    def __init__(self) -> None:
        tokenizer = AutoTokenizer.from_pretrained("./deberta-v3-base-prompt-injection/onnx")
        tokenizer.model_input_names = ["input_ids", "attention_mask"]
        model = ORTModelForSequenceClassification.from_pretrained("./deberta-v3-base-prompt-injection/onnx", export=False)
        self._classifier = pipeline(
            task="text-classification",
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            max_length=512,
        )

    def classify(self, text):
        return self._classifier(text)[0]