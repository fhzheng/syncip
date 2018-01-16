#! /bin/sh
cd $(pwd)
NOW=$(date +"%Y-%m-%d")
FILE="${NOW}.log"
python main.py >> "logs/$FILE"
