#!/bin/sh
python youtube_recommendations.py --query=mueller --n_roots=10 --n_splits=2 --depth=8
python youtube_recommendations.py --query=clinton --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query="cory booker" --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query=obama --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query="kevin mccarthy" --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query=kushner --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query=democrats --n_roots=10 --n_splits=2 --depth=8
python youtube_recommendations.py --query=republicans --n_roots=10 --n_splits=2 --depth=8
python youtube_recommendations.py --query=nra --n_roots=5 --n_splits=2 --depth=8
python youtube_recommendations.py --query="fox news" --n_roots=5 --n_splits=2 --depth=8

