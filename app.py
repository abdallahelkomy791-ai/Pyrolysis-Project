import streamlit as st
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="Pyrolysis Simulator", layout="wide")
st.title("🔥 Pyrolysis Reactor Simulator")

# القائمة الجانبية
st.sidebar.header("Reactor Settings ⚙️")
feedstock_choice = st.sidebar.radio("Select Feedstock Type:", ("Plastic Waste", "Biomass / Wood"))
mass_input = st.sidebar.number_input("Enter Waste Mass (kg)", min_value=1.0, value=100.0)
temperature = st.sidebar.slider("Operating Temperature (°C)", 200, 800, 500)

if st.sidebar.button("Run Simulation 🚀"):
    # المنطق الهندسي
    if feedstock_choice == "Plastic Waste":
        if temperature < 450:
            oil, char, gas = 0.60, 0.30, 0.10
        elif 450 <= temperature <= 600:
            oil, char, gas = 0.80, 0.10, 0.10
        else:
            oil, char, gas = 0.40, 0.05, 0.55
    else: # Biomass
        if temperature < 400:
            oil, char, gas = 0.30, 0.50, 0.20
        else:
            oil, char, gas = 0.60, 0.20, 0.20

    # الحسابات
    m_oil = mass_input * oil
    m_char = mass_input * char
    m_gas = mass_input * gas
    co2_saved = mass_input * 1.5
    net_profit = (m_oil * 0.5 + m_char * 0.3) - (mass_input * 0.1)

    # عرض النتائج
    col1, col2, col3 = st.columns(3)
    col1.metric("Bio-Oil Yield", f"{m_oil:.1f} kg")
    col2.metric("CO2 Saved 🌱", f"{co2_saved:.1f} kg")
    col3.metric("Net Profit 💰", f"${net_profit:.2f}")
    
    # الرسم البياني
    st.divider()
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Product Yields")
        fig1, ax1 = plt.subplots()
        ax1.pie([m_oil, m_char, m_gas], labels=['Bio-Oil', 'Char', 'Syngas'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
        st.pyplot(fig1)
    
    with col_chart2:
        st.info(f"Processing **{feedstock_choice}** at **{temperature}°C**")

else:
    st.write("👈 Please start the simulation from the sidebar.")