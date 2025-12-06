# instal python
FROM python:3.13-slim

# install git
RUN apt-get update && apt-get install -y git && apt-get clean

# got to directory app
WORKDIR /app

# clone repo to docher inside app
RUN git clone https://github.com/lyanks/Team_2.Optimized-standings.git .

# install requirements (will write later)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Run file (for now test file)
CMD ["python", "main.py"]
