FROM python:3.11-slim

# タイムゾーンをAsia/Tokyoに固定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y curl gnupg && \
    curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash && \
    apt-get install -y speedtest && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bot/ .

CMD ["python", "main.py"]
