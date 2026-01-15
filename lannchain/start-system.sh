#!/bin/bash

# LangChain Ollama 一键启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：打印信息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    print_error "未找到Docker，请先安装Docker"
    exit 1
fi

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    print_error "Docker未运行，请启动Docker服务"
    exit 1
fi

print_info "检测到Docker已安装并运行"

# 构建并启动服务
print_info "正在构建并启动LangChain Ollama服务..."

docker-compose up --build