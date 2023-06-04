# 基础镜像
FROM python:3.8
# 设置工作目录
WORKDIR /iotApps
# 复制文件到工作目录
COPY . /iotApps
# 安装所需要的库
RUN pip install --no-cache-dir -r requirements.txt
# 暴露端口
EXPOSE 8000
# 启动服务
CMD ["gunicorn","--bind","0.0.0.0:8000","--timeout","0","wsgi:application"]
