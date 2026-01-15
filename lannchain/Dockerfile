FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# 添加环境变量以连接到ollama服务
ENV OLLAMA_HOST=http://localhost:11434

CMD ["python", "-m", "streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]