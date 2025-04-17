import time
import requests
from requests.exceptions import ChunkedEncodingError, RequestException, HTTPError
from config.api_config import DeepseekConfig


class LLMClient:
    @staticmethod
    def get_response(prompt: str, model_params: dict) -> str:
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            **model_params,
        }

        max_retries = 4
        base_delay = 5

        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    url=DeepseekConfig.BASE_URL + "/chat/completions",
                    headers=DeepseekConfig.HEADERS,
                    json=payload,
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

            except (ChunkedEncodingError, ConnectionError, RequestException) as e:
                if attempt >= max_retries:
                    raise RuntimeError(
                        f"API request failed after {max_retries} retries: {str(e)}"
                    )

                delay = base_delay * (2**attempt)
                print(f"Attempt {attempt + 1}/{max_retries}: Retrying in {delay}s...")
                time.sleep(delay)

            except HTTPError as e:
                raise RuntimeError(f"HTTP Error: {str(e)}")

            except KeyError as e:
                raise RuntimeError(f"Unexpected response format: {str(e)}")

        raise RuntimeError("Unexpected error in API communication")
