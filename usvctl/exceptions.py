from httpx import Response
import json

class APIError(Exception):
    pass

def handle_api_response(response: Response):
    if response.status_code != 200:
        raise APIError(json.loads(response.content)["detail"])
