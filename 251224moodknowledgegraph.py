import streamlit as st
import json
import os
from datetime import datetime
from neo4j import GraphDatabase
from streamlit_agraph import agraph, Node, Edge, Config

# =============================================
# 页面配置
# =============================================
st.set_page_config(
    page_title="让生命绽放光彩 - 知识图谱",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# 知识数据（与 graph.html 完全一致）
# =============================================
KNOWLEDGE = {
    "让生命绽放光彩": {"type": "center", "content": "本讲围绕「生命」这一核心主题，从认识死亡、探索意义、应对危机、积极生活四个维度展开。通过理解死亡的必然性，反思生命的有限与珍贵，学会在危机中成长，最终活出属于自己的精彩人生。", "keywords": ["生命教育", "心理健康", "积极心理学"]},
    "向死而生": {"type": "section", "content": "海德格尔提出「向死而生」的哲学概念——只有真正认识死亡，才能深刻理解生命的意义。本章探讨死亡的本质、人们面对死亡的态度，以及死亡对于理解生命价值的启示。", "keywords": ["死亡认知", "生命有限性", "存在主义"]},
    "认识死亡": {"type": "topic", "content": "医学上死亡经历三个阶段：濒死期（意识模糊、反应迟钝）、临床死亡期（心跳呼吸停止）、生物学死亡期（不可逆的细胞死亡）。人们对死亡的恐惧往往源于对未知的恐惧。", "keywords": ["濒死期", "临床死亡", "脑死亡"]},
    "死亡态度": {"type": "topic", "content": "面对死亡的态度：文化层面不让提（死亡禁忌）、心理层面不敢提（恐惧回避）、认知层面不需提（否认逃避）。库伯勒-罗斯提出悲伤五阶段：震惊、否认、愤怒、抑郁、接受。", "keywords": ["死亡禁忌", "悲伤阶段", "心理防御"]},
    "死亡特征": {"type": "topic", "content": "死亡三大特征：必然性（有生必有死）、偶然性（何时何地不可预测）、终结性（失去一切所拥有的）。正是这些特征提醒我们珍惜当下。", "keywords": ["必然性", "偶然性", "终结性"]},
    "生命意义": {"type": "section", "content": "弗兰克尔《活出生命的意义》指出：人可以被剥夺一切，唯独不能被剥夺选择态度的自由。探索生命意义是人类永恒的追问，也是心理健康的重要基石。", "keywords": ["意义疗法", "价值追求", "存在意义"]},
    "生命特征": {"type": "topic", "content": "生命五大特征：有限性（时间有限）、双重属性（自然性与社会性）、创造性（不断创造新内容）、超越性（能够超越自己）、珍贵性（每个生命都是奇迹）。", "keywords": ["有限性", "双重属性", "创造性"]},
    "意义作用": {"type": "topic", "content": "生命意义的作用：体会生活意义（承担责任带来满足）、确立生活目标（设定人生方向）、增强心理韧性（提高挫折耐受力）。尼采说：知道为什么而活的人，能承受任何怎样活。", "keywords": ["生活目标", "心理韧性", "责任承担"]},
    "琼瑶启示": {"type": "topic", "content": "2024年12月，86岁的琼瑶选择翩然离去。遗书写道：我是火花，我已尽力燃烧过...我活过了，不曾辜负此生！她的选择引发关于生命自主权和死亡尊严的深度思考。", "keywords": ["生命自主", "死亡尊严", "不负此生"]},
    "转危为机": {"type": "section", "content": "心理危机是生活中不可避免的挑战。危机中蕴含着危险，也蕴含着机遇。学会识别危机信号、理解危机反应、掌握应对方法，可以帮助我们在逆境中成长。", "keywords": ["心理危机", "危机干预", "逆境成长"]},
    "危机概念": {"type": "topic", "content": "心理危机三要素：危机事件发生、感知导致主观痛苦、惯常应对方式失效。心理危机不是疾病，而是情感危机反应，多数可在6-8周内自然缓解。", "keywords": ["心理失衡", "应对失效", "情感反应"]},
    "危机特征": {"type": "topic", "content": "心理危机五大特征：突发性（难以控制）、无助性（不知所措）、危险性（影响生活甚至生命）、潜在性（长期积累后爆发）、复杂性（多因素交织）。", "keywords": ["突发性", "无助感", "复杂性"]},
    "危机类型": {"type": "topic", "content": "心理危机三类：成长性危机（发展阶段转换）、境遇性危机（突发外部事件）、存在性危机（人生意义困惑）。不同类型需要不同的应对策略。", "keywords": ["成长性", "境遇性", "存在性"]},
    "危机识别": {"type": "topic", "content": "危机预警信号：情绪异常（持续低落、焦虑）、行为改变（睡眠饮食紊乱）、学习下降、损毁物品、言语暗示（谈论死亡、告别）。发现信号请及时寻求帮助！", "keywords": ["预警信号", "早期识别", "及时求助"]},
    "活出精彩": {"type": "section", "content": "认识了死亡、理解了意义、学会了应对危机，最终目标是活出精彩的人生。积极心理学告诉我们：幸福不是终点，而是一种生活方式。", "keywords": ["积极生活", "幸福感", "自我实现"]},
    "活在当下": {"type": "topic", "content": "正念（Mindfulness）：专注于现在正在经历的事、留意身边发生的幸福小事、用心感受每一个当下。幸福往往藏在平凡时刻中。", "keywords": ["正念", "当下觉知", "幸福感知"]},
    "自我价值": {"type": "topic", "content": "实现自我价值的路径：设定阶段性目标、培养核心能力、持之以恒努力、在实践中调整。马斯洛需求层次理论：自我实现是人类最高层次的需求。", "keywords": ["目标设定", "能力培养", "自我实现"]},
    "亲密关系": {"type": "topic", "content": "良好人际关系是心理健康的保护因素：提供情感支持和归属感、帮助缓解压力、促进个人成长。哈佛85年研究表明：良好人际关系是预测幸福的最重要因素。", "keywords": ["社会支持", "情感连接", "幸福因素"]},
    "敬畏生命": {"type": "topic", "content": "罗曼·罗兰：世界上只有一种真正的英雄主义，那就是认清生活真相后，依旧热爱生活。敬畏生命：尊重自己和他人的生命、在困难中保持希望。", "keywords": ["热爱生活", "英雄主义", "生命尊重"]}
}

# 图谱节点配置 (加大尺寸以容纳文字，仿 ECharts 样式)
NODES_CONFIG = [
    {"id": "让生命绽放光彩", "size": 60, "color": "#5470c6"},
    {"id": "向死而生", "size": 45, "color": "#91cc75"},
    {"id": "生命意义", "size": 45, "color": "#91cc75"},
    {"id": "转危为机", "size": 45, "color": "#91cc75"},
    {"id": "活出精彩", "size": 45, "color": "#91cc75"},
    {"id": "认识死亡", "size": 35, "color": "#fac858"},
    {"id": "死亡态度", "size": 35, "color": "#fac858"},
    {"id": "死亡特征", "size": 35, "color": "#fac858"},
    {"id": "生命特征", "size": 35, "color": "#fac858"},
    {"id": "意义作用", "size": 35, "color": "#fac858"},
    {"id": "琼瑶启示", "size": 35, "color": "#ee6666"},
    {"id": "危机概念", "size": 35, "color": "#fac858"},
    {"id": "危机特征", "size": 35, "color": "#fac858"},
    {"id": "危机类型", "size": 35, "color": "#fac858"},
    {"id": "危机识别", "size": 35, "color": "#ee6666"},
    {"id": "活在当下", "size": 35, "color": "#fac858"},
    {"id": "自我价值", "size": 35, "color": "#fac858"},
    {"id": "亲密关系", "size": 35, "color": "#fac858"},
    {"id": "敬畏生命", "size": 35, "color": "#ee6666"}
]

# 图谱关系（包含标签）
LINKS = [
    {"source": "让生命绽放光彩", "target": "向死而生", "label": "包含"},
    {"source": "让生命绽放光彩", "target": "生命意义", "label": "包含"},
    {"source": "让生命绽放光彩", "target": "转危为机", "label": "包含"},
    {"source": "让生命绽放光彩", "target": "活出精彩", "label": "包含"},
    {"source": "向死而生", "target": "认识死亡", "label": "探讨"},
    {"source": "向死而生", "target": "死亡态度", "label": "分析"},
    {"source": "向死而生", "target": "死亡特征", "label": "总结"},
    {"source": "生命意义", "target": "生命特征", "label": "认识"},
    {"source": "生命意义", "target": "意义作用", "label": "理解"},
    {"source": "生命意义", "target": "琼瑶启示", "label": "反思"},
    {"source": "转危为机", "target": "危机概念", "label": "定义"},
    {"source": "转危为机", "target": "危机特征", "label": "分析"},
    {"source": "转危为机", "target": "危机类型", "label": "分类"},
    {"source": "转危为机", "target": "危机识别", "label": "掌握"},
    {"source": "活出精彩", "target": "活在当下", "label": "实践"},
    {"source": "活出精彩", "target": "自我价值", "label": "追求"},
    {"source": "活出精彩", "target": "亲密关系", "label": "建立"},
    {"source": "活出精彩", "target": "敬畏生命", "label": "升华"},
    # 跨章节关联（虚线）
    {"source": "死亡特征", "target": "生命特征", "label": "对比", "dashed": True},
    {"source": "死亡态度", "target": "危机识别", "label": "关联", "dashed": True},
    {"source": "琼瑶启示", "target": "敬畏生命", "label": "启发", "dashed": True},
    {"source": "意义作用", "target": "自我价值", "label": "驱动", "dashed": True},
    {"source": "危机类型", "target": "活在当下", "label": "应对", "dashed": True},
    {"source": "认识死亡", "target": "敬畏生命", "label": "升华", "dashed": True}
]

# =============================================
# 样式（复刻 graph.html - 单屏适配版）
# =============================================
st.markdown("""
<style>
    /* 全局背景 + 适配视口 */
    .stApp {
        background-color: #f5f7fa;
        overflow: hidden;
    }
    
    /* 彻底隐藏顶部 Header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 主容器紧凑 - 顶部无间距 */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 减小分隔线间距 */
    hr { margin: 0.3rem 0 !important; }
    
    /* 顶部导航栏 - 贴顶 */
    .top-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 10px 24px;
        margin: 0 -1rem 0.5rem -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 0 0 8px 8px;
    }
    .top-header h1 {
        font-size: 17px;
        margin: 0;
        color: white !important;
    }
    .top-header p {
        font-size: 11px;
        opacity: 0.85;
        margin: 2px 0 0 0;
    }
    
    /* 卡片样式 - 紧凑 */
    .detail-card {
        background: #fff;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 8px;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .detail-card h3 {
        font-size: 13px;
        margin-bottom: 6px;
        color: #333;
    }
    .tag {
        font-size: 9px;
        padding: 2px 7px;
        border-radius: 10px;
        background: #667eea;
        color: #fff;
        margin-right: 6px;
    }
    .content-text {
        font-size: 11px;
        line-height: 1.5;
        color: #555;
        margin-top: 5px;
    }
    .kw {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 10px;
        margin: 2px 3px 2px 0;
    }
    
    /* 子卡片 */
    .sub-card {
        background: #f8f9ff;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 5px;
        cursor: pointer;
        border: 1px solid #e8e8e8;
        transition: all 0.2s;
    }
    .sub-card:hover {
        background: #eef2ff;
        border-color: #667eea;
    }
    
    /* 统计卡片 */
    .stat-card {
        background: #fff;
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stat-card .label {
        font-size: 11px;
        color: #888;
        margin-bottom: 5px;
    }
    .stat-card .value {
        font-size: 24px;
        font-weight: 600;
        color: #667eea;
    }
    
    /* 路径标签 */
    .path-tag {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 10px;
        margin: 2px 3px 2px 0;
    }
    
    /* 反馈项 */
    .feedback-item {
        background: #fff3cd;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 5px;
        font-size: 12px;
    }
    
    /* 热门节点 */
    .hot-item {
        padding: 5px 0;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        justify-content: space-between;
        font-size: 12px;
    }
    .hot-item .rank {
        color: #667eea;
        font-weight: bold;
        margin-right: 6px;
    }
    
    /* 图例 - 横向排列 */
    .legend-box {
        background: #fff;
        padding: 6px 14px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .legend-box h5 {
        margin: 0 !important;
        font-size: 10px;
        color: #888;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 10px;
        color: #555;
    }
    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    
    /* 提示框 */
    .tips-box {
        background: #fff;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 10px;
        color: #888;
        line-height: 1.4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-top: 5px;
    }
    
    /* 按钮紧凑 */
    .stButton > button {
        padding: 0.25rem 0.6rem !important;
        font-size: 11px !important;
    }
    
    /* 输入框紧凑 */
    .stTextInput > div > div > input {
        padding: 0.3rem 0.5rem !important;
        font-size: 12px !important;
    }
    .stTextArea > div > div > textarea {
        font-size: 11px !important;
    }
    
    /* 标题紧凑 */
    h5, h4 {
        margin-bottom: 0.3rem !important;
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# Session State 初始化
# =============================================
if 'user_id' not in st.session_state:
    st.session_state.user_id = ''
if 'clicks' not in st.session_state:
    st.session_state.clicks = []
if 'path' not in st.session_state:
    st.session_state.path = []
if 'feedbacks' not in st.session_state:
    st.session_state.feedbacks = []
if 'selected_node' not in st.session_state:
    st.session_state.selected_node = None
if 'mode' not in st.session_state:
    st.session_state.mode = 'student'
if 'teacher_verified' not in st.session_state:
    st.session_state.teacher_verified = False
if 'all_users_data' not in st.session_state:
    st.session_state.all_users_data = {}

# =============================================
# 数据存储（Neo4j + 本地 JSON 降级方案）
# =============================================
DATA_FILE = "student_data.json"

def get_neo4j_driver():
    try:
        uri = st.secrets["NEO4J_URI"]
        user = st.secrets["NEO4J_USER"]
        password = st.secrets["NEO4J_PASSWORD"]
        return GraphDatabase.driver(uri, auth=(user, password))
    except:
        return None

def save_data(user_id, data):
    """保存数据到 Neo4j 或本地 JSON"""
    # 确保有 user_id，如果是空的则标记为 anonymous
    target_id = user_id if user_id else "anonymous"
    
    # 1. 尝试保存到 Neo4j
    driver = get_neo4j_driver()
    if driver:
        try:
            with driver.session() as session:
                session.run("""
                    MERGE (u:Student {id: $uid})
                    SET u.clicks = $clicks, u.path = $path, u.feedbacks = $feedbacks, u.updated = $ts
                """, uid=target_id, 
                    clicks=json.dumps(data.get('clicks', [])), 
                    path=json.dumps(data.get('path', [])), 
                    feedbacks=json.dumps(data.get('feedbacks', [])),
                    ts=datetime.now().isoformat())
            return
        except Exception as e:
            print(f"Neo4j save failed: {e}")
    
    # 2. 降级方案：保存到本地 JSON 文件
    try:
        all_data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                except:
                    pass
        
        all_data[target_id] = {
            'clicks': data.get('clicks', []),
            'path': data.get('path', []),
            'feedbacks': data.get('feedbacks', []),
            'updated': datetime.now().isoformat()
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Local save failed: {e}")

def load_data():
    """加载所有用户数据"""
    # 1. 尝试从 Neo4j 加载
    driver = get_neo4j_driver()
    if driver:
        try:
            with driver.session() as session:
                result = session.run("MATCH (u:Student) RETURN u.id, u.clicks, u.path, u.feedbacks, u.updated")
                users = {}
                for record in result:
                    uid = record['u.id']
                    users[uid] = {
                        'clicks': json.loads(record['u.clicks'] or '[]'),
                        'path': json.loads(record['u.path'] or '[]'),
                        'feedbacks': json.loads(record['u.feedbacks'] or '[]'),
                        'updated': record['u.updated']
                    }
                return users
        except Exception as e:
            print(f"Neo4j load failed: {e}")
    
    # 2. 降级方案：从本地 JSON 加载
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# =============================================
# 辅助函数：记录点击
# =============================================
def record_click(node_name):
    """记录用户点击并更新学习路径"""
    click_record = {'node': node_name, 'ts': datetime.now().isoformat()}
    st.session_state.clicks.append(click_record)
    # 记录路径（去重）
    if not any(p['node'] == node_name for p in st.session_state.path):
        st.session_state.path.append(click_record)
    
    # 保存数据（自动处理 Neo4j 或本地文件）
    save_data(st.session_state.user_id, {
        'clicks': st.session_state.clicks,
        'path': st.session_state.path,
        'feedbacks': st.session_state.feedbacks
    })

# =============================================
# 显示节点详情（复刻 graph.html 的 showDetail）
# =============================================
def show_node_detail(name):
    """显示选中节点的详细信息"""
    data = KNOWLEDGE.get(name)
    if not data:
        st.info("请点击图谱中的节点查看详情")
        return
    
    tag_colors = {"center": "#5470c6", "section": "#91cc75", "topic": "#fac858"}
    tag_names = {"center": "课程主题", "section": "核心章节", "topic": "知识要点"}
    color = tag_colors.get(data['type'], "#667eea")
    tag_name = tag_names.get(data['type'], "知识要点")
    
    # 主卡片
    st.markdown(f"""
    <div class="detail-card" style="border-left-color: {color}">
        <h3><span class="tag" style="background: {color}">{tag_name}</span>{name}</h3>
        <div class="content-text">{data['content']}</div>
        <div style="margin-top: 12px;">
            {''.join([f'<span class="kw">{kw}</span>' for kw in data.get('keywords', [])])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 子节点（只显示直接子节点，不包括虚线关联）
    children = [l['target'] for l in LINKS if l['source'] == name and not l.get('dashed')]
    if children:
        st.markdown("**📌 相关知识点：**")
        for child in children:
            child_data = KNOWLEDGE.get(child, {})
            if child_data:
                # 找到关系标签
                relation_label = next((l['label'] for l in LINKS if l['source'] == name and l['target'] == child), "")
                with st.container():
                    col_btn, col_rel = st.columns([4, 1])
                    with col_btn:
                        if st.button(f"📎 {child}", key=f"child_{child}", use_container_width=True):
                            st.session_state.selected_node = child
                            record_click(child)
                            st.rerun()
                    with col_rel:
                        st.caption(f"[{relation_label}]")

# =============================================
# 构建 agraph 图谱
# =============================================
def build_agraph():
    """构建 streamlit-agraph 图谱节点和边"""
    nodes = []
    edges = []
    
    # 建立颜色映射，用于边染色
    node_color_map = {n["id"]: n["color"] for n in NODES_CONFIG}
    
    for n in NODES_CONFIG:
        nodes.append(Node(
            id=n["id"],
            label=n["id"],
            size=n["size"],
            color=n["color"],
            shape="circle", # 文字在圆圈内
            font={"color": "#111", "size": 14 if n["size"] > 50 else 10}, # 黑色文字
            borderWidth=2,
            borderWidthSelected=4,
            shadow={"enabled": True, "color": "rgba(0,0,0,0.2)", "size": 5, "x": 2, "y": 2}
        ))
    
    for l in LINKS:
        # 边颜色跟随源节点 (仿 ECharts color: 'source')
        source_color = node_color_map.get(l["source"], "#999")
        edge_color = source_color if not l.get("dashed") else "#bbb"
        
        edges.append(Edge(
            source=l["source"],
            target=l["target"],
            label=l["label"],
            color=edge_color,
            font={"color": source_color if not l.get("dashed") else "#888", "size": 10, "align": "middle", "background": "white", "strokeWidth": 0},
            arrows={"to": {"enabled": True, "scaleFactor": 0.5}},
            dashes=l.get("dashed", False),
            width=2 if not l.get("dashed") else 1,
            smooth={"type": "continuous", "roundness": 0} if not l.get("dashed") else {"type": "curvedCW", "roundness": 0.2}
        ))
    
    return nodes, edges

# =============================================
# 顶部导航栏
# =============================================
st.markdown("""
<div class="top-header">
    <div>
        <h1>🌟 让生命绽放光彩</h1>
        <p>第十三讲 · 心理健康知识图谱</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 模式切换按钮
col_btn1, col_btn2, col_spacer = st.columns([1, 1, 4])
with col_btn1:
    if st.button("📚 学生模式", use_container_width=True, type="primary" if st.session_state.mode == 'student' else "secondary"):
        st.session_state.mode = 'student'
        st.rerun()
with col_btn2:
    if st.button("📊 教师模式", use_container_width=True, type="primary" if st.session_state.mode == 'teacher' else "secondary"):
        st.session_state.mode = 'teacher'
        st.rerun()

st.markdown("---")

# =============================================
# 学生模式
# =============================================
if st.session_state.mode == 'student':
    col_sidebar, col_graph = st.columns([1, 2.5])
    
    with col_sidebar:
        # 用户登录（紧凑）
        st.markdown("##### 📝 学号/姓名")
        user_id = st.text_input("", placeholder="例如：2024001", label_visibility="collapsed", key="user_input")
        if user_id:
            st.session_state.user_id = user_id
            st.caption(f"✅ {user_id}")
        
        st.markdown("---")
        
        # 节点详情
        st.markdown("##### 📍 知识点详情")
        
        if st.session_state.selected_node:
            show_node_detail(st.session_state.selected_node)
        else:
            st.markdown("""
            <div style="text-align: center; color: #aaa; padding: 15px 10px;">
                <div style="font-size: 32px; margin-bottom: 6px;">🎯</div>
                <p style="font-size: 11px;">点击节点探索内容</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 学习路径
        st.markdown("##### 📍 学习路径")
        if st.session_state.path:
            path_html = ''.join([f'<span class="path-tag">{p["node"]}</span>' for p in st.session_state.path[-4:]])
            st.markdown(path_html, unsafe_allow_html=True)
        else:
            st.caption("尚无")
        
        st.markdown("---")
        
        # 反馈框（紧凑）
        st.markdown("##### 💭 分享想法")
        feedback = st.text_area("", placeholder="关于生命的思考...", label_visibility="collapsed", height=50, key="feedback_input")
        if st.button("提交", use_container_width=True):
            if feedback.strip():
                st.session_state.feedbacks.append({
                    'content': feedback.strip(),
                    'ts': datetime.now().isoformat()
                })
                # 保存数据
                save_data(st.session_state.user_id, {
                    'clicks': st.session_state.clicks,
                    'path': st.session_state.path,
                    'feedbacks': st.session_state.feedbacks
                })
                st.success("感谢分享！")
                st.rerun()
            else:
                st.warning("请先输入您的想法")
    
    with col_graph:
        # 图例（横向）
        st.markdown("""
        <div class="legend-box">
            <h5>节点类型：</h5>
            <div class="legend-item"><span class="legend-dot" style="background:#5470c6"></span>课程主题</div>
            <div class="legend-item"><span class="legend-dot" style="background:#91cc75"></span>核心章节</div>
            <div class="legend-item"><span class="legend-dot" style="background:#fac858"></span>知识要点</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ee6666"></span>关键概念</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 构建图谱
        nodes, edges = build_agraph()
        
        config = Config(
            width="100%",
            height=500,
            directed=True,
            physics={
                "solver": "forceAtlas2Based",
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.005,
                    "springLength": 200,
                    "springConstant": 0.05,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "minVelocity": 0.75,
                "stabilization": {"enabled": True, "iterations": 200}
            },
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False,
            node={'labelProperty': 'label'},
            link={'labelProperty': 'label', 'renderLabel': True}
        )
        
        # 渲染图谱并捕获点击事件
        selected_node = agraph(nodes=nodes, edges=edges, config=config)
        
        # 处理节点点击
        if selected_node:
            if selected_node != st.session_state.selected_node:
                st.session_state.selected_node = selected_node
                record_click(selected_node)
                st.rerun()
        
        # 提示（单行）
        st.markdown("""
        <div class="tips-box">
            💡 点击节点查看详情 | 拖拽移动 | 滚轮缩放 | 边上文字为关系
        </div>
        """, unsafe_allow_html=True)

# =============================================
# 教师模式
# =============================================
else:
    if not st.session_state.teacher_verified:
        # 密码验证
        st.markdown("### 🔐 教师验证")
        st.markdown("请输入教师密码以查看学情数据")
        pwd = st.text_input("", type="password", placeholder="请输入密码", label_visibility="collapsed")
        if st.button("验 证", use_container_width=False):
            if pwd == "admin888":
                st.session_state.teacher_verified = True
                # 加载数据
                st.session_state.all_users_data = load_data()
                st.rerun()
            else:
                st.error("密码错误，请重试")
    else:
        # 教师数据看板（不显示图谱，只显示数据）
        st.markdown("## 📊 教学数据看板")
        
        # 刷新按钮
        col_actions = st.columns([1, 1, 1, 3])
        with col_actions[0]:
            if st.button("🔄 刷新数据"):
                st.session_state.all_users_data = load_data()
                st.rerun()
        with col_actions[1]:
            if st.button("📥 导出数据"):
                data_str = json.dumps(st.session_state.all_users_data, ensure_ascii=False, indent=2)
                st.download_button("下载 JSON", data_str, f"学生学习数据_{datetime.now().strftime('%Y-%m-%d')}.json", "application/json")
        with col_actions[2]:
            if st.button("🚪 退出教师模式"):
                st.session_state.teacher_verified = False
                st.rerun()
        
        # 统计指标
        users_data = st.session_state.all_users_data
        total_students = len(users_data)
        total_clicks = sum(len(u.get('clicks', [])) for u in users_data.values())
        total_feedbacks = sum(len(u.get('feedbacks', [])) for u in users_data.values())
        total_path = sum(len(u.get('path', [])) for u in users_data.values())
        avg_path = round(total_path / total_students, 1) if total_students > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">👤 已记录学生数</div>
                <div class="value">{total_students}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">🖱️ 总点击次数</div>
                <div class="value">{total_clicks}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">💭 收到反馈数</div>
                <div class="value">{total_feedbacks}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">📍 平均学习节点</div>
                <div class="value">{avg_path}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 学生选择
        st.markdown("### 🎯 学生数据查看")
        user_options = ["— 选择学生 —", "📋 查看所有学生"] + list(users_data.keys())
        selected_user = st.selectbox("", user_options, label_visibility="collapsed")
        
        if selected_user == "📋 查看所有学生":
            for uid, data in users_data.items():
                with st.expander(f"👤 {uid}"):
                    st.write(f"**学习路径** ({len(data.get('path', []))} 个节点)")
                    if data.get('path'):
                        path_html = ''.join([f'<span class="path-tag">{p["node"]}</span>' for p in data['path']])
                        st.markdown(path_html, unsafe_allow_html=True)
                    
                    st.write(f"**点击记录** (最近10条)")
                    for click in data.get('clicks', [])[-10:]:
                        st.text(f"  {click['node']} - {click['ts']}")
                    
                    if data.get('feedbacks'):
                        st.write(f"**反馈内容** ({len(data['feedbacks'])} 条)")
                        for fb in data['feedbacks']:
                            st.info(f"{fb['content']}\n\n_{fb['ts']}_")
        elif selected_user and selected_user != "— 选择学生 —":
            data = users_data.get(selected_user, {})
            if data:
                st.write(f"**学习路径** ({len(data.get('path', []))} 个节点)")
                if data.get('path'):
                    path_html = ''.join([f'<span class="path-tag">{p["node"]}</span>' for p in data['path']])
                    st.markdown(path_html, unsafe_allow_html=True)
                
                st.write(f"**点击记录** (最近10条)")
                for click in data.get('clicks', [])[-10:]:
                    st.text(f"  {click['node']} - {click['ts']}")
                
                if data.get('feedbacks'):
                    st.write(f"**反馈内容** ({len(data['feedbacks'])} 条)")
                    for fb in data['feedbacks']:
                        st.info(f"{fb['content']}\n\n_{fb['ts']}_")
        
        st.markdown("---")
        
        # 热门节点和反馈汇总
        col_hot, col_fb = st.columns(2)
        
        with col_hot:
            st.markdown("### 🔥 热门节点")
            click_counts = {}
            for uid, data in users_data.items():
                for click in data.get('clicks', []):
                    node = click['node']
                    click_counts[node] = click_counts.get(node, 0) + 1
            
            sorted_nodes = sorted(click_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            if sorted_nodes:
                for i, (node, count) in enumerate(sorted_nodes, 1):
                    st.markdown(f"""
                    <div class="hot-item">
                        <span><span class="rank">{i}.</span> {node}</span>
                        <span style="color:#888;font-size:12px">{count} 次</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("暂无数据")
        
        with col_fb:
            st.markdown("### 💭 学生反馈汇总")
            all_feedbacks = []
            for uid, data in users_data.items():
                for fb in data.get('feedbacks', []):
                    all_feedbacks.append({'uid': uid, **fb})
            
            all_feedbacks.sort(key=lambda x: x['ts'], reverse=True)
            
            if all_feedbacks:
                for fb in all_feedbacks[:10]:
                    st.markdown(f"""
                    <div class="feedback-item">
                        <div>{fb['content']}</div>
                        <div style="font-size:11px;color:#888;margin-top:8px"><strong>{fb['uid']}</strong> · {fb['ts']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("暂无反馈")
