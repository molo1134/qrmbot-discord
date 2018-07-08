# qrmbot-discord
port of molo1134/qrmbot to python and discord

## Dependencies

- Python 3.6
- discord.py
- feedparser

## OAuth Token

Add a file `secrets.json` with the contents:

```json
{
  "token": "ADD YOUR OAUTH TOKEN HERE"
}
```

## Deployment

Once `secrets.json` has been added, qrmbot can be deployed in Docker:

```
$ cd qrmbot_directory
$ docker build -t qrmbot .
$ docker run -d --rm --name qrmbot qrmbot
```

To restart:

```
$ docker stop qrmbot && docker run -d --rm --name qrmbot qrmbot
```

