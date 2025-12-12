FROM python:3.11-slim

RUN apt-get update && apt-get install -y git curl && apt-get clean

WORKDIR /app

RUN git clone https://github.com/lyanks/Team_2.Optimized-standings.git .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data /app/frames

EXPOSE 8501

CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
