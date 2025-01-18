# Main script for orchestrating the code review process
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from utils import collect_valid_files, calculate_token_count, split_large_file
from bedrock_client import invoke_model_with_retry
from report_generator import generate_html_report

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ModelRequest(BaseModel):
    model_id: str
    body: str

@app.post("/invoke_model")
def invoke_model(request: ModelRequest):
    try:
        result = invoke_model_with_retry(request.model_id, request.body)
        if not result:
            raise HTTPException(status_code=500, detail="Model invocation failed")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
