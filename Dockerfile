# docker build . -t maciejskorski/enhanced-pll-trng:latest
# docker login
# docker push maciejskorski/enhanced-pll-trng:latest

# inherit data-science packages
FROM jupyter/datascience-notebook:2023-06-01

# install extra dependencies
RUN pip install --no-cache-dir mlflow

# copy repository data
#COPY . ${HOME}/work


