<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>让生命绽放光彩 - 知识图谱</title>
    <script src="https://assets.pyecharts.org/assets/v5/echarts.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: "Microsoft YaHei", sans-serif; background: #f5f7fa; color: #333; }
        
        /* 顶部导航 */
        .top-header { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; padding: 16px 32px; display: flex; justify-content: space-between; align-items: center; }
        .top-header h1 { font-size: 20px; }
        .top-header p { font-size: 12px; opacity: 0.85; margin-top: 4px; }
        .mode-tabs { display: flex; gap: 8px; }
        .mode-tabs button { padding: 10px 24px; border: 2px solid rgba(255,255,255,0.3); border-radius: 8px; background: transparent; color: #fff; cursor: pointer; font-size: 13px; transition: all 0.2s; }
        .mode-tabs button:hover { background: rgba(255,255,255,0.1); }
        .mode-tabs button.active { background: #fff; color: #667eea; border-color: #fff; }
        
        /* 学生模式 - 知识图谱页面 */
        .student-view { display: flex; height: calc(100vh - 70px); }
        .student-view.hide { display: none; }
        
        .sidebar { width: 380px; background: #fff; display: flex; flex-direction: column; border-right: 1px solid #e0e0e0; box-shadow: 2px 0 8px rgba(0,0,0,0.05); }
        
        .user-box { padding: 16px 20px; background: #f8f9ff; border-bottom: 1px solid #e8e8e8; }
        .user-box label { font-size: 12px; color: #888; display: block; margin-bottom: 6px; }
        .user-box input { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; background: #fff; color: #333; font-size: 13px; }
        .user-box input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        .user-status { font-size: 11px; color: #999; margin-top: 6px; }
        
        .content-area { flex: 1; overflow-y: auto; padding: 16px; }
        .placeholder { text-align: center; color: #aaa; padding: 60px 20px; }
        .placeholder .icon { font-size: 50px; margin-bottom: 16px; }
        
        .detail-card { background: #fff; border-radius: 12px; padding: 18px; margin-bottom: 14px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .detail-card h3 { font-size: 16px; margin-bottom: 10px; color: #333; }
        .detail-card .tag { font-size: 10px; padding: 3px 10px; border-radius: 12px; background: #667eea; color: #fff; margin-right: 8px; }
        .detail-card .content { font-size: 13px; line-height: 1.9; color: #555; margin-top: 10px; }
        .detail-card .keywords { margin-top: 12px; }
        .detail-card .kw { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 14px; font-size: 11px; margin: 3px 4px 3px 0; }
        
        .sub-cards { margin-top: 12px; }
        .sub-card { background: #f8f9ff; border-radius: 8px; padding: 12px; margin-bottom: 8px; cursor: pointer; border: 1px solid #e8e8e8; transition: all 0.2s; }
        .sub-card:hover { background: #eef2ff; border-color: #667eea; }
        .sub-card h4 { font-size: 13px; color: #333; margin-bottom: 6px; }
        .sub-card p { font-size: 12px; color: #888; }
        
        .feedback-box { padding: 16px 20px; background: #fff9f0; border-top: 1px solid #e8e8e8; }
        .feedback-box h4 { font-size: 13px; color: #e67e22; margin-bottom: 10px; }
        .feedback-box textarea { width: 100%; height: 70px; padding: 10px; border: 1px solid #ddd; border-radius: 8px; background: #fff; color: #333; font-size: 12px; resize: none; }
        .feedback-box textarea:focus { outline: none; border-color: #e67e22; }
        .feedback-box button { margin-top: 8px; width: 100%; padding: 10px; background: linear-gradient(135deg, #e67e22, #d35400); border: none; border-radius: 8px; color: #fff; font-size: 12px; cursor: pointer; }
        
        .graph-area { flex: 1; position: relative; background: #fafbfc; }
        #chart { width: 100%; height: 100%; }
        
        .legend-box { position: absolute; left: 20px; top: 20px; background: #fff; padding: 14px 18px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
        .legend-box h5 { font-size: 12px; color: #888; margin-bottom: 10px; }
        .legend-item { display: flex; align-items: center; gap: 10px; margin: 6px 0; font-size: 12px; color: #555; }
        .legend-dot { width: 14px; height: 14px; border-radius: 50%; }
        
        .tips-box { position: absolute; right: 20px; top: 20px; background: #fff; padding: 12px 16px; border-radius: 10px; font-size: 11px; color: #888; line-height: 1.8; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
        
        .path-box { position: absolute; left: 20px; bottom: 20px; background: #fff; padding: 12px 16px; border-radius: 10px; max-width: 250px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
        .path-box h5 { font-size: 12px; color: #667eea; margin-bottom: 8px; }
        .path-item { font-size: 11px; color: #555; padding: 3px 0 3px 10px; border-left: 2px solid #667eea; margin: 4px 0; }
        
        /* 教师模式 - 全屏数据页面 */
        .teacher-view { display: none; min-height: calc(100vh - 70px); background: #f5f7fa; }
        .teacher-view.show { display: block; }
        
        .teacher-container { max-width: 1200px; margin: 0 auto; padding: 24px; }
        
        .pwd-section { max-width: 400px; margin: 60px auto; }
        .pwd-card { background: #fff; border-radius: 12px; padding: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center; }
        .pwd-card h3 { font-size: 18px; color: #333; margin-bottom: 8px; }
        .pwd-card p { font-size: 13px; color: #888; margin-bottom: 20px; }
        .pwd-card input { width: 100%; padding: 12px 16px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; margin-bottom: 12px; }
        .pwd-card input:focus { outline: none; border-color: #667eea; }
        .pwd-card .error { color: #e74c3c; font-size: 12px; margin-bottom: 10px; display: none; }
        .pwd-card button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea, #764ba2); border: none; border-radius: 8px; color: #fff; font-size: 14px; cursor: pointer; }
        
        .teacher-data { display: none; }
        .teacher-data.show { display: block; }
        
        .stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .stat-card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .stat-card .label { font-size: 13px; color: #888; margin-bottom: 8px; }
        .stat-card .value { font-size: 28px; font-weight: 600; color: #667eea; }
        
        .section { background: #fff; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section h2 { font-size: 16px; color: #333; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        
        .actions { margin-bottom: 16px; display: flex; gap: 8px; flex-wrap: wrap; }
        .actions button { padding: 10px 20px; border: none; border-radius: 8px; font-size: 13px; cursor: pointer; transition: all 0.2s; }
        .btn-refresh { background: #667eea; color: #fff; }
        .btn-refresh:hover { background: #5a6fd6; }
        .btn-export { background: #2ecc71; color: #fff; }
        .btn-export:hover { background: #27ae60; }
        .btn-clear { background: #e74c3c; color: #fff; }
        .btn-clear:hover { background: #c0392b; }
        
        .user-select { padding: 10px 16px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; min-width: 240px; margin-bottom: 16px; }
        
        .user-card { background: #f9f9f9; border-radius: 10px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #667eea; }
        .user-card h3 { font-size: 15px; color: #333; margin-bottom: 10px; }
        .user-card .meta { font-size: 12px; color: #888; margin-bottom: 12px; }
        
        .data-section { margin-top: 12px; }
        .data-section h4 { font-size: 13px; color: #667eea; margin-bottom: 8px; }
        
        .click-item { background: #fff; padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; display: flex; justify-content: space-between; border: 1px solid #eee; }
        .click-item .node { color: #333; }
        .click-item .time { color: #aaa; font-size: 11px; }
        
        .feedback-item { background: #fff3cd; padding: 12px; border-radius: 8px; margin-bottom: 8px; }
        .feedback-item .content { font-size: 14px; color: #333; line-height: 1.6; }
        .feedback-item .time { font-size: 11px; color: #888; margin-top: 8px; }
        
        .path-tag { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 4px 10px; border-radius: 14px; font-size: 12px; margin: 2px 4px 2px 0; }
        
        .empty { color: #aaa; font-size: 13px; text-align: center; padding: 20px; }
        
        .hot-item { padding: 8px 0; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; }
        .hot-item:last-child { border-bottom: none; }
        .hot-item .rank { color: #667eea; font-weight: bold; margin-right: 8px; }
        .hot-item .count { color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="top-header">
        <div>
            <h1>🌟 让生命绽放光彩</h1>
            <p>第十三讲 · 心理健康知识图谱</p>
        </div>
        <div class="mode-tabs">
            <button class="active" id="btnStudent" onclick="switchMode('student')">📚 学生模式</button>
            <button id="btnTeacher" onclick="switchMode('teacher')">📊 教师模式</button>
        </div>
    </div>
    
    <!-- 学生模式 - 知识图谱 -->
    <div class="student-view" id="studentView">
        <aside class="sidebar">
            <div class="user-box">
                <label>请输入学号/姓名</label>
                <input type="text" id="userId" placeholder="例如：2024001 张三" />
                <div class="user-status" id="userStatus">输入后开始记录学习轨迹</div>
            </div>
            
            <div class="content-area" id="contentArea">
                <div class="placeholder">
                    <div class="icon">🎯</div>
                    <p>点击图谱中的节点</p>
                    <p style="margin-top:8px;font-size:12px">探索知识内容</p>
                </div>
            </div>
            
            <div class="feedback-box">
                <h4>💭 关于死亡，你有什么想法？</h4>
                <textarea id="feedbackInput" placeholder="分享你的思考和感悟..."></textarea>
                <button onclick="submitFeedback()">提交我的想法</button>
            </div>
        </aside>
        
        <main class="graph-area">
            <div id="chart"></div>
            
            <div class="legend-box">
                <h5>节点类型</h5>
                <div class="legend-item"><span class="legend-dot" style="background:#5470c6"></span>课程主题</div>
                <div class="legend-item"><span class="legend-dot" style="background:#91cc75"></span>核心章节</div>
                <div class="legend-item"><span class="legend-dot" style="background:#fac858"></span>知识要点</div>
                <div class="legend-item"><span class="legend-dot" style="background:#ee6666"></span>关键概念</div>
            </div>
            
            <div class="tips-box">点击节点查看详情<br>拖拽移动节点<br>滚轮缩放图谱</div>
            
            <div class="path-box">
                <h5>📍 学习路径</h5>
                <div id="pathList"><span style="color:#aaa">尚无记录</span></div>
            </div>
        </main>
    </div>
    
    <!-- 教师模式 - 数据页面 -->
    <div class="teacher-view" id="teacherView">
        <div class="teacher-container">
            <div class="pwd-section" id="pwdSection">
                <div class="pwd-card">
                    <h3>🔐 教师验证</h3>
                    <p>请输入教师密码以查看学情数据</p>
                    <input type="password" id="teacherPwd" placeholder="请输入密码" />
                    <div class="error" id="pwdError">密码错误，请重试</div>
                    <button onclick="verifyTeacher()">验 证</button>
                </div>
            </div>
            
            <div class="teacher-data" id="teacherData">
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="label">👤 已记录学生数</div>
                        <div class="value" id="statStudents">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">🖱️ 总点击次数</div>
                        <div class="value" id="statClicks">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">💭 收到反馈数</div>
                        <div class="value" id="statFeedbacks">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">📍 平均学习节点</div>
                        <div class="value" id="statAvgPath">0</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🎯 学生数据查看</h2>
                    <div class="actions">
                        <button class="btn-refresh" onclick="loadTeacherData()">🔄 刷新数据</button>
                        <button class="btn-export" onclick="exportData()">📥 导出数据</button>
                        <button class="btn-clear" onclick="clearAllData()">🗑️ 清空所有数据</button>
                    </div>
                    <select class="user-select" id="userSelect" onchange="showUserDetail()">
                        <option value="">— 选择学生 —</option>
                        <option value="__all__">📋 查看所有学生</option>
                    </select>
                    <div id="userDetailArea">
                        <div class="empty">请选择一个学生查看其学习数据</div>
                    </div>
                </div>
                
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
                    <div class="section">
                        <h2>🔥 热门节点</h2>
                        <div id="hotNodes"><div class="empty">暂无数据</div></div>
                    </div>
                    <div class="section">
                        <h2>💭 学生反馈汇总</h2>
                        <div id="feedbackList" style="max-height:300px;overflow-y:auto"><div class="empty">暂无反馈</div></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        var currentMode = 'student';
        var teacherVerified = false;
        var allUsersData = {};
        
        // 知识数据
        var KNOWLEDGE = {
            "让生命绽放光彩": { type: "center", content: "本讲围绕「生命」这一核心主题，从认识死亡、探索意义、应对危机、积极生活四个维度展开。通过理解死亡的必然性，反思生命的有限与珍贵，学会在危机中成长，最终活出属于自己的精彩人生。", keywords: ["生命教育", "心理健康", "积极心理学"] },
            "向死而生": { type: "section", content: "海德格尔提出「向死而生」的哲学概念——只有真正认识死亡，才能深刻理解生命的意义。本章探讨死亡的本质、人们面对死亡的态度，以及死亡对于理解生命价值的启示。", keywords: ["死亡认知", "生命有限性", "存在主义"] },
            "认识死亡": { type: "topic", content: "医学上死亡经历三个阶段：濒死期（意识模糊、反应迟钝）、临床死亡期（心跳呼吸停止）、生物学死亡期（不可逆的细胞死亡）。人们对死亡的恐惧往往源于对未知的恐惧。", keywords: ["濒死期", "临床死亡", "脑死亡"] },
            "死亡态度": { type: "topic", content: "面对死亡的态度：文化层面不让提（死亡禁忌）、心理层面不敢提（恐惧回避）、认知层面不需提（否认逃避）。库伯勒-罗斯提出悲伤五阶段：震惊、否认、愤怒、抑郁、接受。", keywords: ["死亡禁忌", "悲伤阶段", "心理防御"] },
            "死亡特征": { type: "topic", content: "死亡三大特征：必然性（有生必有死）、偶然性（何时何地不可预测）、终结性（失去一切所拥有的）。正是这些特征提醒我们珍惜当下。", keywords: ["必然性", "偶然性", "终结性"] },
            "生命意义": { type: "section", content: "弗兰克尔《活出生命的意义》指出：人可以被剥夺一切，唯独不能被剥夺选择态度的自由。探索生命意义是人类永恒的追问，也是心理健康的重要基石。", keywords: ["意义疗法", "价值追求", "存在意义"] },
            "生命特征": { type: "topic", content: "生命五大特征：有限性（时间有限）、双重属性（自然性与社会性）、创造性（不断创造新内容）、超越性（能够超越自己）、珍贵性（每个生命都是奇迹）。", keywords: ["有限性", "双重属性", "创造性"] },
            "意义作用": { type: "topic", content: "生命意义的作用：体会生活意义（承担责任带来满足）、确立生活目标（设定人生方向）、增强心理韧性（提高挫折耐受力）。尼采说：知道为什么而活的人，能承受任何怎样活。", keywords: ["生活目标", "心理韧性", "责任承担"] },
            "琼瑶启示": { type: "topic", content: "2024年12月，86岁的琼瑶选择翩然离去。遗书写道：我是火花，我已尽力燃烧过...我活过了，不曾辜负此生！她的选择引发关于生命自主权和死亡尊严的深度思考。", keywords: ["生命自主", "死亡尊严", "不负此生"] },
            "转危为机": { type: "section", content: "心理危机是生活中不可避免的挑战。危机中蕴含着危险，也蕴含着机遇。学会识别危机信号、理解危机反应、掌握应对方法，可以帮助我们在逆境中成长。", keywords: ["心理危机", "危机干预", "逆境成长"] },
            "危机概念": { type: "topic", content: "心理危机三要素：危机事件发生、感知导致主观痛苦、惯常应对方式失效。心理危机不是疾病，而是情感危机反应，多数可在6-8周内自然缓解。", keywords: ["心理失衡", "应对失效", "情感反应"] },
            "危机特征": { type: "topic", content: "心理危机五大特征：突发性（难以控制）、无助性（不知所措）、危险性（影响生活甚至生命）、潜在性（长期积累后爆发）、复杂性（多因素交织）。", keywords: ["突发性", "无助感", "复杂性"] },
            "危机类型": { type: "topic", content: "心理危机三类：成长性危机（发展阶段转换）、境遇性危机（突发外部事件）、存在性危机（人生意义困惑）。不同类型需要不同的应对策略。", keywords: ["成长性", "境遇性", "存在性"] },
            "危机识别": { type: "topic", content: "危机预警信号：情绪异常（持续低落、焦虑）、行为改变（睡眠饮食紊乱）、学习下降、损毁物品、言语暗示（谈论死亡、告别）。发现信号请及时寻求帮助！", keywords: ["预警信号", "早期识别", "及时求助"] },
            "活出精彩": { type: "section", content: "认识了死亡、理解了意义、学会了应对危机，最终目标是活出精彩的人生。积极心理学告诉我们：幸福不是终点，而是一种生活方式。", keywords: ["积极生活", "幸福感", "自我实现"] },
            "活在当下": { type: "topic", content: "正念（Mindfulness）：专注于现在正在经历的事、留意身边发生的幸福小事、用心感受每一个当下。幸福往往藏在平凡时刻中。", keywords: ["正念", "当下觉知", "幸福感知"] },
            "自我价值": { type: "topic", content: "实现自我价值的路径：设定阶段性目标、培养核心能力、持之以恒努力、在实践中调整。马斯洛需求层次理论：自我实现是人类最高层次的需求。", keywords: ["目标设定", "能力培养", "自我实现"] },
            "亲密关系": { type: "topic", content: "良好人际关系是心理健康的保护因素：提供情感支持和归属感、帮助缓解压力、促进个人成长。哈佛85年研究表明：良好人际关系是预测幸福的最重要因素。", keywords: ["社会支持", "情感连接", "幸福因素"] },
            "敬畏生命": { type: "topic", content: "罗曼·罗兰：世界上只有一种真正的英雄主义，那就是认清生活真相后，依旧热爱生活。敬畏生命：尊重自己和他人的生命、在困难中保持希望。", keywords: ["热爱生活", "英雄主义", "生命尊重"] }
        };
        
        // 图谱数据
        var nodes = [
            { name: "让生命绽放光彩", symbolSize: 80, category: 0, itemStyle: { color: "#5470c6" } },
            { name: "向死而生", symbolSize: 55, category: 1, itemStyle: { color: "#91cc75" } },
            { name: "生命意义", symbolSize: 55, category: 1, itemStyle: { color: "#91cc75" } },
            { name: "转危为机", symbolSize: 55, category: 1, itemStyle: { color: "#91cc75" } },
            { name: "活出精彩", symbolSize: 55, category: 1, itemStyle: { color: "#91cc75" } },
            { name: "认识死亡", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "死亡态度", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "死亡特征", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "生命特征", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "意义作用", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "琼瑶启示", symbolSize: 40, category: 3, itemStyle: { color: "#ee6666" } },
            { name: "危机概念", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "危机特征", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "危机类型", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "危机识别", symbolSize: 40, category: 3, itemStyle: { color: "#ee6666" } },
            { name: "活在当下", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "自我价值", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "亲密关系", symbolSize: 40, category: 2, itemStyle: { color: "#fac858" } },
            { name: "敬畏生命", symbolSize: 40, category: 3, itemStyle: { color: "#ee6666" } }
        ];
        
        var links = [
            { source: "让生命绽放光彩", target: "向死而生", value: "包含" },
            { source: "让生命绽放光彩", target: "生命意义", value: "包含" },
            { source: "让生命绽放光彩", target: "转危为机", value: "包含" },
            { source: "让生命绽放光彩", target: "活出精彩", value: "包含" },
            { source: "向死而生", target: "认识死亡", value: "探讨" },
            { source: "向死而生", target: "死亡态度", value: "分析" },
            { source: "向死而生", target: "死亡特征", value: "总结" },
            { source: "生命意义", target: "生命特征", value: "认识" },
            { source: "生命意义", target: "意义作用", value: "理解" },
            { source: "生命意义", target: "琼瑶启示", value: "反思" },
            { source: "转危为机", target: "危机概念", value: "定义" },
            { source: "转危为机", target: "危机特征", value: "分析" },
            { source: "转危为机", target: "危机类型", value: "分类" },
            { source: "转危为机", target: "危机识别", value: "掌握" },
            { source: "活出精彩", target: "活在当下", value: "实践" },
            { source: "活出精彩", target: "自我价值", value: "追求" },
            { source: "活出精彩", target: "亲密关系", value: "建立" },
            { source: "活出精彩", target: "敬畏生命", value: "升华" },
            // 跨章节关联
            { source: "死亡特征", target: "生命特征", value: "对比", lineStyle: { type: "dashed", opacity: 0.5 } },
            { source: "死亡态度", target: "危机识别", value: "关联", lineStyle: { type: "dashed", opacity: 0.5 } },
            { source: "琼瑶启示", target: "敬畏生命", value: "启发", lineStyle: { type: "dashed", opacity: 0.5 } },
            { source: "意义作用", target: "自我价值", value: "驱动", lineStyle: { type: "dashed", opacity: 0.5 } },
            { source: "危机类型", target: "活在当下", value: "应对", lineStyle: { type: "dashed", opacity: 0.5 } },
            { source: "认识死亡", target: "敬畏生命", value: "升华", lineStyle: { type: "dashed", opacity: 0.5 } }
        ];
        
        var categories = [{ name: "课程主题" }, { name: "核心章节" }, { name: "知识要点" }, { name: "关键概念" }];
        
        // 初始化图谱
        var chart = echarts.init(document.getElementById("chart"));
        var option = {
            backgroundColor: "#fafbfc",
            title: { text: "让生命绽放光彩", subtext: "点击节点查看详情", left: "center", top: 10, textStyle: { color: "#333", fontSize: 18 }, subtextStyle: { color: "#888" } },
            tooltip: { trigger: "item", formatter: "{b}", backgroundColor: "#fff", borderColor: "#ddd", textStyle: { color: "#333" } },
            series: [{
                type: "graph", layout: "force", roam: true, draggable: true,
                force: { repulsion: 600, gravity: 0.1, edgeLength: [80, 180], friction: 0.6 },
                label: { show: true, position: "inside", fontSize: 11, color: "#333", fontWeight: "bold", formatter: function(p) { return p.name.length > 4 ? p.name.slice(0,4) + "\n" + p.name.slice(4) : p.name; } },
                lineStyle: { color: "source", width: 2, opacity: 0.7, curveness: 0 },
                edgeLabel: { show: true, fontSize: 10, formatter: "{c}", color: "#888" },
                edgeSymbol: ["", "arrow"], edgeSymbolSize: 8,
                data: nodes, links: links, categories: categories
            }]
        };
        chart.setOption(option);
        window.addEventListener("resize", function() { chart.resize(); });
        
        chart.on("click", function(params) {
            if (params.dataType === "node") {
                recordClick(params.name);
                showDetail(params.name);
            }
        });
        
        // 显示详情
        function showDetail(name) {
            var data = KNOWLEDGE[name];
            if (!data) return;
            var area = document.getElementById("contentArea");
            var tagColors = { center: "#5470c6", section: "#91cc75", topic: "#fac858" };
            var tagNames = { center: "课程主题", section: "核心章节", topic: "知识要点" };
            var html = "<div class=\"detail-card\" style=\"border-left-color:" + (tagColors[data.type] || "#667eea") + "\">";
            html += "<h3><span class=\"tag\" style=\"background:" + (tagColors[data.type] || "#667eea") + "\">" + (tagNames[data.type] || "知识要点") + "</span>" + name + "</h3>";
            html += "<div class=\"content\">" + data.content + "</div>";
            html += "<div class=\"keywords\">";
            for (var i = 0; i < data.keywords.length; i++) { html += "<span class=\"kw\">" + data.keywords[i] + "</span>"; }
            html += "</div></div>";
            var children = [];
            for (var i = 0; i < links.length; i++) { if (links[i].source === name && !links[i].lineStyle) children.push(links[i].target); }
            if (children.length > 0) {
                html += "<div class=\"sub-cards\">";
                for (var i = 0; i < children.length; i++) {
                    var cd = KNOWLEDGE[children[i]];
                    if (cd) {
                        html += "<div class=\"sub-card\" onclick=\"showDetail('" + children[i] + "');recordClick('" + children[i] + "')\">";
                        html += "<h4>" + children[i] + "</h4><p>" + cd.content.slice(0, 40) + "...</p></div>";
                    }
                }
                html += "</div>";
            }
            area.innerHTML = html;
        }
        
        // 用户数据
        function getUserId() { return document.getElementById("userId").value.trim() || "anonymous"; }
        function getUserKey() { return "user_" + getUserId(); }
        function getUserData() {
            var d = localStorage.getItem(getUserKey());
            return d ? JSON.parse(d) : { userId: getUserId(), clicks: [], feedbacks: [], path: [], created: new Date().toISOString() };
        }
        function saveUserData(data) {
            data.updated = new Date().toISOString();
            localStorage.setItem(getUserKey(), JSON.stringify(data));
            var users = JSON.parse(localStorage.getItem("all_users") || "[]");
            var uid = getUserId();
            if (uid !== "anonymous" && users.indexOf(uid) === -1) { users.push(uid); localStorage.setItem("all_users", JSON.stringify(users)); }
        }
        function recordClick(name) {
            var data = getUserData();
            data.clicks.push({ node: name, ts: new Date().toISOString() });
            var found = false;
            for (var i = 0; i < data.path.length; i++) { if (data.path[i].node === name) { found = true; break; } }
            if (!found) data.path.push({ node: name, ts: new Date().toISOString() });
            saveUserData(data);
            updatePath();
        }
        function updatePath() {
            var data = getUserData();
            var el = document.getElementById("pathList");
            if (data.path.length === 0) { el.innerHTML = "<span style=\"color:#aaa\">尚无记录</span>"; return; }
            var html = "";
            var arr = data.path.slice(-5).reverse();
            for (var i = 0; i < arr.length; i++) { html += "<div class=\"path-item\">" + arr[i].node + "</div>"; }
            el.innerHTML = html;
        }
        function submitFeedback() {
            var input = document.getElementById("feedbackInput");
            var content = input.value.trim();
            if (!content) { alert("请先输入您的想法"); return; }
            var data = getUserData();
            data.feedbacks.push({ content: content, ts: new Date().toISOString() });
            saveUserData(data);
            input.value = "";
            alert("感谢分享！");
        }
        
        // 模式切换
        function switchMode(mode) {
            currentMode = mode;
            document.getElementById("btnStudent").className = mode === "student" ? "active" : "";
            document.getElementById("btnTeacher").className = mode === "teacher" ? "active" : "";
            document.getElementById("studentView").className = mode === "student" ? "student-view" : "student-view hide";
            document.getElementById("teacherView").className = mode === "teacher" ? "teacher-view show" : "teacher-view";
            if (mode === "teacher" && teacherVerified) { loadTeacherData(); }
        }
        
        // 教师验证
        function verifyTeacher() {
            var pwd = document.getElementById("teacherPwd").value;
            if (pwd === "admin888") {
                teacherVerified = true;
                document.getElementById("pwdSection").style.display = "none";
                document.getElementById("teacherData").className = "teacher-data show";
                loadTeacherData();
            } else {
                document.getElementById("pwdError").style.display = "block";
            }
        }
        
        // 加载教师数据
        function loadTeacherData() {
            var users = JSON.parse(localStorage.getItem("all_users") || "[]");
            allUsersData = {};
            var totalClicks = 0, totalFeedbacks = 0, totalPath = 0, clickCounts = {};
            
            var anonData = localStorage.getItem("user_anonymous");
            if (anonData) {
                allUsersData["anonymous"] = JSON.parse(anonData);
                totalClicks += (allUsersData["anonymous"].clicks || []).length;
                totalFeedbacks += (allUsersData["anonymous"].feedbacks || []).length;
                totalPath += (allUsersData["anonymous"].path || []).length;
                var ac = allUsersData["anonymous"].clicks || [];
                for (var j = 0; j < ac.length; j++) { clickCounts[ac[j].node] = (clickCounts[ac[j].node] || 0) + 1; }
            }
            
            for (var i = 0; i < users.length; i++) {
                var d = localStorage.getItem("user_" + users[i]);
                if (d) {
                    var data = JSON.parse(d);
                    allUsersData[users[i]] = data;
                    totalClicks += (data.clicks || []).length;
                    totalFeedbacks += (data.feedbacks || []).length;
                    totalPath += (data.path || []).length;
                    var clicks = data.clicks || [];
                    for (var j = 0; j < clicks.length; j++) { clickCounts[clicks[j].node] = (clickCounts[clicks[j].node] || 0) + 1; }
                }
            }
            
            var userCount = Object.keys(allUsersData).length;
            document.getElementById("statStudents").textContent = userCount;
            document.getElementById("statClicks").textContent = totalClicks;
            document.getElementById("statFeedbacks").textContent = totalFeedbacks;
            document.getElementById("statAvgPath").textContent = userCount > 0 ? (totalPath / userCount).toFixed(1) : "0";
            
            var select = document.getElementById("userSelect");
            select.innerHTML = "<option value=\"\">— 选择学生 —</option><option value=\"__all__\">📋 查看所有学生</option>";
            for (var uid in allUsersData) {
                var opt = document.createElement("option");
                opt.value = uid;
                opt.textContent = uid === "anonymous" ? "匿名用户" : uid;
                select.appendChild(opt);
            }
            
            var sorted = [];
            for (var k in clickCounts) sorted.push([k, clickCounts[k]]);
            sorted.sort(function(a, b) { return b[1] - a[1]; });
            var top5 = sorted.slice(0, 5);
            var hotHtml = top5.length > 0 ? "" : "<div class=\"empty\">暂无数据</div>";
            for (var i = 0; i < top5.length; i++) { hotHtml += "<div class=\"hot-item\"><span><span class=\"rank\">" + (i+1) + ".</span> " + top5[i][0] + "</span><span class=\"count\">" + top5[i][1] + " 次</span></div>"; }
            document.getElementById("hotNodes").innerHTML = hotHtml;
            
            var allFeedbacks = [];
            for (var uid in allUsersData) {
                var fbs = allUsersData[uid].feedbacks || [];
                for (var j = 0; j < fbs.length; j++) { allFeedbacks.push({ content: fbs[j].content, ts: fbs[j].ts, uid: uid }); }
            }
            allFeedbacks.sort(function(a, b) { return new Date(b.ts) - new Date(a.ts); });
            var fbHtml = allFeedbacks.length === 0 ? "<div class=\"empty\">暂无反馈</div>" : "";
            for (var i = 0; i < allFeedbacks.length; i++) {
                fbHtml += "<div class=\"feedback-item\"><div class=\"content\">" + allFeedbacks[i].content + "</div><div class=\"time\"><strong>" + (allFeedbacks[i].uid === "anonymous" ? "匿名用户" : allFeedbacks[i].uid) + "</strong> · " + new Date(allFeedbacks[i].ts).toLocaleString() + "</div></div>";
            }
            document.getElementById("feedbackList").innerHTML = fbHtml;
        }
        
        function showUserDetail() {
            var uid = document.getElementById("userSelect").value;
            var area = document.getElementById("userDetailArea");
            if (!uid) { area.innerHTML = "<div class=\"empty\">请选择一个学生查看其学习数据</div>"; return; }
            if (uid === "__all__") {
                var html = "";
                for (var id in allUsersData) { html += renderUserCard(id, allUsersData[id]); }
                area.innerHTML = html || "<div class=\"empty\">暂无学生数据</div>";
                return;
            }
            var data = allUsersData[uid];
            if (!data) { area.innerHTML = "<div class=\"empty\">该学生暂无数据</div>"; return; }
            area.innerHTML = renderUserCard(uid, data);
        }
        
        function renderUserCard(uid, data) {
            var clicks = data.clicks || [];
            var feedbacks = data.feedbacks || [];
            var path = data.path || [];
            var html = "<div class=\"user-card\">";
            html += "<h3>👤 " + (uid === "anonymous" ? "匿名用户" : uid) + "</h3>";
            html += "<div class=\"meta\">首次访问：" + (data.created ? new Date(data.created).toLocaleString() : "未知") + " | 最后更新：" + (data.updated ? new Date(data.updated).toLocaleString() : "未知") + "</div>";
            html += "<div class=\"data-section\"><h4>📍 学习路径（" + path.length + " 个节点）</h4><div>";
            if (path.length > 0) { for (var i = 0; i < path.length; i++) { html += "<span class=\"path-tag\">" + path[i].node + "</span>"; } } else { html += "<span style=\"color:#aaa\">暂无</span>"; }
            html += "</div></div>";
            html += "<div class=\"data-section\"><h4>🖱️ 点击记录（最近10条）</h4>";
            if (clicks.length > 0) {
                var recentClicks = clicks.slice(-10).reverse();
                for (var i = 0; i < recentClicks.length; i++) { html += "<div class=\"click-item\"><span class=\"node\">" + recentClicks[i].node + "</span><span class=\"time\">" + new Date(recentClicks[i].ts).toLocaleString() + "</span></div>"; }
            } else { html += "<div class=\"empty\">暂无点击记录</div>"; }
            html += "</div>";
            if (feedbacks.length > 0) {
                html += "<div class=\"data-section\"><h4>💭 反馈内容（" + feedbacks.length + " 条）</h4>";
                for (var i = 0; i < feedbacks.length; i++) { html += "<div class=\"feedback-item\"><div class=\"content\">" + feedbacks[i].content + "</div><div class=\"time\">" + new Date(feedbacks[i].ts).toLocaleString() + "</div></div>"; }
                html += "</div>";
            }
            html += "</div>";
            return html;
        }
        
        function exportData() {
            var dataStr = JSON.stringify(allUsersData, null, 2);
            var blob = new Blob([dataStr], { type: "application/json" });
            var a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "学生学习数据_" + new Date().toISOString().slice(0, 10) + ".json";
            a.click();
        }
        
        function clearAllData() {
            if (!confirm("确定要清空所有学生数据吗？此操作不可恢复！")) return;
            var users = JSON.parse(localStorage.getItem("all_users") || "[]");
            for (var i = 0; i < users.length; i++) { localStorage.removeItem("user_" + users[i]); }
            localStorage.removeItem("user_anonymous");
            localStorage.removeItem("all_users");
            loadTeacherData();
            document.getElementById("userDetailArea").innerHTML = "<div class=\"empty\">请选择一个学生查看其学习数据</div>";
            alert("所有数据已清空");
        }
        
        document.getElementById("userId").addEventListener("change", function() {
            var uid = this.value.trim();
            if (uid) {
                document.getElementById("userStatus").textContent = "已登录: " + uid;
                document.getElementById("userStatus").style.color = "#2ecc71";
                updatePath();
            }
        });
        
        updatePath();
    </script>
</body>
</html>
