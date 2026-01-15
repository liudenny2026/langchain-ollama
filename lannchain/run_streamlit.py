import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """安装必要的依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "app/requirements.txt"])
        print("依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        sys.exit(1)

def check_ollama():
    """检查Ollama是否已安装"""
    try:
        import ollama
        # 尝试连接Ollama服务
        ollama.list()
        print("Ollama服务连接正常")
        return True
    except Exception as e:
        print(f"Ollama服务不可用，请确保Ollama已安装并运行: {e}")
        return False

def run_streamlit_app():
    """运行Streamlit应用"""
    print("正在启动Streamlit应用...")
    print("请在浏览器中打开 http://localhost:8501")
    subprocess.check_call([
        sys.executable, "-m", "streamlit", "run", 
        "app/main.py",
        "--server.address", "0.0.0.0",
        "--server.port", os.environ.get("PORT", "8501")
    ])

if __name__ == "__main__":
    print("LangChain Streamlit 多轮对话系统")
    print("="*40)
    
    install_dependencies()
    
    if check_ollama():
        run_streamlit_app()
    else:
        print("\n请先安装并启动Ollama，然后拉取所需的模型:")
        print("1. 下载并安装Ollama: https://ollama.ai")
        print("2. 运行命令: ollama pull qwen3:1.7b")
        print("3. 重新运行此脚本")