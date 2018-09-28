FROM gorialis/discord.py:3.7-rewrite-extras

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN apt update && \
    apt-get install -y texlive-full \
    > /dev/null && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["./run-qrm.sh"]
