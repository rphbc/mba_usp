FROM python:3.10-slim

WORKDIR /app

COPY api/ ./
COPY common/ ./common

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt punkt_tab stopwords wordnet omw-1.4 averaged_perceptron_tagger averaged_perceptron_tagger_eng

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
