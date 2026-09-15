# --------------------------
# 构建阶段：安装所有依赖
# --------------------------
FROM python:3.12-slim AS builder 

# 工作目录
WORKDIR /app

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 uv
RUN pip install uv

# 拷贝依赖描述文件
COPY pyproject.toml uv.lock ./

# 创建虚拟环境，安装所有依赖
RUN uv sync  

# --------------------------
# 运行阶段：轻量化运行镜像
# --------------------------
FROM python:3.12-slim

WORKDIR /app

# 从构建阶段拷贝虚拟环境
COPY --from=builder /app/.venv /runtime/.venv

# 激活venv（把venv的bin加到PATH）
ENV PATH="/runtime/.venv/bin:$PATH"