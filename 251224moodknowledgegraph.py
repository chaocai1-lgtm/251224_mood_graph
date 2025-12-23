import streamlit as st
import os
from neo4j import GraphDatabase
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components

# 设置页面配置
st.set_page_config(
    page_title="AI+心理健康课程知识图谱",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式自定义 (浅色主题)
st.markdown("""
<style>
    .reportview-container {
        background: #f5f7fa;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
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
        # 本地回退 (或者提示配置)
        return None

def init_db(driver, nodes, links):
    if not driver:
        return False
    
    with driver.session() as session:
        # 清空旧数据
        session.run("MATCH (n) DETACH DELETE n")
        
        # 创建节点
        for n in nodes:
            session.run(
                "CREATE (n:Concept {name: $name, type: $type})",
                name=n['name'], type=n['type']
            )
            
        # 创建关系
        for l in links:
            session.run(
                """
                MATCH (a:Concept {name: $source}), (b:Concept {name: $target})
                CREATE (a)-[:RELATION {label: $label}]->(b)
                """,
                source=l['source'], target=l['target'], label=l['label']
            )
    return True

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
    st.sidebar.title("控制面板")
    
    # 模式切换
    mode = st.sidebar.radio("选择视图模式", ["学生模式 (知识图谱)", "教师模式 (教学分析)"])
    
    # 数据库管理 (折叠)
    with st.sidebar.expander("数据库管理 (管理员)"):
        st.write("如果这是首次部署，请点击下方按钮初始化数据库。")
        if st.button("初始化/重置数据库"):
            driver = get_driver()
            if driver:
                nodes, links = parse_txt_data()
                if init_db(driver, nodes, links):
                    st.success(f"成功导入 {len(nodes)} 个节点, {len(links)} 条关系！")
                else:
                    st.error("导入失败")
            else:
                st.error("未检测到数据库连接配置 (Secrets)")

    # 获取数据
    driver = get_driver()
    nodes, links = get_graph_data(driver)
    
    if not nodes:
        st.warning("暂无数据，请先在侧边栏初始化数据库，或检查 knowledge_export_251224.txt 文件。")
        return

    if mode == "教师模式 (教学分析)":
        show_teacher_dashboard(nodes, links)
    else:
        show_knowledge_graph(nodes, links)

def show_teacher_dashboard(nodes, links):
    st.title("📊 教学分析看板")
    
    # 统计指标
    col1, col2, col3, col4 = st.columns(4)
    
    pain_points = [n for n in nodes if n['type'] == 'PainPoint']
    methods = [n for n in nodes if n['type'] == 'Method']
    mechanisms = [n for n in nodes if n['type'] == 'Mechanism']
    modules = [n for n in nodes if n['type'] == 'Module']
    
    col1.metric("学生痛点", len(pain_points), "+2")
    col2.metric("干预方法", len(methods), "+5")
    col3.metric("理论机制", len(mechanisms))
    col4.metric("课程章节", len(modules))
    
    st.markdown("---")
    
    # 图表区域
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("痛点分布 (Top 5)")
        # 模拟数据，实际可从数据库聚合
        st.bar_chart({"大学适应": 15, "自我认知": 12, "情绪失控": 10, "人际冲突": 8, "学业压力": 6})
        
    with c2:
        st.subheader("方法使用热度")
        st.line_chart({"腹式呼吸": 45, "正念冥想": 38, "认知重构": 30, "蝴蝶拍": 25})

    st.subheader("最近预警记录")
    st.table([
        {"学生ID": "2024001", "痛点": "情绪失控", "触发机制": "前额叶失控", "推荐方法": "蝴蝶拍", "状态": "已干预"},
        {"学生ID": "2024002", "痛点": "持续低落", "触发机制": "多巴胺不足", "推荐方法": "运动激活", "状态": "跟进中"},
        {"学生ID": "2024003", "痛点": "社交恐惧", "触发机制": "杏仁核过敏", "推荐方法": "系统脱敏", "状态": "待处理"},
    ])

def show_knowledge_graph(nodes, links):
    st.title("🧠 心理健康知识图谱")
    
    # 搜索框
    search_term = st.text_input("搜索知识点...", "")
    
    # Pyvis 可视化
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#333")
    
    # 颜色映射
    color_map = {
        'Module': '#5470c6',    # 蓝
        'Mechanism': '#91cc75', # 绿
        'Method': '#fac858',    # 黄
        'PainPoint': '#ee6666', # 红
        'Unknown': '#999999'
    }
    
    # 添加节点
    for n in nodes:
        color = color_map.get(n['type'], '#999999')
        # 如果搜索匹配，高亮
        if search_term and search_term in n['name']:
            color = "#ff00ff"
            size = 30
        else:
            size = 20 if n['type'] == 'PainPoint' else 15
            
        net.add_node(n['name'], label=n['name'], title=n['type'], color=color, size=size)
        
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

if __name__ == "__main__":
    main()
