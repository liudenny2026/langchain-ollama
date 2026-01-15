import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
import ollama
import os

# 设置页面标题和配置
st.set_page_config(
    page_title="北京麦弗瑞科技有限公司智能对话系统",
    page_icon="🤖",
    layout="wide"
)

# 页面标题
st.title("🤖 北京麦弗瑞科技有限公司智能对话系统")
st.markdown("---")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏设置
st.sidebar.title("对话设置")

# Ollama服务器地址设置
ollama_host = st.sidebar.text_input("Ollama服务器地址", value="http://localhost:11434", help="输入Ollama服务器地址")

# 连接测试按钮
if st.sidebar.button("测试连接"):
    with st.sidebar:
        with st.spinner("正在连接Ollama服务器..."):
            try:
                # 设置环境变量以使用自定义主机
                if ollama_host != "http://localhost:11434":
                    os.environ['OLLAMA_HOST'] = ollama_host
                else:
                    # 如果是默认地址，确保环境变量未设置或已清除
                    if 'OLLAMA_HOST' in os.environ:
                        del os.environ['OLLAMA_HOST']
                
                # 测试连接
                models = ollama.list()
                if isinstance(models, dict) and 'models' in models:
                    model_names = [model['name'] for model in models['models']]
                else:
                    model_names = [model['name'] for model in models]
                
                st.success(f"✅ 连接成功！找到 {len(model_names)} 个模型")
                
                # 在侧边栏显示模型列表
                st.markdown("### 可用模型列表:")
                for model in model_names:
                    st.markdown(f"- `{model}`")
                
                # 更新session state以供后续使用
                st.session_state['ollama_connected'] = True
                st.session_state['available_models'] = model_names
                st.session_state['connection_error'] = None
                
            except Exception as e:
                st.error(f"❌ 连接失败: {str(e)}")
                st.session_state['ollama_connected'] = False
                st.session_state['available_models'] = ['qwen3:1.7b']  # 默认模型
                st.session_state['connection_error'] = str(e)

# 检查是否已连接并获取模型列表
if 'available_models' not in st.session_state:
    # 尝试默认连接
    try:
        models = ollama.list()
        if isinstance(models, dict) and 'models' in models:
            st.session_state['available_models'] = [model['name'] for model in models['models']]
        else:
            st.session_state['available_models'] = [model['name'] for model in models]
        st.session_state['ollama_connected'] = True
    except Exception:
        st.session_state['available_models'] = ['qwen3:1.7b']
        st.session_state['ollama_connected'] = False

# 模型选择
selected_model = st.sidebar.selectbox(
    "选择模型", 
    st.session_state['available_models'], 
    index=0 if 'qwen3:1.7b' in st.session_state['available_models'] else 0
)

# 温度设置
temperature = st.sidebar.slider("温度 (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="控制生成文本的随机性，值越高越随机")

# 最大预测token数
max_tokens = st.sidebar.slider("最大预测Token数", min_value=128, max_value=2048, value=512, step=64, help="控制生成文本的最大长度")

# 清除对话历史按钮
if st.sidebar.button("清除对话历史"):
    st.session_state.messages = []
    st.rerun()

# 检查Ollama服务是否可用
def check_ollama_service():
    try:
        # 使用当前设置的主机
        if ollama_host != "http://localhost:11434":
            os.environ['OLLAMA_HOST'] = ollama_host
        else:
            if 'OLLAMA_HOST' in os.environ:
                del os.environ['OLLAMA_HOST']
        
        ollama.list()
        return True
    except Exception as e:
        st.error(f"Ollama服务不可用: {e}")
        return False

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入
if prompt := st.chat_input("请输入您的消息..."):
    # 添加用户消息到历史记录
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 显示助手思考过程
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 正在思考中...")
        
        try:
            # 检查Ollama服务
            if check_ollama_service():
                # 使用LangChain的Ollama集成
                llm = Ollama(
                    model=selected_model,
                    temperature=temperature,
                    num_predict=max_tokens,
                    base_url=ollama_host if ollama_host != "http://localhost:11434" else None
                )
                
                # 提取对话历史作为上下文
                context = ""
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        context += f"Human: {msg['content']}\n"
                    else:
                        context += f"Assistant: {msg['content']}\n"
                
                # 构建完整提示
                full_prompt = f"{context}\nHuman: {prompt}\nAssistant: "
                
                # 调用LangChain的Ollama模型
                response = llm.invoke(full_prompt)
                
                # 显示并添加到历史记录
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                error_msg = f"Ollama服务不可用，请检查服务器地址和连接状态。"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except Exception as e:
            error_msg = f"处理请求时出现错误: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 显示当前对话轮数
st.sidebar.markdown(f"**当前对话轮数**: {len([m for m in st.session_state.messages if m['role'] == 'user'])}")

# 添加关于信息
st.sidebar.markdown("---")
st.sidebar.markdown("### 关于")
st.sidebar.markdown("这是一个基于LangChain和Ollama的多轮对话系统。")
st.sidebar.markdown("- 使用Streamlit构建界面")
st.sidebar.markdown("- 集成LangChain框架")
st.sidebar.markdown("- 支持多轮对话记忆")
st.sidebar.markdown("- 可自定义Ollama服务器地址")
st.sidebar.markdown("- 支持模型选择")
st.sidebar.markdown("- 可调节生成参数")