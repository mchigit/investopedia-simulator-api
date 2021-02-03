#!/usr/bin/env bash

rm -rf ./dist
rm -rf ./simulatorTradingApi.egg-info

python3 setup.py sdist bdist_wheel

python3 -m twine upload --repository testpypi dist/*
