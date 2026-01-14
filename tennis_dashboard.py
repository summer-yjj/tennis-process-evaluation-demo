import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# --- 页面基本配置 ---
st.set_page_config(page_title="网球教学"
                              "过程性评价系统", page_icon="📊", layout="wide")

# --- 侧边栏：控制面板 ---
with st.sidebar:
    st.title("🎓 博士研究设想验证 Demo")
    st.info("本系统对应研究框架中的：'过程性评价与成长档案'")

    # 模拟选择学生
    student_id = st.selectbox("选择学生档案", ["学生 A (2021001)", "学生 B (2021002)", "学生 C (2021003)"])
    semester = st.selectbox("选择学期", ["2023-2024 秋季", "2023-2024 春季"])

    st.markdown("---")
    st.write("Designed for PhD Interview")


# --- 模拟数据生成函数 (Mock Data) ---
def get_student_data(student_name):
    # 这里我们用随机数模拟一个学生的成长数据
    # 在真实系统中，这些数据来自数据库
    np.random.seed(len(student_name))  # 保证每次选同一个人数据一致

    # 雷达图数据：五维能力模型
    categories = ['正手技术', '反手技术', '发球速度', '场上移动', '战术意识']
    r_values = np.random.randint(60, 95, size=5)
    class_avg = np.random.randint(70, 85, size=5)

    # 趋势图数据：12周的变化
    weeks = [f"第{i}周" for i in range(1, 13)]
    progress = np.cumsum(np.random.randn(12) + 0.5) + 60  # 模拟波动上升
    progress = np.clip(progress, 0, 100)  # 限制在0-100分

    return categories, r_values, class_avg, weeks, progress


# 获取数据
categories, student_scores, class_avg_scores, weeks, progress_data = get_student_data(student_id)

# --- 主页面布局 ---

# 1. 标题区
st.title(f"📊 {student_id.split(' ')[0]} - 网球技能成长数字档案")
st.markdown("基于 **多模态数据融合** 的过程性评价分析面板")

# 2. 核心指标卡片 (Metric Cards)
col1, col2, col3, col4 = st.columns(4)
col1.metric("本学期综合评分", f"{int(np.mean(student_scores))}", "+2.4")
col2.metric("出勤率", "92%", "-1%")
col3.metric("正手击球稳定性", "High", "等级 A")
col4.metric("AI 预测潜力值", "88.5", "Top 10%")

st.markdown("---")

# 3. 图表区 (两列布局)
c1, c2 = st.columns([1, 1.5])  # 左窄右宽

with c1:
    st.subheader("能力维度诊断 (五维模型)")
    # 画雷达图
    fig_radar = go.Figure()

    # 学生数据
    fig_radar.add_trace(go.Scatterpolar(
        r=student_scores,
        theta=categories,
        fill='toself',
        name='该学生'
    ))

    # 班级平均数据
    fig_radar.add_trace(go.Scatterpolar(
        r=class_avg_scores,
        theta=categories,
        fill='toself',
        name='班级平均',
        line=dict(dash='dot', color='gray')
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # 模拟 AI 诊断文本
    weakness_idx = np.argmin(student_scores)
    strength_idx = np.argmax(student_scores)
    st.warning(
        f"🤖 **AI 诊断报告**: \n该生在 **{categories[strength_idx]}** 方面表现优异，但在 **{categories[weakness_idx]}** 方面低于班级平均水平，建议下阶段通过多球训练强化。")

with c2:
    st.subheader("学期技能成长轨迹 (过程性评价)")
    # 画折线图
    df_trend = pd.DataFrame({
        "周次": weeks,
        "综合能力值": progress_data
    })

    fig_line = px.line(df_trend, x="周次", y="综合能力值", markers=True,
                       line_shape="spline", title="12周技能追踪")

    # 添加一条趋势线
    fig_line.add_hline(y=np.mean(progress_data), line_dash="dash", line_color="green", annotation_text="平均水平")

    st.plotly_chart(fig_line, use_container_width=True)

    st.info("📈 **趋势分析**: 数据显示该生在第4-6周处于平台期，第8周后呈现显著上升趋势，与'专项体能介入'时间点吻合。")

# --- 底部：详细数据表 ---
with st.expander("查看原始详细数据记录"):
    st.dataframe(pd.DataFrame([student_scores], columns=categories, index=["当前得分"]))