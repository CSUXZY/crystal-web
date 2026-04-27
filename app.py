import streamlit as st
import sqlite3
import pandas as pd

# 1. 页面级配置（支持设置网页图标和宽屏模式）
st.set_page_config(page_title="晶体带隙数据库", page_icon="💎", layout="wide")

# 2. 侧边栏：用于放置控制面板
with st.sidebar:
    st.header("⚙️ 调控面板")
    search_formula = st.text_input("输入化学式 (例如: ZnO):").strip()
    bg_range = st.slider("筛选带隙范围 (eV):", 0.0, 15.0, (0.0, 15.0), 0.1)
    
    st.markdown("---")
    # 添加一张侧边栏的趣味图片 (需确保图片在同一目录下，或使用URL)
    # st.image("your_funny_crystal.jpg", caption="每天看点晶体，心情好极了")
    st.image("ag.png", caption="From Physics-Informed Deep Learning to Experimental Realization: Unlocking Entropy-Stabilized Titanium Halide Solid Electrolytes")

# 3. 主界面布局
st.title("💎 无机晶体带隙极速检索")

# 添加一个可折叠的说明区
with st.expander("ℹ️ 关于本网站的说明（点击展开）"):
    st.write("本数据库包含 240,000 个无机晶体的带隙预测数据。数据仅供学术交流与研究参考。")

@st.cache_resource
def get_connection():
    return sqlite3.connect('crystals.db', check_same_thread=False)

conn = get_connection()

# 4. 执行检索与展示（逻辑与之前一致）
query = "SELECT formula as '化学式', bandgap as '带隙 (eV)' FROM crystal_data WHERE bandgap >= ? AND bandgap <= ?"
params = [bg_range[0], bg_range[1]]

if search_formula:
    query += " AND formula = ?"
    params.append(search_formula)

df_result = pd.read_sql_query(query, conn, params=params)

if df_result.empty:
    st.warning("未找到匹配的晶体数据。")
else:
    st.success(f"**共命中 {len(df_result)} 条数据**")
    st.dataframe(df_result, use_container_width=True, hide_index=True)
