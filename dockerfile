FROM continuumio/miniconda3

RUN mkdir src
WORKDIR /src
COPY . .

# Support M1 with conda-forge
RUN conda install -c conda-forge --file requirements.txt -y
RUN python setup.py develop

# Start all jupyter inside folder notebooks
WORKDIR /src/notebooks
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
