#!/bin/bash
pushd $(dirname $0)

python3 -m venv ./venv
./venv/bin/pip install pillow ttkthemes copykitten
./venv/bin/python3 ./broBallGenerator.py

popd
