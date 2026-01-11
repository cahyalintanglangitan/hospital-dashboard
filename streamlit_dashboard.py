
# DASHBOARD ANALISIS WAKTU TUNGGU RUMAH SAKIT
# Diagnostic Dashboard - Identifikasi Penyebab

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Analisis Waktu Tunggu RS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-title {
        font-size: 48px;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        padding: 20px;
    }
    .question-box {
        font-size: 24px;
        color: #dc2626;
        text-align: center;
        padding: 20px;
        background: #fef2f2;
        border-radius: 10px;
        border-left: 5px solid #dc2626;
        margin: 20px 0;
    }
    .cause-card {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        color: #1f2937;
    }
    .cause-card h3 {
        color: #92400e;
        margin-top: 0;
    }
    .cause-card p, .cause-card ul {
        color: #1f2937;
    }
    .cause-card b {
        color: #92400e;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    """Load semua data hasil analisis"""
    
    dept_df = pd.DataFrame({
        'Department': ['Neurology', 'Internal Medicine', 'General Surgery',
                       'Orthopedics', 'Cardiology', 'Emergency', 'Oncology',
                       'Pediatrics', 'Obstetrics', 'Radiology'],
        'Avg_Wait': [165, 161, 161, 155, 153, 149, 149, 146, 146, 138],
        'Total_Patients': [498, 504, 506, 492, 483, 485, 528, 526, 480, 489]
    })
    
    hour_df = pd.DataFrame({
        'Hour': list(range(7, 18)),
        'Wait_Time': [151, 150, 155, 150, 152, 153, 149, 152, 153, 156, 151],
        'Volume': [157, 575, 535, 550, 545, 578, 564, 542, 562, 377, 106],
        'Staff': [4.9, 5.0, 5.1, 4.9, 4.9, 4.9, 5.0, 4.9, 5.0, 5.0, 5.3]
    })
    
    day_df = pd.DataFrame({
        'Day': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'],
        'Wait_Time': [155, 151, 153, 151, 148, 152, 154],
        'Volume': [715, 757, 691, 655, 710, 741, 722]
    })
    
    staff_df = pd.DataFrame({
        'Doctors': [2, 3, 4, 5, 6, 7],
        'Wait_Time': [146.8, 152.7, 152.2, 152.1, 153.5, 154.9],
        'Patients': [112, 731, 1488, 1806, 700, 154]
    })
    
    triage_df = pd.DataFrame({
        'Category': ['Immediate', 'Emergency', 'Urgent', 'Semi-urgent', 'Non-urgent'],
        'Wait_Time': [107, 110, 129, 149, 175],
        'Count': [93, 399, 958, 1477, 2064],
        'Percentage': [1.9, 8.0, 19.2, 29.6, 41.4]
    })
    
    appt_df = pd.DataFrame({
        'Status': ['Hadir', 'Dibatalkan', 'No-Show'],
        'Count': [86032, 18254, 6615],
        'Percentage': [77.2, 16.4, 5.9]
    })
    
    return dept_df, hour_df, day_df, staff_df, triage_df, appt_df

dept_df, hour_df, day_df, staff_df, triage_df, appt_df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=100)
    st.title("📊 Dashboard Navigation")
    
    page = st.radio(
        "Pilih Halaman:",
        ["🏠 Ringkasan Eksekutif", "🔍 Analisis Detail"]
    )
    
    st.markdown("---")
    
    st.markdown("### 📋 Info Dataset")
    st.info("""
    **Dataset 1:** Hospital Wait Time
    - 4,991 records pasien
    - 10 departemen
    - Periode: Jan-Mar 2024
    
    **Dataset 2:** Appointments
    - 110,901 records
    - Analisis efisiensi appointment
    """)
    
    st.markdown("---")
    
    st.caption("""
    **Dibuat oleh:**
    Cahya Lintang Ayu Langitan
    NIM: 23523056
    
    **Tools:**
    PySpark | Streamlit | Plotly
    """)

# ============================================================
# PAGE 1: RINGKASAN EKSEKUTIF
# ============================================================

