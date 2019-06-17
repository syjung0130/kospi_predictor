#!/bin/sh
docker run -it --volume="$PWD/..:/workdir/predictor" --volume="$PWD/build:/workdir/build" scrapper:imx-1
