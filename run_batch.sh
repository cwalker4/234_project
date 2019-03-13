#!/bin/sh
python youtube_recommendations.py --query="paul ryan" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query=gillibrand --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query=biden --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query="gavin newsom" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query="beto orourke" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query="ted cruz" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query="susan collins" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query="lindsay graham" --n_roots=7 --n_splits=2 --depth=8
python youtube_recommendations.py --query=kavanaugh --n_roots=7 --n_splits=2 --depth=8

