# 4UOnly LOLCode Interpreter (CMSC 124)

## Run locally
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Share with ngrok
In a second terminal, while `app.py` is running:

    ngrok http 5000

Open the https URL that ngrok prints. Do not turn on Flask `debug=True` while a tunnel is open.

## Layout
- `app.py` Flask routes (`/` page, `/run` analyzer API)
- `analyzers/lexical_analyzer.py` Milestone 1
- `analyzers/syntax_analyzer.py` Milestone 2 
- `templates/`, `static/` frontend
- `test_lol/` sample .lol files
