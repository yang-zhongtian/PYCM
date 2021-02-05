#!/bin/sh -l

pip install --no-cache-dir requests

py_output=$(python -c "import requests; print(requests.get('https://api.github.com/repos/yangzhongtian001/PYCM/releases/tags/' + '$0'.replace('refs/tags/', '')).json().get('upload_url'))")

echo "::set-output name=upload_url::$py_output"