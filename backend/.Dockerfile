FROM python:3.12

WORKDIR /backend

ENV Api_key="ab53d75a6bf0364d4b54acc37f31849a"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]