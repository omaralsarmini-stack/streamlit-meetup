@echo off
setlocal

set "PYTHON=.venv\Scripts\python.exe"
set "UV=%USERPROFILE%\.local\bin\uv.exe"

if exist "%PYTHON%" (
	"%PYTHON%" -m streamlit run hello.py
) else if exist "%UV%" (
	"%UV%" run --with streamlit streamlit run hello.py
) else (
	python -m streamlit run hello.py
)

endlocal
