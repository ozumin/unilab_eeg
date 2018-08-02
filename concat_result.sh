#!/bin/bash
echo "clean result.csv"
rm -rf data/result.csv

echo "concatenate dataframe..."
cat data/base.csv data/*result.csv > data/result.csv

echo "draw dendrogram..."
Rscript dend.R

echo "open pdf..."
open cluster.pdf