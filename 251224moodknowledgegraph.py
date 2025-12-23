import streamlit as st
import os
from neo4j import GraphDatabase
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components

# 设置页面配置
st.set_page_config(
    page_title="让生命绽放光彩 - 知识图谱",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式自定义 (浅色主题，复刻 graph.html 风格)
st.markdown("""
<style>
    /* 全局背景 */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* 顶部导航栏模拟 */
    .top-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1rem;
        border-radius: 0 0 10px 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .css-1r6slb0, .css-12w0qpk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 侧边栏 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* 标题颜色 */
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    /* 统计卡片 */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# --- 数据处理 ---

DATA_FILE = 'knowledge_export_251224.txt'

def parse_txt_data():
    """解析本地 TXT 文件获取节点和关系"""
    nodes = []
    links = []
    current_section = None
    
    if not os.path.exists(DATA_FILE):
        return [], []

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line == 'Nodes:':
            current_section = 'nodes'
            continue
        elif line == 'Links:':
            current_section = 'links'
            continue
            
        if current_section == 'nodes':
            if line.startswith('- '):
                # - Name [Type]
                parts = line[2:].split(' [')
                name = parts[0]
                type_ = parts[1][:-1] if len(parts) > 1 else 'Unknown'
                nodes.append({'name': name, 'type': type_})
        
        elif current_section == 'links':
            if line.startswith('- '):
                # - Source -> Target (Label)
                try:
                    parts = line[2:].split(' -> ')
                    source = parts[0]
                    rest = parts[1].split(' (')
                    target = rest[0]
                    label = rest[1][:-1] if len(rest) > 1 else 'RELATED'
                    links.append({'source': source, 'target': target, 'label': label})
                except:
                    pass
                    
    return nodes, links

# --- Neo4j 连接 ---

def get_driver():
    try:
        # 优先尝试从 Streamlit Secrets 获取
        uri = st.secrets["NEO4J_URI"]
        user = st.secrets["NEO4J_USER"]
        password = st.secrets["NEO4J_PASSWORD"]
        return GraphDatabase.driver(uri, auth=(user, password))
    except Exception:
        return None

def get_graph_data(driver):
    """从数据库获取图谱数据"""
    nodes = []
    links = []
    if not driver:
        return parse_txt_data() # 回退到本地文件

    try:
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN n.name, n.type")
            for record in result:
                nodes.append({'name': record['n.name'], 'type': record['n.type']})
            
            result = session.run("MATCH (a)-[r]->(b) RETURN a.name, b.name, r.label")
            for record in result:
                links.append({'source': record['a.name'], 'target': record['b.name'], 'label': record['r.label']})
    except:
        return parse_txt_data() # 连接失败回退
        
    return nodes, links

# --- 界面逻辑 ---

def main():
    # 顶部 Header
    st.markdown("""
    <div class="top-header">
        <h1 style="color: white; margin: 0; font-size: 24px;">让生命绽放光彩 - 知识图谱</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">AI + 心理健康课程教学辅助系统</p>
    </div>
    """, unsafe_allow_html=True)

    # 侧边栏控制
    st.sidebar.title("控制面板")
    
    # 模式切换 (模拟 graph.html 的 tab)
    mode = st.sidebar.radio("视图模式", ["👨‍🎓 学生模式 (知识图谱)", "👨‍🏫 教师模式 (教学数据)"])
    
    # 获取数据
    driver = get_driver()
    nodes, links = get_graph_data(driver)
    
    if not nodes:
        st.warning("暂无数据，请确保已运行 upload_data.py 上传数据，或检查 knowledge_export_251224.txt 文件。")
        return

    if "教师" in mode:
        show_teacher_dashboard(nodes, links)
    else:
        show_student_view(nodes, links)

def show_teacher_dashboard(nodes, links):
    # 密码验证 (模拟 graph.html 的 admin888)
    if 'teacher_auth' not in st.session_state:
        st.session_state.teacher_auth = False
        
    if not st.session_state.teacher_auth:
        st.markdown("### 🔒 教师权限验证")
        pwd = st.text_input("请输入教师密码", type="password")
        if st.button("登录"):
            if pwd == "admin888":
                st.session_state.teacher_auth = True
                st.rerun()
            else:
                st.error("密码错误")
        return

    st.markdown("## 📊 教学数据看板")
    
    # 统计指标
    col1, col2, col3, col4 = st.columns(4)
    
    # 根据实际数据类型统计
    sections = [n for n in nodes if n['type'] == 'Section']
    topics = [n for n in nodes if n['type'] == 'Topic']
    subtopics = [n for n in nodes if n['type'] == 'SubTopic']
    
    col1.metric("总知识点数", len(nodes))
    col2.metric("核心章节", len(sections))
    col3.metric("二级主题", len(topics))
    col4.metric("知识关联", len(links))
    
    st.markdown("---")
    
    # 图表区域
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("知识点分布")
        # 简单统计各类型数量
        type_counts = {}
        for n in nodes:
            t = n['type']
            type_counts[t] = type_counts.get(t, 0) + 1
        st.bar_chart(type_counts)
        
    with c2:
        st.subheader("学生学习热度 (模拟)")
        # 模拟数据
        st.line_chart({
            "向死而生": 85,
            "转危为机": 62,
            "活出精彩": 93,
            "认识死亡": 45,
            "生命意义": 78
        })

    st.subheader("最近学习记录")
    st.table([
        {"学生ID": "2024001", "学习章节": "向死而生", "停留时长": "15min", "状态": "完成"},
        {"学生ID": "2024002", "学习章节": "转危为机", "停留时长": "8min", "状态": "进行中"},
        {"学生ID": "2024003", "学习章节": "活出精彩", "停留时长": "22min", "状态": "完成"},
    ])
    
    if st.button("退出教师模式"):
        st.session_state.teacher_auth = False
        st.rerun()

def show_student_view(nodes, links):
    col_main, col_info = st.columns([3, 1])
    
    with col_main:
        st.markdown("### 🕸️ 知识结构网络")
        
        # Pyvis 可视化
        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#333")
        
        # 颜色映射
        color_map = {
            'Root': '#ee6666',      # 红
            'Section': '#5470c6',   # 蓝
            'Topic': '#91cc75',     # 绿
            'SubTopic': '#fac858',  # 黄
            'Unknown': '#999999'
        }
        
        # 添加节点
        for n in nodes:
            color = color_map.get(n['type'], '#999999')
            size = 25
            if n['type'] == 'Root': size = 40
            elif n['type'] == 'Section': size = 30
            elif n['type'] == 'Topic': size = 20
            
            # Title 用于鼠标悬停显示内容
            # Pyvis 的 title 属性支持 HTML
            content_preview = n.get('content', '')
            # 截取一部分内容显示
            # 注意：这里我们无法直接从 txt 解析得到 content，因为 parse_txt_data 只解析了 Nodes/Links 结构
            # 如果需要 content，需要修改 parse_txt_data 或者在 knowledge_export_251224.txt 中包含 content
            # 目前 knowledge_export_251224.txt 确实包含了 content，但 parse_txt_data 没读取
            # 为了简化，我们暂时只显示名字
            
            net.add_node(n['name'], label=n['name'], title=n['name'], color=color, size=size)
            
        # 添加边
        for l in links:
            net.add_edge(l['source'], l['target'], title=l['label'], color='#cccccc')
            
        # 物理模拟配置
        net.force_atlas_2based()
        
        # 保存并展示
        try:
            path = tempfile.mktemp(suffix=".html")
            net.save_graph(path)
            with open(path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=620)
        except Exception as e:
            st.error(f"图谱渲染失败: {e}")
            
    with col_info:
        st.markdown("### 💡 知识点详情")
        st.info("在左侧图谱中探索知识点。")
        
        # 由于 Pyvis 在 Streamlit 中很难实现点击回调，我们用一个选择框来模拟“点击查看详情”
        selected_node_name = st.selectbox("选择知识点查看详情:", [n['name'] for n in nodes])
        
        if selected_node_name:
            st.markdown(f"#### {selected_node_name}")
            # 这里需要重新读取 content，或者优化数据结构
            # 简单起见，我们再次读取 txt 查找 content (性能较低但可行)
            content = "暂无详细内容"
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                capture = False
                for line in lines:
                    if line.startswith(f"- {selected_node_name} ["):
                        capture = True
                        continue
                    if capture:
                        if line.startswith("- ") or line.startswith("Links:"):
                            break
                        if not line.startswith("  keywords:"):
                            content = line.strip()
                            if content: break
            
            st.markdown(f">{content}")
            
            st.markdown("---")
            st.markdown("**相关资源:**")
            st.markdown("- 📄 [课程讲义.pdf](#)")
            st.markdown("- 📺 [教学视频](#)")

if __name__ == "__main__":
    main()
