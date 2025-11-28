import streamlit as st
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة (عشان تبقى عريضة وشيك)
st.set_page_config(page_title="Advanced Pyrolysis Simulator", layout="wide", page_icon="🔥")

# سحر CSS عشان نظبط شكل العناوين والزراير
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.title("🔥 Advanced Pyrolysis Kinetic Simulator")
st.markdown("Modeling multicomponent biomass degradation kinetics with interactive charts.")
st.divider()

# --- 2. التصميم الجديد (نظام الكروت) ---
# هنعمل 3 أعمدة (زي صاحبك) عشان نحط فيهم المدخلات
col_input1, col_input2, col_input3 = st.columns(3)

# الكارت الأول: إعدادات التشغيل
with col_input1:
    with st.container(border=True): # دي اللي بتعمل البرواز (الكارت)
        st.header("⚙️ Operating Conditions")
        feedstock_choice = st.selectbox("Waste Type", ("Plastic Waste", "Biomass / Wood"))
        mass_input = st.number_input("Initial Mass (kg)", value=100.0, step=10.0)
        heating_rate = st.number_input("Heating Rate (K/min)", value=10.0)

# الكارت الثاني: الحرارة
with col_input2:
    with st.container(border=True):
        st.header("🌡️ Temperature Profile")
        initial_temp = st.number_input("Initial Temp (°C)", value=25.0)
        final_temp = st.slider("Max Temperature (°C)", 300, 900, 500)
        
# الكارت الثالث: معلومات إضافية (عشان الشكل يكمل)
with col_input3:
    with st.container(border=True):
        st.header("⚗️ Reactor Specs")
        residence_time = st.slider("Residence Time (sec)", 1, 60, 5)
        efficiency = st.progress(85)
        st.caption("Reactor Efficiency: High")

# زرار التشغيل الكبير
st.write("") # مسافة
if st.button("🚀 Start Simulation"):
    
    # --- نفس المنطق الهندسي بتاعنا ---
    if feedstock_choice == "Plastic Waste":
        if final_temp < 450:
            oil, char, gas = 0.60, 0.30, 0.10
        elif 450 <= final_temp <= 600:
            oil, char, gas = 0.80, 0.10, 0.10
        else:
            oil, char, gas = 0.40, 0.05, 0.55
    else: # Biomass
        if final_temp < 400:
            oil, char, gas = 0.30, 0.50, 0.20
        else:
            oil, char, gas = 0.60, 0.20, 0.20

    # الحسابات
    m_oil = mass_input * oil
    m_char = mass_input * char
    m_gas = mass_input * gas
    co2_saved = mass_input * 1.5
    net_profit = (m_oil * 0.5 + m_char * 0.3) - (mass_input * 0.1)

    # --- عرض النتائج بشكل شيك ---
    st.success("Simulation Completed Successfully!")
    
    # صف النتائج (Metrics)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Bio-Oil Yield", f"{m_oil:.1f} kg", delta=f"{oil:.0%}")
    m2.metric("Bio-Char Yield", f"{m_char:.1f} kg", delta=f"{char:.0%}")
    m3.metric("Syngas Yield", f"{m_gas:.1f} kg", delta=f"{gas:.0%}")
    m4.metric("Net Profit", f"${net_profit:.2f}", delta_color="normal")

    st.divider()

    # الرسومات البيانية
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("📊 Mass Balance Analysis")
        fig1, ax1 = plt.subplots(facecolor='none') # خلفية شفافة عشان تليق مع الدارك مود
        ax1.pie([m_oil, m_char, m_gas], labels=['Oil', 'Char', 'Gas'], 
                autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], textprops={'color':"white"})
        st.pyplot(fig1, use_container_width=True)
        
    with chart_col2:
        st.subheader("💰 Economic & Environmental")
        fig2, ax2 = plt.subplots(facecolor='none')
        ax2.bar(['CO2 Saved', 'Profit ($)'], [co2_saved, net_profit], color=['#2ecc71', '#f1c40f'])
        ax2.tick_params(colors='white') # أرقام بيضاء
        # بنخلي الخلفية شفافة عشان تليق مع الدارك مود
        fig2.patch.set_alpha(0.0)
        ax2.patch.set_alpha(0.0)
        # تلوين المحاور
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white') 
        ax2.xaxis.label.set_color('white')
        ax2.yaxis.label.set_color('white')
        
        st.pyplot(fig2, use_container_width=True)

else:
    st.info("👋 Ready to run. Adjust parameters and click Start.")
