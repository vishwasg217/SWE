#!/bin/sh
cd api_design || exit
uvicorn app.main:app --host=0.0.0.0 --port="${PORT:-5000}"
