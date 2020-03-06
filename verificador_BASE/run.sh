#!/bin/bash

rm *.csv

scrapy crawl base -o data.csv -t csv

scrapy crawl racius -o racius.csv -t csv

python csv_union.py
