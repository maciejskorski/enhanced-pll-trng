# docker build . -t maciejskorski/enhanced-pll-trng:v1.0

FROM jupyter/datascience-notebook:2023-06-01

RUN pip install --no-cache-dir mlflow

