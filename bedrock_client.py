# Bedrock Client Module with Rate Limiting
from tenacity import retry, wait_fixed, stop_after_attempt
from ratelimit import limits, sleep_and_retry
import boto3

# Initialize the Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Define rate limits (e.g., 5 requests per second)
REQUESTS_PER_SECOND = 5

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
@limits(calls=REQUESTS_PER_SECOND, period=1)
@sleep_and_retry
def invoke_model_with_retry(model_id: str, body: str) -> str:
    """Invokes the Bedrock model with retries and rate-limiting."""
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        response_body = []
        for chunk in response["body"].iter_chunks():
            response_body.append(chunk.decode("utf-8"))
        return ''.join(response_body)
    except Exception as e:
        print(f"Error invoking model: {e}")
        return ""
    except Exception as e:
        raise RuntimeError(f"Failed to invoke model: {e}")
    return response["body"].read().decode("utf-8")
