# twitter-stream-archive

![](https://github.com/kevincoakley/twitter-stream-archive/workflows/Python%20package/badge.svg)
![Docker Test & Publish to ghcr.io](https://github.com/kevincoakley/twitter-stream-archive/workflows/Docker%20Test%20&%20Publish%20to%20ghcr.io/badge.svg)
[![codecov](https://codecov.io/gh/kevincoakley/twitter-stream-archive/branch/master/graph/badge.svg)](https://codecov.io/gh/kevincoakley/twitter-stream-archive)

Install twitter-stream-archive from source:

    $ git clone https://github.com/kevincoakley/twitter-stream-archive.git
    $ cd twitter-stream-archive
    $ pip install -r requirements.txt
    $ python setup.py install
    
Command line options and environment variables:

    $ twitter-stream-archive
    --debug
    --consumer-token [CONSUMER_TOKEN] - Twitter API Consumer Token. (Required)
    --consumer-token-secret [CONSUMER_TOKEN_SECRET] - Twitter API Consumer Token Secret. (Required)
    --access-token [ACCESS_TOKEN] - Twitter API Access Token. (Required)
    --access-token-secret [ACCESS_TOKEN_SECRET] - Twitter API Access Token Secret. (Required)
    --archive-path [ARCHIVE_PATH] - Path to Save Archived Tweets. (Required)
    --stream-track [STREAM_TRACK] - Comma Separated List of Terms to Apply to the Stream Filter.
    --stream-locations [STREAM_LOCATIONS] - Comma Separated List of Geo Coordinates to Apply to the Stream Filter.
    
Build twitter-stream-archive into a Docker container:

    $ git clone https://github.com/kevincoakley/twitter-stream-archive.git
    $ cd twitter-stream-archive
    $ docker build . --file Dockerfile --tag twitter-stream-archive
    
Run twitter-stream-archive from a Docker container:

    docker run --name twitter-stream-archive -d \
    -e CONSUMER_TOKEN='consumer-token' \
    -e CONSUMER_TOKEN_SECRET='consumer-token-secret' \
    -e ACCESS_TOKEN='access-token' \
    -e ACCESS_TOKEN_SECRET='access-token' \
    -e ARCHIVE_PATH='/twitter-stream-archive/' \
    -e STREAM_TRACK='track,terms' \
    -e STREAM_LOCATIONS='x1,y1,x2,y2' \
    -v '/local/path:/twitter-stream-archive/' \
    -p 8000:8000 \
    twitter-stream-archive