# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目的依赖文件（requirements.txt）
COPY requirements.txt .

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 复制除 config.py 外的所有文件
COPY . .

CMD ["python", "main.py"]