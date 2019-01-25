# Development

[![Build Status](https://travis-ci.org/dakl/tv-backlight-api.svg?branch=master)](https://travis-ci.org/dakl/tv-backlight-api)

## Run locally

~~~bash
python run.py
~~~

# Deplotyment

## Build & push

~~~bash
docker build -t dakl/tv-backlight-api .
docker push dakl/tv-backlight-api
~~~

## Run Container

~~~bash
docker run \
-e TV_BACKLIGHT_DEVICE_ID=(echo $TV_BACKLIGHT_DEVICE_ID) \
-e PARTICLE_ACCESS_TOKEN=(echo $PARTICLE_ACCESS_TOKEN) \
-p 8000:8000 \
dakl/tv-backlight-api
~~~
