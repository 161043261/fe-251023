from src.app import app
from uvicorn import run

if __name__ == "__main__":
    """
    Debug
    """
    run(app, host="0.0.0.0", port=3000)
