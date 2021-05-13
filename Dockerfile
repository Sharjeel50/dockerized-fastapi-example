FROM python:3.8-slim
WORKDIR /all
COPY . /all
RUN pip install -r requirements.txt
WORKDIR app
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
