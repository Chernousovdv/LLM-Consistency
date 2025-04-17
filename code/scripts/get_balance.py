import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


def get_deepseek_balance(api_key: str) -> dict:
    """
    Fetch balance information from DeepSeek API

    Args:
        api_key: DeepSeek API key

    Returns:
        Dictionary containing balance information

    Raises:
        requests.exceptions.RequestException: If API request fails
        ValueError: If API returns invalid JSON
    """
    url = "https://api.deepseek.com/user/balance"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for 4XX/5XX responses
        return response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}") from e


def main():
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in .env file")

        balance_info = get_deepseek_balance(api_key)

        # Pretty print the response
        print("DeepSeek API Balance Information:")
        print(
            f"Is available: {balance_info.get('is_available', 'N/A')}\n"
            f"Total balance: {balance_info.get('balance_infos', [{}])[1].get('total_balance', 'N/A')} Yuan"
        )

    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
