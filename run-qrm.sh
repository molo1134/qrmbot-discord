#!/bin/bash

while true; do
    git pull;
    python qrmbot.py || exit 1;
done

