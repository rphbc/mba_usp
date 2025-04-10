FROM python:3.10-slim

WORKDIR /app

COPY worker/ ./
COPY common/ ./common

COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt punkt_tab stopwords wordnet omw-1.4 averaged_perceptron_tagger averaged_perceptron_tagger_eng

CMD ["python", "consumer.py"]
