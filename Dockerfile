# install python (краще 3.11 для стабільності бібліотек)
FROM python:3.11-slim

# install git and curl
RUN apt-get update && apt-get install -y git curl && apt-get clean

# go to directory app
WORKDIR /app

# copy local files to docker inside app (ЗАМІСТЬ GIT CLONE)
COPY . .

# install python deps
RUN pip install --no-cache-dir -r requirements.txt
# про всяк випадок додаємо бібліотеки для сайту
RUN pip install --no-cache-dir streamlit plotly pandas numpy

# create folders
RUN mkdir -p /app/data /app/frames

# expose port
EXPOSE 8501

# Run web app
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
