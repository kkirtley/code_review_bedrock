# Bedrock Client Module with Rate Limiting
from tenacity import retry, wait_fixed, stop_after_attempt
from ratelimit import limits, sleep_and_retry
import boto3
import json

# Initialize the Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Define rate limits (e.g., 5 requests per second)
REQUESTS_PER_SECOND = 5

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
@limits(calls=REQUESTS_PER_SECOND, period=1)
@sleep_and_retry
def invoke_model_with_retry(model_id: str, body: str) -> str:
    """Invokes the Bedrock model with retries and rate-limiting."""
    text_config = ",{\"maxTokenCount\":8192,\"stopSequences\":[],\"temperature\":0,\"topP\":1}}"
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps({"inputText": body}),
            contentType="application/json",
            accept="application/json"
        )
        response_body = []
        for chunk in response["body"].iter_chunks():
            response_body.append(chunk.decode("utf-8"))
        return ''.join(response_body)
    except Exception as e:
        raise RuntimeError(f"Failed to invoke model: {e}")
