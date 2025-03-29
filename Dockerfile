FROM python

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5800
CMD ["python3", "app.py"]