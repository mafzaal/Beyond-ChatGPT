FROM python:3.12-slim
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user for security
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app



# Copy requirements first for better caching
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY --chown=user . $HOME/app

COPY . .

RUN --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true

EXPOSE 7860
CMD ["chainlit", "run", "app.py","--host","0.0.0.0", "--port", "7860"]

