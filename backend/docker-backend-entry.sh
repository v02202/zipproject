#!/bin/bash
while ! nc -z db 5432; do sleep 3; done
uvicorn app:app --host 0.0.0.0 --reload