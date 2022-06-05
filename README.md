# Google AutoML Evaluation Script

## Setup

First create a virtualenv environment and activate it:

```bash
python3 -m virtualenv .venv
. .venv/bin/activte
```

Install the dependencies with pip:

```bash
pip3 install -r requirements.txt
```

## Run the code

```
docker run --rm -ti -v /home/jorge/gcp/creds:/creds google/cloud-sdk:latest /bin/bash
gcloud auth activate-service-account --key-file=/creds/automl-runner.json --project=minecraft-server-330203
gcloud auth application-default print-access-token
```
To run, execute the script after activating:

```bash
run_eval.py <json token> <image path>
```

Remember to press any key after the image shows to close it.
