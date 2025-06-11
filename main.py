# Main script for orchestrating the code review process
"""_summary_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
from bedrock_client import invoke_model_with_retry
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ModelRequest(BaseModel):
    """
    ModelRequest represents a request to a model with the specified model ID and body content.

    Attributes:
        model_id (str): The unique identifier of the model.
        body (str): The content or payload to be processed by the model.
    """
    model_id: str
    body: str

@app.post("/invoke_model")
def invoke_model(request: ModelRequest):
    """
    Invokes a model with the given request and handles retries and exceptions.

    Args:
        request (ModelRequest): The request object containing the model ID and request body.

    Returns:
        dict: A dictionary containing the result of the model invocation.

    Raises:
        HTTPException: If the model invocation fails or an exception occurs during the process.
    """
    try:
        result = invoke_model_with_retry(request.model_id, request.body)
        if not result:
            raise HTTPException(status_code=500, detail="Model invocation failed")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
