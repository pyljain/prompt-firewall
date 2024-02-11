from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PIIDetector():
    def __init__(self, conf_file) -> None:
        provider = NlpEngineProvider(conf_file=conf_file)
        nlp_engine = provider.create_engine()

        self._analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine, 
            supported_languages=["en"]
        )

    def classify(self, text="", language="en"):
        return self._analyzer.analyze(text=text, language=language)
