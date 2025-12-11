# fe-251020

```bash
conda create -p ./.venv python=3.13
conda activate ./.venv
pip install clerk-backend-api fastapi openai python-dotenv sqlalchemy uvicorn ruff

ruff format ./backend
```

## Ngrok

- Use [Chocolatey](https://chocolatey.org/install)
- Use [Scoop](https://scoop.sh/)

```bash
choco install ngrok
ngrok config add-authtoken

ngrok http 3000
```
