# Guardrails prototype

A prototype to execute checks that will serve as active guardrails for core services. Checks covered include - prompt injection checks, PII detection, regex based checks. A core part of this prototype explore running these checks in parallel to make this invocation time efficient.

## Prerequisite
Download the `deid_roberta_i2b2` model to a local (or globally accessible) directory.

## Setup

```sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run
```sh
make run # Run server
make test # Run a sample test
```

## TO DOs
1. Handle chunking
1. Handle chunks in parallel 
1. Write tests
1. Test performance / RTT
1. Add more patterns to GitLeaks
