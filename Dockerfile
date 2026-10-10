ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

COPY addon /app/addon
COPY requirements.txt /app/

CMD ["python", "addon/bundle_addon.py"]
