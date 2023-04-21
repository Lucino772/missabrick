# MissABrick

Miss A Brick is a small app that allows you to search for Lego sets and download a excel file containing all the parts. The data comes from the website [rebrickable.com](https://rebrickable.com/downloads/).

# Build and run

You can build the image for this app by simply running the following command:
```shell
docker build -t missabrick:latest .
```

An then run the app:
```shell
docker run -d -p 8080:8080 missabrick:latest
```

You can also juste pull the image from GitHub Container registry:
```shell
docker pull ghcr.io/lucino772/missabrick:main
```