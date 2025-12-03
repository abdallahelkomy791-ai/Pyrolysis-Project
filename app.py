import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Pyrolysis Predictor", layout="wide", page_icon="🧠")

# تحميل الموديل الذكي
@st.cache_resource
def load_model():
    try:
        return joblib.load('pyrolysis_model.pkl')
    except:
        return None

model = load_model()

# تنسيق CSS (للأزرار والخطوط)
st.markdown("""
<style>
    .stButton>button {width: 100%; background-color: #00cec9; color: white; font-weight: bold; border-radius: 10px;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI-Powered Pyrolysis Simulator")
st.markdown("Predict product yields using **Machine Learning (Random Forest)** trained on **750+ real experiments**.")
st.divider()

# لو الموديل مش موجود، نطلع رسالة تنبيه
if model is None:
    st.error("⚠️ ملف الموديل 'pyrolysis_model.pkl' غير موجود! تأكد من تشغيل train_model.py أولاً.")
    st.stop()

# --- القائمة الجانبية (اختيار المادة) ---
# الميزة هنا: لما تختار مادة، هو بيملأ التحليل الكيميائي لوحده (Presets)
st.sidebar.header("1. Feedstock Presets")
material_type = st.sidebar.selectbox(
    "Choose Material Template",
    ("Plastic (Polyethylene)", "Biomass (Wood Sawdust)", "Biomass (Rice Husk)", "Custom Mix")
)

# قيم افتراضية (Presets) عشان المستخدم ميتعبش في الكتابة
# C, H, O, N, Ash, Vm, FC
defaults = {"C": 50.0, "H": 6.0, "N": 0.1, "O": 40.0, "Ash": 1.0, "Vm": 80.0, "FC": 15.0}

if "Plastic" in material_type:
    # البلاستيك كربون وهيدروجين عالي
    defaults = {"C": 85.0, "H": 14.0, "N": 0.1, "O": 0.5, "Ash": 0.5, "Vm": 99.0, "FC": 0.5}
elif "Wood" in material_type:
    defaults = {"C": 50.0, "H": 6.0, "N": 0.1, "O": 43.0, "Ash": 1.0, "Vm": 85.0, "FC": 14.0}
elif "Rice" in material_type:
    defaults = {"C": 38.0, "H": 5.0, "N": 0.5, "O": 36.0, "Ash": 20.0, "Vm": 65.0, "FC": 15.0}

# --- واجهة المدخلات (3 كروت) ---
col1, col2, col3 = st.columns([1, 1.5, 1.5])

with col1:
    with st.container(border=True):
        st.header("⚙️ Conditions")
        input_mass = st.number_input("Input Mass (kg)", 100.0, step=10.0)
        temp = st.slider("Temperature (°C)", 300, 900, 500)
        heating_rate = st.number_input("Heating Rate (°C/min)", value=20.0)

with col2:
    with st.container(border=True):
        st.header("🧪 Elemental Analysis")
        c1, c2 = st.columns(2)
        c = c1.number_input("Carbon (C) %", value=defaults["C"])
        h = c2.number_input("Hydrogen (H) %", value=defaults["H"])
        
        c3, c4 = st.columns(2)
        o = c3.number_input("Oxygen (O) %", value=defaults["O"])
        n = c4.number_input("Nitrogen (N) %", value=defaults["N"])

with col3:
    with st.container(border=True):
        st.header("🔥 Proximate Analysis")
        p1, p2, p3 = st.columns(3)
        ash = p1.number_input("Ash %", value=defaults["Ash"])
        vm = p2.number_input("Volatiles %", value=defaults["Vm"])
        fc = p3.number_input("Fixed C %", value=defaults["FC"])

# --- زرار التشغيل الذكي ---
st.write("")
if st.button("🔮 Predict Yields with AI"):
    
    # 1. تجهيز البيانات للموديل (لازم نفس ترتيب التدريب بالظبط)
    # ['C', 'H', 'O', 'N', 'Ash', 'Vm', 'FC', 'T', 'HR']
    input_data = pd.DataFrame([[c, h, o, n, ash, vm, fc, temp, heating_rate]], 
                              columns=['C', 'H', 'O', 'N', 'Ash', 'Vm', 'FC', 'T', 'HR'])
    
    # 2. الموديل يتوقع النتيجة
    prediction = model.predict(input_data)[0]
    
    # النواتج: [Liquid, Char, Gas]
    pred_liq = prediction[0]
    pred_char = prediction[1]
    pred_gas = prediction[2]
    
    # تصحيح النسب لتساوي 100% (Normalization)
    total = pred_liq + pred_char + pred_gas
    if total > 0:
        pred_liq = (pred_liq / total) * 100
        pred_char = (pred_char / total) * 100
        pred_gas = (pred_gas / total) * 100
    
    # تحويل لكتلة (kg)
    m_liq = (pred_liq / 100) * input_mass
    m_char = (pred_char / 100) * input_mass
    m_gas = (pred_gas / 100) * input_mass
    
    # حسابات اقتصادية
    net_profit = (m_liq * 0.5 + m_char * 0.3) - (input_mass * 0.1)

    # --- عرض النتائج ---
    st.success("Analysis Complete based on ML Model!")
    
    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Bio-Oil (Liquid)", f"{m_liq:.1f} kg", f"{pred_liq:.1f}%")
    k2.metric("Bio-Char (Solid)", f"{m_char:.1f} kg", f"{pred_char:.1f}%")
    k3.metric("Syngas (Gas)", f"{m_gas:.1f} kg", f"{pred_gas:.1f}%")
    k4.metric("Net Profit", f"${net_profit:.2f}", delta_color="normal")

    st.divider()

    # الرسومات البيانية
    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Yield Distribution")
        fig, ax = plt.subplots(facecolor='none')
        # ألوان مميزة
        colors = ['#ff7675', '#74b9ff', '#55efc4']
        ax.pie([m_liq, m_char, m_gas], labels=['Oil', 'Char', 'Gas'], 
               autopct='%1.1f%%', colors=colors, textprops={'color':"white"})
        st.pyplot(fig, use_container_width=True)
        
    with g2:
        st.subheader("Model Logic")
        st.info(f"""
        The AI Model predicts based on:
        - **Temperature:** {temp}°C
        - **Carbon Content:** {c}%
        - **Heating Rate:** {heating_rate} °C/min
        
        *Note: Higher Carbon usually favors Char, while higher Temp favors Gas/Oil.*
        """)

else:
    st.info("👈 Adjust parameters and click Predict to run the AI.")