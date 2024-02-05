run: 
	uvicorn main:app --reload

test: 
	curl -X POST -v -H "content-type: application/json" -d @sample-two.json http://localhost:8000/check

# 	pip install --upgrade-strategy eager install optimum[onnxruntime]
