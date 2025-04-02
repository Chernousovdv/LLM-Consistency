import requests
from config.api_config import DeepseekConfig


class LLMClient:
    @staticmethod
    def get_response(prompt: str, model_params: dict) -> str:
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            **model_params,
        }

        try:
            response = requests.post(
                url=DeepseekConfig.BASE_URL + "/chat/completions",
                headers=DeepseekConfig.HEADERS,
                json=payload,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"API request failed: {str(e)}")
