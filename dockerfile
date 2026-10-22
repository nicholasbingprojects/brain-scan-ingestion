FROM python:3.11-slim

# Install Node.js for official bids-validator CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    node.js \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g bids-validator

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "run_pipeline.py"]