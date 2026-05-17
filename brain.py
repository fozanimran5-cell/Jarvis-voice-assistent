import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL")
FALLBACK_MODELS = ["neural-chat", "llama2", "mistral", "dolphin-mixtral", "llama3", "lama"]


def _query_model(model, prompt):
    print(f"[Sending to Ollama: host={OLLAMA_HOST} model={model}]")
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )

    if response.status_code != 200:
        try:
            body = response.json()
        except Exception:
            body = response.text
        return False, response.status_code, body

    return True, response.json(), None


def _get_available_models():
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/models", timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()
        if isinstance(data, dict):
            models = data.get("models") or data.get("model")
            if isinstance(models, list):
                return [m.get("name") if isinstance(m, dict) and "name" in m else m for m in models]
        if isinstance(data, list):
            return [m.get("name") if isinstance(m, dict) and "name" in m else m for m in data]
    except Exception:
        return None

    return None


def ask_ai(prompt):
    """Send prompt to Llama via Ollama API. Set OLLAMA_MODEL to choose a model."""
    try:
        available_models = _get_available_models()
        if available_models is not None:
            if MODEL_NAME:
                if MODEL_NAME in available_models:
                    candidates = [MODEL_NAME]
                else:
                    print(f"[Requested model not installed: {MODEL_NAME}]")
                    candidates = [model for model in FALLBACK_MODELS if model in available_models]
                    if not candidates:
                        candidates = available_models.copy()
            else:
                candidates = [model for model in FALLBACK_MODELS if model in available_models]
                if not candidates:
                    candidates = available_models.copy()
        else:
            candidates = [MODEL_NAME] if MODEL_NAME else FALLBACK_MODELS

        for model in candidates:
            if not model:
                continue

            success, result, error = _query_model(model, prompt)
            if not success:
                if isinstance(error, dict) and error.get("error") and "not found" in str(error.get("error")).lower():
                    print(f"[Model not found: {model}]")
                    continue
                print(f"[Ollama error {result}: {error}]")
                return f"Ollama error {result}: {error}"

            if isinstance(result, dict) and "response" in result:
                return result["response"].strip()
            if isinstance(result, dict) and "results" in result and isinstance(result["results"], list) and result["results"]:
                first = result["results"][0]
                if isinstance(first, dict) and "content" in first:
                    return first["content"].strip()
                return str(first)
            return "No response from Llama"

        return (
            f"No Ollama model available. Tried: {', '.join(candidates)}. "
            "Run: ollama pull <model> and then ollama serve, or set OLLAMA_MODEL to a model you downloaded."
        )

    except requests.exceptions.ConnectionError:
        error_msg = (
            "Cannot connect to Ollama. Make sure Ollama is installed and running (ollama serve) "
            "and that a model is downloaded."
        )
        print(f"[Connection Error: {error_msg}]")
        return error_msg
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[Exception: {error_msg}]")
        return error_msg