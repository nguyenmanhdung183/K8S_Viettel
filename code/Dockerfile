# Sử dụng image cơ sở
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép các tệp yêu cầu và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Sao chép thư mục instance vào container
COPY instance /app/instance

# Chạy ứng dụng
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
