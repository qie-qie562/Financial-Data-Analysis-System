import streamlit as st
import pandas as pd

# 你的财务数据
data = {
    "年份": [2023, 2024, 2025],
    "总资产": [272699660092.25, 298944579918.70, 303834844021.44],
    "总负债": [49043190797.43, 56933264798.10, 49875590112.37],
    "营业收入": [147693604994.14, 170899152276.34, 168838102514.79],
    "净利润": [77521476277.80, 89334728025.90, 85310324833.67],
    "货币资金": [69070136376.12, 59295822956.89, 51690610946.50],
    "应收账款": [60373410.41, 18974192.75, 2609048.49],
    "存货": [46435185061.53, 54343285157.47, 61427421796.18],
    "经营现金流": [66593247721.09, 92463692168.43, 61522204989.35]
}
df = pd.DataFrame(data)

# 计算财务指标
def calc(df):
    df["流动比率"] = df["货币资金"] / df["总负债"]
    df["资产负债率"] = df["总负债"] / df["总资产"]
    df["销售净利率"] = df["净利润"] / df["营业收入"]
    df["资产周转率"] = df["营业收入"] / df["总资产"]
    df["权益乘数"] = 1 / (1 - df["资产负债率"])
    df["ROE(杜邦)"] = df["销售净利率"] * df["资产周转率"] * df["权益乘数"]
    return df
df = calc(df)

# 登录页面
def login_page():
    st.title("🔐 财务数据分析系统 — 登录")
    st.write("请输入账号密码进入系统")
    user = st.text_input("账号：")
    pwd = st.text_input("密码：", type="password")
    if st.button("点击登录"):
        if user == "admin" and pwd == "123456":
            st.session_state.flag = 1
            st.rerun()
        else:
            st.error("账号密码错误")

# 主系统分页
def main_page():
    # 左侧菜单栏
    st.sidebar.title("📋 功能导航")
    select = st.sidebar.radio(
        "请选择功能页面",
        ["🏠 系统首页",
         "📑 原始财务数据",
         "📊 财务指标分析页面",
         "📈 杜邦分析独立页面",
         "📉 数据可视化图表"]
    )
    st.sidebar.divider()
    if st.sidebar.button("🚪 退出登录"):
        st.session_state.flag = 0
        st.rerun()

    # 页面1：首页
    if select == "🏠 系统首页":
        st.title("🏠 欢迎进入财务数据分析系统")
        st.divider()
        st.write("本系统基于Python+Streamlit网页开发")
        st.write("包含：财务数据查询、指标分析、杜邦分析、数据可视化")

    # 页面2：原始数据
    elif select == "📑 原始财务数据":
        st.title("📑 原始财务数据页面")
        st.dataframe(df.iloc[:,0:8].round(2), use_container_width=True)

    # 页面3：财务指标【单独一页】
    elif select == "📊 财务指标分析页面":
        st.title("📊 财务指标分析（独立页面）")
        st.write("核心短期偿债、偿债能力、盈利指标")
        show_data = df[["年份","流动比率","资产负债率","销售净利率","ROE(杜邦)"]].round(3)
        st.dataframe(show_data, use_container_width=True)

    # 页面4：杜邦【单独一页】
    elif select == "📈 杜邦分析独立页面":
        st.title("📈 杜邦综合分析（独立页面）")
        st.info("杜邦公式：ROE = 销售净利率 × 资产周转率 × 权益乘数")
        dup = df[["年份","ROE(杜邦)","销售净利率","资产周转率","权益乘数"]].round(3)
        st.dataframe(dup, use_container_width=True)

    # 页面5：图表（换成Streamlit自带图表，不用matplotlib）
    elif select == "📉 数据可视化图表":
        st.title("📉 营收净利润趋势图表页面")
        chart_df = df[["年份", "营业收入", "净利润"]].set_index("年份")
        st.line_chart(chart_df, use_container_width=True)

# 程序入口
if "flag" not in st.session_state:
    st.session_state.flag = 0

if st.session_state.flag == 0:
    login_page()
else:
    main_page()
