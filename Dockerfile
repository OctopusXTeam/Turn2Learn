FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем директорию для данных и копируем только default_cards.json
RUN mkdir -p /app/data
COPY data/default_cards.json /app/data/

CMD ["python", "bot.py"] 