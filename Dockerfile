FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml README.md ./
COPY src ./src
COPY main.py ./

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "main.py"]
CMD ["--symbols", "AAPL"]
