#!/usr/bin/env bash
set -e

if [ -x ".venv/bin/python" ]; then
	.venv/bin/python -m streamlit run hello.py
else
	python3 -m streamlit run hello.py
fi
