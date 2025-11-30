# install python on this image
FROM python:3.13-slim

# install git
RUN apt-get update && apt-get install -y git && apt-get clean

#g o to app directory
WORKDIR /app

# clone repository to inside folder of docker app
RUN git clone https://github.com/lyanks/Team_2.Optimized-standings.git .

# install requirements (will later install)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# run file (test for now, do not have anuthing else in git yet)
CMD ["python", "test.py"]
