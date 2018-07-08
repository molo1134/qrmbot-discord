FROM gorialis/discord.py:full

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "qrmbot.py"]