if page == "🏠 Ringkasan Eksekutif":
    
    st.markdown('<p class="big-title">🏥 Analisis Waktu Tunggu Rumah Sakit</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="question-box">
    <b>🎯 Pertanyaan Bisnis:</b><br>
    "Apa penyebab utama tingginya waktu tunggu pasien di rumah sakit?"
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("## 📊 Kondisi Saat Ini")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏱️ Waktu Tunggu", "152 menit", 
                  delta="+32 min dari target", delta_color="inverse")
    
    with col2:
        st.metric("🎯 Target Standar", "120 menit", 
                  delta="Standar industri")
    
    with col3:
        st.metric("📊 Status Departemen", "10/10", 
                  delta="100% di atas target", delta_color="inverse")
    
    with col4:
        st.metric("🚨 Akar Masalah", "22.3%", 
                  delta="Appointment waste")
    
    st.markdown("---")
    
    # JAWABAN
    st.markdown("## 🔍 JAWABAN: 5 Penyebab Utama + 1 Root Cause")
    
    st.markdown("""
    <div class="cause-card">
    <h3>1️⃣ MASALAH SISTEMIK (Hospital-Wide)</h3>
    <p><b>Temuan:</b> SEMUA 10 departemen melebihi target 120 menit</p>
    <ul>
        <li>Rentang: 138-165 menit</li>
        <li>Gap terkecil: Radiology +18 menit</li>
        <li>Gap terbesar: Neurology +45 menit</li>
    </ul>
    <p><b>💡 Kesimpulan:</b> Masalah bukan di departemen spesifik, tapi di <b>SISTEM OPERASIONAL</b> yang mempengaruhi seluruh rumah sakit.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cause-card">
    <h3>2️⃣ POLA STAFFING TIDAK DINAMIS</h3>
    <p><b>Temuan:</b> Jumlah dokter flat (4.9-5.3) di semua jam</p>
    <ul>
        <li>Variasi staffing: 8%</li>
        <li>Variasi volume pasien: 442% (106-578 pasien/jam)</li>
        <li>Peak hours: Jam 09:00 dan 16:00</li>
    </ul>
    <p><b>💡 Kesimpulan:</b> Staffing tidak responsif terhadap demand → <b>Understaffed di jam sibuk, overstaffed di jam sepi</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cause-card">
    <h3>3️⃣ WEEKEND BACKLOG</h3>
    <p><b>Temuan:</b> Hari Senin memiliki waktu tunggu tertinggi</p>
    <ul>
        <li>Senin: 155 menit dengan 715 pasien</li>
        <li>Minggu: 722 pasien (volume tertinggi)</li>
        <li>Jumat: 148 menit dengan 710 pasien (performa terbaik)</li>
    </ul>
    <p><b>💡 Kesimpulan:</b> Pasien terakumulasi selama weekend dan datang bersamaan di Senin tanpa mekanisme khusus untuk menangani lonjakan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cause-card">
    <h3>4️⃣ ALOKASI SUMBER DAYA TIDAK EFEKTIF</h3>
    <p><b>Temuan:</b> Korelasi dokter vs waktu tunggu = +0.014 (≈ 0)</p>
    <ul>
        <li>Shift 7 dokter: 154.9 menit (TERTINGGI)</li>
        <li>Shift 2 dokter: 146.8 menit (terendah)</li>
        <li>Paradoks: Lebih banyak dokter ≠ waktu tunggu lebih rendah</li>
    </ul>
    <p><b>💡 Kesimpulan:</b> Dokter ditempatkan secara reaktif di jam yang sudah sibuk, bukan proaktif berdasarkan prediksi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cause-card">
    <h3>5️⃣ 71% PASIEN NON-URGENT MEMENUHI SISTEM</h3>
    <p><b>Temuan:</b> Mayoritas pasien tidak memerlukan sumber daya klinik utama</p>
    <ul>
        <li>Non-urgent: 41.4% (wait 175 menit)</li>
        <li>Semi-urgent: 29.6% (wait 149 menit)</li>
        <li>Total: 71% pasien untuk kasus simple</li>
    </ul>
    <p><b>💡 Kesimpulan:</b> Pasien non-urgent mengantri bersama pasien urgent, menciptakan kemacetan dan mengonsumsi sumber daya yang seharusnya untuk emergency.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ROOT CAUSE
    st.markdown("## 🚨 ROOT CAUSE: Appointment Waste 22.3%")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.error("""
        ### 📉 Penyebab Fundamental
        
        Dari 110,901 appointments:
        - **Hadir:** 86,032 (77.2%)
        - **Dibatalkan:** 18,254 (16.4%)
        - **No-Show:** 6,615 (5.9%)
        - **TOTAL WASTE:** 24,869 (22.3%)
        
        **Dampak:**
        - 12,434 jam-dokter terbuang
        - Kapasitas efektif -22.3%
        - Slot kosong tidak dapat dipulihkan
        - Pasien walk-in terakumulasi
        
        **Ini menjelaskan kenapa:**
        Menambah dokter TIDAK efektif! Masalahnya bukan kekurangan sumber daya, tapi **UTILISASI YANG RENDAH**.
        """)
    
    with col2:
        fig_waste = go.Figure(data=[go.Pie(
            labels=appt_df['Status'],
            values=appt_df['Count'],
            hole=0.5,
            marker_colors=['#10b981', '#f59e0b', '#dc2626'],
            textinfo='label+percent'
        )])
        
        total_appts = appt_df['Count'].sum()
        fig_waste.update_layout(
            title="Distribusi Status Appointment",
            annotations=[dict(text=f'{total_appts:,}<br>Total', x=0.5, y=0.5, 
                              font_size=16, showarrow=False)],
            height=400
        )
        
        st.plotly_chart(fig_waste, use_container_width=True)
    
    st.markdown("---")
    
    # Keterkaitan
    st.markdown("## 🔗 Keterkaitan Antar Penyebab")
    
    st.info("""
    Kelima penyebab **SALING TERKAIT** dalam siklus setan:
    
    **Appointment Waste 22.3%** (root cause)
    → Kapasitas efektif berkurang
    → Pasien tidak dapat appointment → menjadi walk-in
    → Walk-in + 71% non-urgent → kemacetan
    → Kemacetan di semua departemen (sistemik)
    → Management: tambah dokter di jam sibuk (reaktif)
    → Root cause tidak ditangani → tambah dokter tidak efektif (korelasi ≈ 0)
    → Weekend backlog memperparah
    → Waktu tunggu tetap tinggi
    → Pasien frustrasi → lebih sering cancel/no-show
    → Kembali ke awal (**Siklus Setan**)
    """)
    
    st.success("""
    ## ✅ Kesimpulan Diagnostic
    
    **JAWABAN PERTANYAAN BISNIS:**
    
    Penyebab utama tingginya waktu tunggu adalah **kombinasi dari 5 faktor** yang saling terkait:
    
    1. **Masalah sistemik** (100% departemen di atas target)
    2. **Staffing tidak dinamis** (8% variasi vs 442% demand)
    3. **Weekend backlog** (Senin 155 min, surge tidak di-handle)
    4. **Alokasi sumber daya tidak efektif** (korelasi ≈ 0)
    5. **71% non-urgent memenuhi sistem** (no flow separation)
    
    **ROOT CAUSE yang mendasari semua penyebab:** **Appointment Waste 22.3%**
    
    Pembaziran 24,869 appointments (12,434 jam-dokter) menciptakan siklus setan yang memperburuk semua penyebab lainnya.
    
    📊 **Lihat analisis detail di halaman "Analisis Detail"**
    """)

# ============================================================
# PAGE 2: ANALISIS DETAIL
# ============================================================

else:  # Analisis Detail
    
    st.markdown("## 🔍 Analisis Detail per Penyebab")
    
    st.info("Pilih dimensi analisis untuk melihat data dan visualisasi detail")
    
    dimension = st.selectbox(
        "Pilih dimensi analisis:",
        ["1️⃣ Masalah Sistemik (Departemen)", 
         "2️⃣ Staffing Tidak Dinamis (Per Jam)",
         "3️⃣ Weekend Backlog (Per Hari)", 
         "4️⃣ Alokasi Sumber Daya (Korelasi)",
         "5️⃣ Non-Urgent Congest (Triage)",
         "🚨 Root Cause (Appointment Waste)"]
    )
    
    # Departemen
    if "Departemen" in dimension:
        st.markdown("### 🏥 Penyebab #1: Masalah Sistemik")
        
        fig_dept = px.bar(
            dept_df.sort_values('Avg_Wait'),
            x='Avg_Wait',
            y='Department',
            orientation='h',
            color='Avg_Wait',
            color_continuous_scale='RdYlGn_r',
            text='Avg_Wait',
            title='Waktu Tunggu per Departemen',
            labels={'Avg_Wait': 'Waktu Tunggu (menit)'}
        )
        
        fig_dept.add_vline(x=120, line_dash="dash", line_color="green", 
                           annotation_text="Target: 120 min")
        fig_dept.update_traces(texttemplate='%{text:.0f} min', textposition='outside')
        fig_dept.update_layout(height=500, showlegend=False)
        
        st.plotly_chart(fig_dept, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error(f"""
            **Terburuk:**
            - {dept_df.nlargest(1, 'Avg_Wait')['Department'].values[0]}: 
              {dept_df.nlargest(1, 'Avg_Wait')['Avg_Wait'].values[0]:.0f} menit (+45 min)
            - {dept_df.nlargest(2, 'Avg_Wait').iloc[1]['Department']}: 
              {dept_df.nlargest(2, 'Avg_Wait').iloc[1]['Avg_Wait']:.0f} menit (+41 min)
            """)
        
        with col2:
            st.success(f"""
            **Terbaik (masih > target):**
            - {dept_df.nsmallest(1, 'Avg_Wait')['Department'].values[0]}: 
              {dept_df.nsmallest(1, 'Avg_Wait')['Avg_Wait'].values[0]:.0f} menit (+18 min)
            """)
        
        st.warning("""
        **💡 Kesimpulan:**
        
        SEMUA 10 departemen melebihi target → **MASALAH SISTEMIK**
        
        Penyebab bukan di skill dokter atau peralatan spesifik departemen, 
        melainkan di sistem operasional yang mempengaruhi seluruh rumah sakit.
        """)
    
    # Per Jam
    elif "Per Jam" in dimension:
        st.markdown("### ⏰ Penyebab #2: Staffing Tidak Dinamis")
        
        fig_hour = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_hour.add_trace(
            go.Scatter(x=hour_df['Hour'], y=hour_df['Wait_Time'], 
                       name="Wait Time", line=dict(color='red', width=3),
                       mode='lines+markers'),
            secondary_y=False,
        )
        
        fig_hour.add_trace(
            go.Bar(x=hour_df['Hour'], y=hour_df['Volume'], 
                   name="Volume Pasien", marker_color='lightblue', opacity=0.6),
            secondary_y=True,
        )
        
        fig_hour.add_trace(
            go.Scatter(x=hour_df['Hour'], y=hour_df['Staff'], 
                       name="Jumlah Dokter", line=dict(color='green', width=2, dash='dash'),
                       mode='lines+markers'),
            secondary_y=False,
        )
        
        fig_hour.add_hline(y=120, line_dash="dash", line_color="green", 
                           annotation_text="Target", secondary_y=False)
        
        fig_hour.update_layout(
            title="Pola Per Jam: Wait Time vs Volume vs Staffing",
            height=500
        )
        
        fig_hour.update_yaxes(title_text="Wait Time (min) / Dokter", secondary_y=False)
        fig_hour.update_yaxes(title_text="Volume Pasien", secondary_y=True)
        
        st.plotly_chart(fig_hour, use_container_width=True)
        
        st.warning("""
        **💡 Kesimpulan:**
        
        Staffing flat (4.9-5.3 dokter) tidak mengikuti fluktuasi demand (106-578 pasien).
        
        - Variasi staffing: 8%
        - Variasi volume: 442%
        - Hasil: Understaffed di jam sibuk, overstaffed di jam sepi
        """)
    
    # Per Hari
    elif "Per Hari" in dimension:
        st.markdown("### 📅 Penyebab #3: Weekend Backlog")
        
        fig_day = go.Figure()
        
        fig_day.add_trace(go.Bar(
            x=day_df['Day'], y=day_df['Wait_Time'],
            marker_color=['#dc2626' if d == 'Senin' else '#3b82f6' for d in day_df['Day']],
            text=day_df['Wait_Time'],
            texttemplate='%{text:.0f} min',
            textposition='outside',
            name='Wait Time'
        ))
        
        fig_day.add_hline(y=120, line_dash="dash", line_color="green")
        
        fig_day.update_layout(
            title="Waktu Tunggu per Hari",
            yaxis_title="Waktu Tunggu (menit)",
            height=400
        )
        
        st.plotly_chart(fig_day, use_container_width=True)
        
        fig_vol = px.bar(day_df, x='Day', y='Volume', 
                         color='Volume', color_continuous_scale='Blues',
                         text='Volume', title="Volume Pasien per Hari")
        fig_vol.update_traces(textposition='outside')
        fig_vol.update_layout(showlegend=False, height=400)
        
        st.plotly_chart(fig_vol, use_container_width=True)
        
        st.warning("""
        **💡 Kesimpulan:**
        
        **Senin:** 155 min, 715 pasien (terburuk)  
        **Jumat:** 148 min, 710 pasien (terbaik)  
        
        Dengan volume hampir sama, selisih 7 menit menunjukkan weekend backlog effect yang signifikan.
        """)
    
    # Korelasi
    elif "Korelasi" in dimension:
        st.markdown("### 👥 Penyebab #4: Alokasi Sumber Daya Tidak Efektif")
        
        fig_corr = px.scatter(
            staff_df, x='Doctors', y='Wait_Time', size='Patients',
            color='Wait_Time', color_continuous_scale='RdYlGn_r',
            title="Korelasi: Jumlah Dokter vs Waktu Tunggu",
            labels={'Doctors': 'Jumlah Dokter', 'Wait_Time': 'Waktu Tunggu (menit)'}
        )
        
        fig_corr.add_hline(y=120, line_dash="dash", line_color="green")
        fig_corr.update_layout(height=500, showlegend=False)
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Correlation Coefficient", "+0.014", 
                      help="Mendekati 0 = tidak ada korelasi")
        
        with col2:
            st.metric("Paradoks", "7 dokter = 154.9 min", 
                      delta="Tertinggi!", delta_color="inverse")
        
        st.error("""
        **Paradoks:**
        
        Shift dengan 7 dokter: 154.9 menit (TERTINGGI)  
        Shift dengan 2 dokter: 146.8 menit (terendah)
        
        **Kenapa?** Dokter banyak di shift yang sudah sibuk + kasus kompleks (reaktif), bukan berdasarkan prediksi (proaktif).
        """)
    
    # Triage
    elif "Triage" in dimension:
        st.markdown("### 🚨 Penyebab #5: Non-Urgent Congest Sistem")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_triage = px.bar(
                triage_df, x='Wait_Time', y='Category', orientation='h',
                color='Wait_Time', color_continuous_scale='RdYlGn_r',
                text='Wait_Time', title="Wait Time per Kategori Triage"
            )
            
            fig_triage.add_vline(x=120, line_dash="dash", line_color="green")
            fig_triage.update_traces(texttemplate='%{text:.0f} min', textposition='outside')
            fig_triage.update_layout(showlegend=False, height=400)
            
            st.plotly_chart(fig_triage, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                triage_df, values='Count', names='Category',
                title="Distribusi Pasien", hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.error("""
        **Masalah:**
        
        71% pasien (Non-urgent 41.4% + Semi-urgent 29.6%) seharusnya tidak perlu sumber daya klinik utama.
        
        Non-urgent wait: 175 menit (+55 min dari target)
        """)
    
    # Root Cause
    else:
        st.markdown("### 🚨 ROOT CAUSE: Appointment Waste 22.3%")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig_appt = go.Figure(data=[go.Pie(
                labels=appt_df['Status'],
                values=appt_df['Count'],
                hole=0.5,
                marker_colors=['#10b981', '#f59e0b', '#dc2626'],
                pull=[0, 0.1, 0.1]
            )])
            
            total = appt_df['Count'].sum()
            fig_appt.update_layout(
                title="Status Appointment",
                annotations=[dict(text=f'{total:,}<br>Total', x=0.5, y=0.5, 
                                  font_size=16, showarrow=False)],
                height=400
            )
            
            st.plotly_chart(fig_appt, use_container_width=True)
        
        with col2:
            productive = appt_df[appt_df['Status'] == 'Hadir']['Count'].values[0]
            waste = appt_df[appt_df['Status'] != 'Hadir']['Count'].sum()
            
            fig_compare = go.Figure(data=[
                go.Bar(x=['Produktif', 'Terbuang'], 
                       y=[productive, waste],
                       marker_color=['#10b981', '#dc2626'],
                       text=[productive, waste],
                       texttemplate='%{text:,}',
                       textposition='outside')
            ])
            
            fig_compare.update_layout(
                title="Slot Produktif vs Terbuang",
                yaxis_title="Jumlah Appointments",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_compare, use_container_width=True)
        
        st.error("""
        **Dampak:**
        
        - Total waste: 24,869 appointments (22.3%)
        - 12,434 jam-dokter terbuang
        - Kapasitas efektif -22.3%
        
        **Ini menjelaskan** mengapa menambah dokter tidak efektif!
        """)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption("""
📊 **Dashboard Analisis Waktu Tunggu Rumah Sakit** | 
Big Data Analytics Project | 
Cahya Lintang Ayu Langitan (23523056) | 
Powered by PySpark + Streamlit + Plotly
""")
