FROM python:3.10

EXPOSE 8501

WORKDIR /app

COPY producer/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY producer/producer.py .
CMD streamlit run producer.py

