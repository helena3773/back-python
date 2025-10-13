# ============================
# Stage 1 — Build dependencies
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc pkg-config default-libmysqlclient-dev libopenmpi-dev openmpi-bin && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# ---- 핵심 수정 부분 ----
RUN pip install --upgrade pip setuptools wheel && \
    pip install "numpy<2.0" cython==0.29.36 && \
    pip install --no-cache-dir -r requirements.txt
# ------------------------

# ============================
# Stage 2 — Final runtime image
# ============================
FROM python:3.11-slim

WORKDIR /app

# ✅ Chromium 설치 (Google Chrome 대신)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb3 default-libmysqlclient-dev \
        chromium chromium-driver fonts-liberation libglib2.0-0 libnss3 libx11-xcb1 \
        libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 \
        libasound2 libatk-bridge2.0-0 libxss1 libgtk-3-0 libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# ✅ 환경 변수 등록 — chromedriver_autoinstaller가 chromium을 인식하도록
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMIUM_PATH=/usr/bin/chromium \
    PATH=$PATH:/usr/lib/chromium/

# OpenMPI 등 필요한 런타임 라이브러리 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 libsm6 libxext6 libxrender1 libopenmpi-dev openmpi-bin && \
    rm -rf /var/lib/apt/lists/*

# ---- 핵심 수정 부분 ----
# builder에서 site-packages를 그대로 복사
COPY --from=builder /usr/local /usr/local
# ------------------------

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
