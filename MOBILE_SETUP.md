# PC Setup (Streamlit)

This project is now PC-only.

## Start App (Windows PowerShell)

```powershell
.\run_streamlit.ps1
```

Open:

```text
http://localhost:8503
```

## If First Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then run:

```powershell
.\run_streamlit.ps1
```

## Quick Troubleshooting

- If port 8503 is busy, close old Python/Streamlit processes and run again.
- If dependencies are missing, re-run `pip install -r requirements.txt` in `.venv`.
