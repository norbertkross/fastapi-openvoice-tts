# Use the official Miniconda3 image as a base
FROM continuumio/miniconda3

# Set up the environment
ENV CONDA_ENV=openvoice
ENV PATH /opt/conda/envs/$CONDA_ENV/bin:$PATH

# Create the Conda environment and install packages
RUN conda create -n $CONDA_ENV python=3.9 && \
    conda install -n $CONDA_ENV -c conda-forge numba librosa bokeh umap-learn h5py llvmlite && \
    conda clean -a

# Initialize conda
RUN conda init

# Install pyworld using pip in the environment
# RUN conda run -n $CONDA_ENV pip install pyworld

# Set the working directory
WORKDIR /app

# Copy your project files into the container (optional)
COPY . /app

# Clear pip cache
RUN conda run -n openvoice pip cache purge

# Install dependencies for dtw-python
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev

# Install necessary Python packages
RUN conda run -n openvoice pip install numpy==1.22.0 setuptools wheel Cython


# Install your package if you have a setup.py (adjust if needed)
RUN conda run -n $CONDA_ENV pip install dtw-python
RUN conda run -n $CONDA_ENV pip install melo
RUN conda run -n $CONDA_ENV pip install pydub
RUN conda run -n $CONDA_ENV pip install aiofiles

RUN conda run -n $CONDA_ENV pip install -e .

# Install MeloTTS from GitHub
RUN conda run -n $CONDA_ENV pip install git+https://github.com/myshell-ai/MeloTTS.git

# Run the unidic download command
RUN conda run -n $CONDA_ENV python -m unidic download

RUN apt update
RUN apt install ffmpeg -y

# Install FastAPI and Uvicorn
RUN conda run -n $CONDA_ENV pip install fastapi uvicorn

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Install any remaining packages with pip if necessary
RUN conda run -n $CONDA_ENV pip install cardboardlint
RUN conda run -n $CONDA_ENV pip install --no-cache-dir -r requirements.txt


# Use the conda run to set the default command to start the FastAPI application
CMD ["conda", "run", "-n", "openvoice", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
