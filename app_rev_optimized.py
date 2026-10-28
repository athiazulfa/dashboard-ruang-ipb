
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import base64
import io

st.set_page_config(
    page_title="Optimalisasi Ruang Kuliah IPB University",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD DATA
# =========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_excel(filename, file_bytes=None):
    """Baca Excel dari file default atau byte hasil upload."""
    if file_bytes is not None:
        return pd.read_excel(io.BytesIO(file_bytes))
    path = DATA_DIR / filename
    if path.exists() and path.is_file():
        return pd.read_excel(path)
    return pd.DataFrame()

# Data upload disimpan di session_state: tersedia selama sesi aplikasi berjalan.
if "data_semester" not in st.session_state:
    st.session_state["data_semester"] = {}

# =========================
# DESAIN
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F5F8FC;
    color: #26364B;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17365D 0%, #102744 100%);
    border-right: 1px solid #29496F;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #DCE7F5;
    font-size: 12px;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 8px 10px;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #29496F;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #17365D;
    letter-spacing: -0.4px;
}

.eyebrow {
    color: #B28A12;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #64748B;
    font-size: 13px;
    line-height: 1.7;
}

.kpi, .panel {
    background: #FFFFFF;
    border: 1px solid #E1E8F0;
    border-radius: 14px;
    padding: 17px;
    box-shadow: 0 3px 12px rgba(23, 54, 93, 0.04);
}

.kpi {
    min-height: 120px;
}

.kpi-label {
    color: #64748B;
    font-size: 12px;
    margin-bottom: 10px;
}

.kpi-value {
    color: #17365D;
    font-size: 25px;
    font-weight: 800;
}

.kpi-note {
    color: #8290A3;
    font-size: 11px;
    margin-top: 7px;
}

.stButton > button {
    background: #F4C542;
    color: #17365D;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #E4B52E;
    color: #102744;
}

hr {
    border-color: #DCE5EF;
}
/* MENU UTAMA */


.menu-card {
    background: #FFFFFF;
    border: 1px solid #DCE5F1;
    border-top: 4px solid #F6C744;
    border-radius: 16px;
    padding: 14px 16px;
    height: 135px;
    min-height: 0;
    box-shadow: 0 4px 14px rgba(28, 58, 96, 0.06);
    transition: all 0.2s ease;
    box-sizing: border-box;
    overflow: hidden;
}

.menu-card:hover {
    border-top-color: #294F85;
    box-shadow: 0 8px 22px rgba(28, 58, 96, 0.12);
    transform: translateY(-3px);
}

.menu-icon {
    background: #FFF4CC;
    color: #294F85;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 8px;
}

.menu-title {
    color: #1B385D;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
}

.menu-desc {
    color: #687A91;
    font-size: 12px;
    line-height: 1.4;
}


.detail-chart-header {
    background: linear-gradient(110deg, #183455, #294F85);
    border-left: 7px solid #F6C744;
    border-radius: 14px;
    padding: 17px 22px;
    margin: 18px 0 12px 0;
    box-shadow: 0 5px 14px rgba(28, 58, 96, 0.10);
}

.detail-chart-title {
    color: #F6C744;
    font-size: 21px;
    font-weight: 750;
    margin: 0;
    line-height: 1.4;
}

.detail-chart-subtitle {
    color: #FFFFFF;
    font-size: 13px;
    margin-top: 5px;
}


/* Subheader untuk grafik detail */
.subchart-header {
    background: #EAF0F8;
    border-left: 5px solid #F6C744;
    border-radius: 10px;
    padding: 13px 18px;
    margin: 18px 0 14px 0;
}

.subchart-title {
    color: #1B385D;
    font-size: 19px;
    font-weight: 700;
    margin: 0;
    line-height: 1.4;
}

.subchart-subtitle {
    color: #687A91;
    font-size: 13px;
    margin-top: 5px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #183455, #102944);
}

.sidebar-brand {
    text-align: center;
    padding: 20px 8px 26px;
    margin-bottom: 22px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

.sidebar-logo {
    width: 62px;
    height: 62px;
    margin: 0 auto 14px;
    border-radius: 14px;
    background: #FFFFFF;
    color: #183455;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 1px;
}

.sidebar-title {
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 750;
    line-height: 1.4;
}

.sidebar-subtitle {
    color: #F6C744;
    font-size: 10px;
    letter-spacing: 1px;
    margin-top: 8px;
}

.sidebar-menu-label {
    color: #B8C9DF;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin: 0 0 12px 8px;
}


/* Semua tombol menu */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    text-align: left;

    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;

    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
}

/* Teks di dalam tombol rata kiri */
[data-testid="stSidebar"] .stButton > button p {
    width: 100%;
    text-align: left;
    margin: 0;
}

/* Menu tidak aktif */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06);
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.04);
}

/* Efek saat diarahkan ke menu */
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.13);
    color: #F6C744;
    border-color: rgba(255,255,255,0.15);
}

/* Menu aktif */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #F6C744;
    color: #183455;
    border: 1px solid #F6C744;
    box-shadow: 0 4px 12px rgba(246,199,68,0.20);
}

/* Jarak antar menu */
[data-testid="stSidebar"] .stButton {
    margin-bottom: 6px;
}


/* Paksa isi tombol sidebar rata kiri */
[data-testid="stSidebar"] div.stButton > button {
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    text-align: left !important;
    padding-left: 18px !important;
}

/* Paksa teks label ikut rata kiri */
[data-testid="stSidebar"] div.stButton > button div,
[data-testid="stSidebar"] div.stButton > button p,
[data-testid="stSidebar"] div.stButton > button span {
    text-align: left !important;
}

/* Lebarkan area teks tombol */
[data-testid="stSidebar"] div.stButton > button p {
    flex: 1 !important;
    width: 100% !important;
    margin: 0 !important;
}

/* Menu sidebar: rata kiri */
[data-testid="stSidebar"] .stButton {
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    display: grid !important;
    grid-template-columns: 1fr !important;
    justify-content: start !important;
    text-align: left !important;
    padding: 12px 16px !important;
}

[data-testid="stSidebar"] .stButton > button > div {
    width: 100% !important;
    display: flex !important;
    justify-content: flex-start !important;
    text-align: left !important;
}

[data-testid="stSidebar"] .stButton > button p {
    width: 100% !important;
    text-align: left !important;
    margin: 0 !important;
}


/* Kartu identitas IPB */
.sidebar-brand {
    text-align: center;
    padding: 24px 14px 22px;
    margin: 12px 0 24px;
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, 0.10),
        rgba(255, 255, 255, 0.035)
    );
    border: 1px solid rgba(246, 199, 68, 0.38);
    border-top: 3px solid #F6C744;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
    box-sizing: border-box;
}

/* Logo IPB */
.sidebar-logo {
    width: 92px;
    height: 92px;
    object-fit: contain;
    display: block;
    margin: 0 auto 18px;
    padding: 5px;
    background: #FFFFFF;
    border: 2px solid rgba(246, 199, 68, 0.85);
    border-radius: 20px;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.15);
}

/* Nama sistem */
.sidebar-brand-title {
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 800;
    line-height: 1.4;
    letter-spacing: 0.2px;
    margin-top: 4px;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.12);
}

/* IPB UNIVERSITY - warna emas */
.sidebar-brand-subtitle {
    display: inline-block;
    color: #F6C744;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 12px;
    padding: 7px 14px;
    border: 1px solid rgba(246, 199, 68, 0.45);
    border-radius: 20px;
    background: rgba(246, 199, 68, 0.09);
}

/* Deskripsi analisis */
.sidebar-brand-description {
    color: #E0EAF5;
    font-size: 11px;
    line-height: 1.7;
    margin-top: 16px;
    padding: 0 2px;
}

.sidebar-brand-description strong {
    display: block;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
    margin-top: 5px;
}

/* Garis pemisah */
.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.16);
    margin: 20px 0 26px;
}


/* Footer identitas direktorat */
.sidebar-footer {
    margin-top: 35px;
    padding: 20px 10px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    text-align: center;
    color: #C5D4E5;
    font-size: 11px;
    line-height: 1.7;
}

.sidebar-footer .footer-directorate {
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 700;
    line-height: 1.6;
}

.footer-program {
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.5;
    margin-top: 4px;
    letter-spacing: 0.3px;
}
.sidebar-footer .footer-university {
    color: #C5D4E5;
    font-size: 10px;
    letter-spacing: 1.5px;
    margin-top: 8px;
}

/* Header grafik detail berdampingan */
.side-chart-header {
    background: #EAF0F8;
    border-left: 5px solid #F6C744;
    border-radius: 12px;
    padding: 15px 17px;
    min-height: 88px;
    margin: 8px 0 14px 0;
    box-sizing: border-box;
}

.side-chart-title {
    color: #19395F;
    font-size: 18px;
    font-weight: 750;
    line-height: 1.4;
    margin: 0 0 5px 0;
}

.side-chart-subtitle {
    color: #718096;
    font-size: 12px;
    line-height: 1.5;
    margin: 0;
}

/* =================================
   SIDEBAR RINGKAS TANPA SCROLL
   ================================= */

/* Kurangi ruang di seluruh sidebar */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}

/* Kartu identitas */
.sidebar-brand {
    padding: 12px 10px 14px !important;
    margin: 0 0 12px !important;
}

/* Logo IPB lebih kecil */
.sidebar-logo {
    width: 66px !important;
    height: 66px !important;
    margin: 0 auto 8px !important;
    padding: 3px !important;
    border-radius: 14px !important;
}

/* Judul sistem */
.sidebar-brand-title {
    font-size: 17px !important;
    line-height: 1.3 !important;
    margin-top: 2px !important;
}

/* Deskripsi sistem */
.sidebar-brand-description {
    font-size: 10px !important;
    line-height: 1.4 !important;
    margin-top: 7px !important;
}

/* Periode semester */
.sidebar-brand-description strong {
    display: block;
    margin-top: 4px;
    font-size: 10px;
}

/* IPB University */
.sidebar-brand-subtitle {
    font-size: 10px !important;
    margin-top: 7px !important;
    padding: 4px 9px !important;
}

/* Garis pemisah */
.sidebar-divider {
    margin: 10px 0 12px !important;
}

/* Label menu navigasi */
.sidebar-section-title {
    margin: 0 0 8px 4px !important;
    font-size: 10px !important;
}

/* Tombol menu lebih pendek dan rata kiri */
section[data-testid="stSidebar"] div.stButton > button {
    min-height: 0 !important;
    height: 42px !important;
    padding: 8px 12px !important;
    margin-bottom: 4px !important;
    border-radius: 10px !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

/* Teks tombol rata kiri */
section[data-testid="stSidebar"] div.stButton > button p {
    text-align: left !important;
    font-size: 13px !important;
    margin: 0 !important;
}

/* Footer sidebar */
.sidebar-footer {
    padding: 10px 4px 4px !important;
    margin-top: 10px !important;
    line-height: 1.4 !important;
}

.footer-directorate,
.footer-program {
    font-size: 10px !important;
    line-height: 1.4 !important;
}

.footer-university {
    font-size: 9px !important;
    margin-top: 5px !important;
}



</style>
""", unsafe_allow_html=True)


# =========================
# CUSTOM STYLE NAVY & GOLD
# =========================
st.markdown("""
<style>
    .chart-header {
        background: linear-gradient(120deg, #142D4E 0%, #244B7A 100%);
        padding: 28px 32px;
        border-radius: 16px;
        margin: 10px 0 24px 0;
        border-left: 7px solid #F6C445;
        box-shadow: 0 5px 16px rgba(20, 45, 78, 0.12);
    }

    .chart-title {
        color: #F6C445;
        font-size: 28px;
        font-weight: 750;
        margin: 0 0 8px 0;
        line-height: 1.35;
    }

    .chart-subtitle {
        color: #E5EDF7;
        font-size: 15px;
        margin: 0;
        line-height: 1.6;
    }

    .section-label {
        color: #142D4E;
        font-size: 18px;
        font-weight: 700;
        margin: 12px 0;
    }
    
/* Rapikan ruang kosong di atas halaman */
header[data-testid="stHeader"] {
    background: transparent;
    height: 2rem;
}

div[data-testid="stAppViewBlockContainer"] {
    padding-top: 1rem;
}

/* Warna dasar halaman */
.stApp {
    background-color: #F4F7FC;
}

/* Sidebar navy */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #19395F 0%,
        #102B49 100%
    );
}

/* Tombol kuning dengan teks navy */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s ease;
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR & NAVIGASI

pages = [
    "Beranda",
    "Analisis Kondisi",
    "Data dan Validasi",
    "Optimasi Alokasi",
    "Hasil Rekomendasi"
]
def pindah_menu(nama_menu):
    st.session_state["menu_navigasi"] = nama_menu

if "menu_navigasi" not in st.session_state:
    st.session_state["menu_navigasi"] = "Beranda"

with st.sidebar:
    st.markdown("""
    <style>
    /* Identitas sidebar */
    .sidebar-brand {
        text-align: center;
        padding: 12px 4px 22px;
    }

    .sidebar-logo {
        width: 54px !important;
        height: 54px !important;
        display: block !important;
        object-fit: contain;
        margin: 0 auto 5px !important;
    }
    .sidebar-brand {
    text-align: center !important;
    }
    .sidebar-brand img.sidebar-logo {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
    }

    .sidebar-brand-title {
        color: #FFFFFF;
        font-size: 17px;
        font-weight: 800;
        line-height: 1.4;
    }

    .sidebar-brand-subtitle {
        color: #F6C744;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 8px;
    }

    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.18);
        margin: 6px 0 22px;
    }

    .sidebar-section-title {
        color: #B8CBE2;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0 0 12px 4px;
    }
    

    /* Tombol navigasi */
    section[data-testid="stSidebar"]
    div.stButton > button {
        background: rgba(255,255,255,0.045);
        color: #FFFFFF;
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 10px;
        min-height: 46px;
        padding: 8px 12px;
        text-align: left;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"]
    div.stButton > button:hover {
        background: rgba(255,255,255,0.12);
        border-color: #F6C744;
        color: #FFFFFF;
    }

    /* Logo dan identitas tidak terpengaruh tombol */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #19395F 0%, #102B49 100%
        );
    }

    </style>
    """, unsafe_allow_html=True)
    
    
    # Baca logo IPB
    
    
# Logo dan identitas sidebar
    LOGO_PATH = Path(__file__).parent / "Logo_IPB.png"

    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=92)

    st.markdown("""
<div class="sidebar-brand-title">
    Optimalisasi<br>Ruang Kuliah
</div>

<div class="sidebar-brand-description">
    Analisis Kapasitas dan Kebutuhan Ruang 
    <strong>Semester Genap dan Ganjil 2025/2026</strong>
</div>

<hr class="sidebar-divider">

<div class="sidebar-section-title">
    MENU NAVIGASI
</div>
""", unsafe_allow_html=True)
    menu_items = [
        ("Beranda", "⌂"),
        ("Analisis Kondisi", "▥"),
        ("Data dan Validasi", "▤"),
        ("Optimasi Alokasi", "⚙"),
        ("Hasil Rekomendasi", "☑"),
    ]

    for nama, ikon in menu_items:
        aktif = st.session_state["menu_navigasi"] == nama

        if aktif:
            st.markdown("""
            <style>
            section[data-testid="stSidebar"]
            div.stButton > button[kind="primary"] {
                background: #F6C744 !important;
                color: #19395F !important;
                border: 1px solid #F6C744 !important;
                font-weight: 800 !important;
            }
            </style>
            """, unsafe_allow_html=True)

        st.button(
            f"{ikon}     {nama}",
            key=f"nav_{nama}",
            on_click=pindah_menu,
            args=(nama,),
            use_container_width=True,
            type="primary" if aktif else "secondary"
        )

menu = st.session_state["menu_navigasi"]



# =========================
# HEADER
# =========================
col_title, col_semester = st.columns([3, 1])

with col_title:
    st.title("Optimalisasi Ruang Kuliah IPB")
    st.markdown(
        '<div class="subtitle">Pemantauan penggunaan ruang, '
        'kebutuhan perkuliahan, dan rekomendasi alokasi ruang.</div>',
        unsafe_allow_html=True
    )

with col_semester:
    semester = st.selectbox(
        "Semester aktif",
        ["Genap 2025/2026", "Ganjil 2026/2027"],
        key="semester_aktif"
    )

# Muat sumber data sesuai semester yang sedang dipilih.
# Genap memakai file bawaan sebagai data awal; semester lain perlu diunggah.
_data_semester = st.session_state["data_semester"].get(semester, {})
if semester == "Genap 2025/2026":
    _jadwal_default = load_excel("data genap.xlsx")
    _rekap_default = load_excel("rekap genap.xlsx")
else:
    _jadwal_default = pd.DataFrame()
    _rekap_default = pd.DataFrame()

df_jadwal = _data_semester.get("jadwal", _jadwal_default).copy()
df_rekap = _data_semester.get("rekap", _rekap_default).copy()

df_jadwal.columns = df_jadwal.columns.astype(str).str.strip()
df_rekap.columns = df_rekap.columns.astype(str).str.strip()
if not df_rekap.empty:
    df_rekap = df_rekap.rename(columns={"Unnamed: 0": "Fakultas"})
    if "Fakultas" not in df_rekap.columns and len(df_rekap.columns) > 0:
        df_rekap = df_rekap.rename(columns={df_rekap.columns[0]: "Fakultas"})

st.write("")

# HALAMAN BERANDA
if menu == "Beranda":
    if not df_rekap.empty:
        df = df_rekap.copy()
        df.columns = df.columns.astype(str).str.strip()
        df = df.rename(columns={df.columns[0]: "Fakultas"})

        for col in [
            "Kebutuhan", "Ruangan Tersedia", "Dipakai", "Meminjam"
        ]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        total_kebutuhan = df["Kebutuhan"].sum()
        total_kapasitas = df["Ruangan Tersedia"].sum()
        total_dipakai = df["Dipakai"].sum()
        total_meminjam = df["Meminjam"].sum()
    else:
        total_kebutuhan = total_kapasitas = 0
        total_dipakai = total_meminjam = 0

    
    # Header ringkasan
    st.markdown("""
    <div style="
        background:#17365D;
        border-bottom:4px solid #F4C542;
        border-radius:12px 12px 0 0;
        padding:16px 20px;
        margin-top:18px;
    ">
        <div style="
            color:white;
            font-size:20px;
            font-weight:700;
            margin-top:5px;
        ">Pemanfaatan Ruang Kuliah yang Lebih Optimal</div>
        <div style="
            color:#DCE7F5;
            font-size:12px;
            margin-top:5px;
        ">Ringkasan kebutuhan dan pemanfaatan ruang kuliah seluruh fakultas.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 KPI BERANDA
    st.markdown("""
    <style>
    
    
    .kpi-card {
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #FAFCFF 100%
    );
    border: 1.5px solid #C8D8EA;
    border-left: 4px solid #294F91;
    border-radius: 16px;
    padding: 18px 22px;
    min-height: 155px;
    box-shadow:
        0 4px 12px rgba(25, 57, 95, 0.06),
        inset 0 0 0 1px rgba(255, 255, 255, 0.8);
    box-sizing: border-box;
    transition: all 0.2s ease;
    }

    .kpi-card:hover {
    border-color: #F6C744;
    border-left-color: #F6C744;
    box-shadow: 0 7px 18px rgba(25, 57, 95, 0.12);
    transform: translateY(-2px);
    }

    .kpi-top {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 10px;
    min-height: 42px;
    }

    .kpi-icon {
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: 600;
    flex-shrink: 0;
    }

    .kpi-label {
    color: #294F78;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.2px;
    line-height: 1.4;
    }

    .kpi-value {
    color: #19395F;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 6px;
    letter-spacing: -0.4px;
    font-variant-numeric: tabular-nums;
    }

    .kpi-note {
    color: #71839B;
    font-size: 13px;
    line-height: 1.4;
    }

    </style>
    """, unsafe_allow_html=True)
    total_surplus = total_kapasitas - total_kebutuhan


    k1, k2, k3 = st.columns(3, gap="large")

    cards = [
        (
            k1,
            "TOTAL KEBUTUHAN SESI",
            total_kebutuhan,
            "Jumlah sesi yang dibutuhkan seluruh fakultas",
            "▦",
            "#E6EEFF"
        ),
        (
            k2,
            "TOTAL KAPASITAS SESI",
            total_kapasitas,
            "Total kapasitas sesi yang tersedia",
            "▤",
            "#FFF3D4"
        ),
        (
            k3,
            "SURPLUS KAPASITAS",
            total_surplus,
            (
                "Kapasitas melebihi kebutuhan"
                if total_surplus >= 0
                else "Kebutuhan melebihi kapasitas"
            ),
            ("+" if total_surplus >= 0 else "−"),
            "#DDF7EE" if total_surplus >= 0 else "#FFE8EC"
        ),
    ]

    for col, label, value, note, icon, icon_bg in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-icon"
                         style="background:{icon_bg}; color:#19395F;">
                        {icon}
                    </div>
                    <div class="kpi-label">{label}</div>
                </div>
                <div class="kpi-value">{value:,.0f}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")



# =========================
# TOP 5 SURPLUS DAN DEFISIT
# =========================

    # Styling kartu
    st.markdown("""
    <style>
    
    
    .top5-card {
    background: transparent;
    border: none;
    border-radius: 12px;
    padding: 0;
    overflow: hidden;
    min-height: unset;
    box-shadow: none;
    }

    .top5-header {
    background: #17365D;
    margin: 0 0 12px 0;
    padding: 12px 16px;
    border-bottom: 3px solid #F4C542;
    border-radius: 12px;
    }

    .top5-heading {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 700;
    margin: 0;
    }

    .top5-icon {
    background: #F4C542;
    color: #17365D;
    width: 30px;
    height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 16px;
    flex-shrink: 0;
    }

    .top5-caption {
    color: #DCE7F5;
    font-size: 11px;
    line-height: 1.4;
    margin-top: 5px;
    margin-left: 39px;
    }

    .top5-row {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 10px;
    }

    .top5-rank {
    width: 29px;
    min-width: 29px;
    text-align: center;
    padding: 7px 0;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    }

    .top5-name {
    flex: 1;
    font-size: 13px;
    font-weight: 700;
    color: #17365D;
    }

    .top5-value {
    font-size: 13px;
    font-weight: 800;
    white-space: nowrap;
    }

    .top5-unit {
    font-size: 10px;
    color: #64748B;
    }

    .top5-track {
    flex: 1;
    min-width: 0;
    height: 28px;
    border-radius: 7px;
    overflow: hidden;
    margin: 0;
    background: #EDF1F6;
    }

    .top5-bar {
    height: 100%;
    border-radius: 7px;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    }

    </style>
    """, unsafe_allow_html=True)

    # Pastikan kolom numerik
    df_rekap["Selisih Ketersediaan"] = pd.to_numeric(
        df_rekap["Selisih Ketersediaan"], errors="coerce"
    ).fillna(0)
    

    st.markdown("""
    <div style="
        font-size:23px;
        font-weight:750;
        color:#17365D;
        border-left:5px solid #F4C542;
        padding-left:14px;
        line-height:1.35;
    ">
        Analisis Kebutuhan dan Ketersediaan Ruang per Fakultas
    </div>
    <div style="
        font-size:13px;
        color:#64748B;
        margin:8px 0 16px 19px;
    ">
        Perbandingan kebutuhan sesi kuliah dengan surplus atau defisit
        ketersediaan ruang pada setiap fakultas.
    </div>
    </div>
    """, unsafe_allow_html=True)


    if not df_rekap.empty:
    # Pastikan data numerik
        df_rekap["Kebutuhan"] = pd.to_numeric(
        df_rekap["Kebutuhan"], errors="coerce"
    ).fillna(0)

    df_rekap["Selisih Ketersediaan"] = pd.to_numeric(
        df_rekap["Selisih Ketersediaan"], errors="coerce"
    ).fillna(0)

    # Pisahkan selisih positif dan negatif
    df["Surplus"] = df_rekap["Selisih Ketersediaan"].clip(lower=0)
    df["Defisit"] = df_rekap["Selisih Ketersediaan"].clip(upper=0)

    fig = go.Figure()

    # Batang kebutuhan
    fig.add_trace(go.Bar(
        x=df["Fakultas"],
        y=df["Kebutuhan"],
        name="Kebutuhan",
        marker_color="#294F85",
        text=df["Kebutuhan"],
        textposition="inside",
        texttemplate="%{text:.0f}",
        insidetextfont=dict(color="white", size=10)
    ))

    # Selisih ketersediaan positif
    fig.add_trace(go.Bar(
        x=df["Fakultas"],
        y=df["Surplus"],
        name="Surplus Ketersediaan",
        marker_color="#F4C542",
        text=df["Surplus"].apply(
            lambda x: f"{x:.0f}" if x > 0 else ""
        ),
        textposition="inside",
        insidetextfont=dict(color="#17365D", size=10)
    ))


    # Selisih ketersediaan negatif
    fig.add_trace(go.Bar(
        x=df["Fakultas"],
        y=df["Defisit"],
        name="Defisit Ketersediaan",
        marker_color="#E95D70",
        text=df["Defisit"].apply(
            lambda x: f"{x:.0f}" if x < 0 else ""
        ),
        textposition="outside",
        textfont=dict(color="#B9384D", size=10)
    ))

    # Garis titik-titik kapasitas tersedia untuk setiap fakultas
    fig.add_trace(go.Scatter(
    x=df["Fakultas"],
    y=df["Ruangan Tersedia"],
    mode="markers+text",
    name="Kapasitas Tersedia",
    marker=dict(
        symbol="line-ew",
        size=18,
        color="#17212F",
        line=dict(width=3, color="#17212F")
    ),
    text=df["Ruangan Tersedia"].apply(
        lambda x: f"{x:,.0f}"
    ),
    textposition="top center",
    textfont=dict(
        size=11,
        color="#17212F"
    ),
     cliponaxis=False,
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Kapasitas tersedia: %{y:,.0f} sesi"
        "<extra></extra>"
    )
    ))

    fig.update_layout(
        barmode="relative",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=430,
        margin=dict(t=50, b=40, l=20, r=20),
        legend=dict(
            orientation="h",
            y=1.12,
            x=0
        ),
        xaxis_title="Fakultas",
        yaxis_title="Jumlah sesi",
        yaxis=dict(
            zeroline=True,
            zerolinecolor="#8793A5"
        )
    )

    st.plotly_chart(fig, width="stretch")

    # Dua kolom untuk surplus dan defisit
    col_surplus, col_defisit = st.columns(2, gap="large")
    
        # =========================
        # TOP 5 SURPLUS
        # =========================
    with col_surplus:
            top_surplus = (
                df_rekap.loc[
                    df_rekap["Selisih Ketersediaan"] > 0,
                    ["Fakultas", "Selisih Ketersediaan"]
                ]
                .nlargest(5, "Selisih Ketersediaan")
            )
    
            st.markdown("""
            <div class="top5-card">
                <div class="top5-header">
                    <div class="top5-heading">
                        <span class="top5-icon">↑</span>
                        <span>Top 5 Surplus Ruang</span>
                    </div>
                    <div class="top5-caption">
                        Fakultas dengan potensi ketersediaan sesi tertinggi
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
            max_s = (
                top_surplus["Selisih Ketersediaan"].max()
                if not top_surplus.empty else 1
            )
    
            for i, (_, row) in enumerate(top_surplus.iterrows(), start=1):
                nilai = row["Selisih Ketersediaan"]
                persen = nilai / max_s * 100
    
                
                st.markdown(f"""
                <div class="top5-row">
                    <div class="top5-rank"
                         style="background:#FFF4CC;color:#8A6800">
                        {i:02d}
                    </div>
                    <div class="top5-track" style="background:#EDF1F6">
                        <div class="top5-bar"
                             style="width:{persen}%;background:#F4C542;color:#17365D;">
                            <span style="padding-left:10px;">{row['Fakultas']}</span>
                        </div>
                    </div>
                    <div class="top5-value" style="color:#294F85">
                        +{nilai:,.0f}
                    </div>
                    <div class="top5-unit">sesi</div>
                </div>
                """, unsafe_allow_html=True)

    
            st.markdown("</div>", unsafe_allow_html=True)
    
        # =========================
        # TOP 5 DEFISIT
        # =========================
    with col_defisit:
            top_defisit = (
                df_rekap.loc[
                    df_rekap["Selisih Ketersediaan"] < 0,
                    ["Fakultas", "Selisih Ketersediaan"]
                ]
                .nsmallest(5, "Selisih Ketersediaan")
            )
    
            st.markdown("""
            <div class="top5-card">
                <div class="top5-header"
                     style="border-bottom-color:#E95D70">
                    <div class="top5-heading">
                        <span class="top5-icon"
                              style="background:#FCECEF;color:#C43D52">↓</span>
                        <span>Top 5 Defisit Ruang</span>
                    </div>
                    <div class="top5-caption">
                        Fakultas yang diprioritaskan mendapat tambahan ruang
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
            max_d = (
                abs(top_defisit["Selisih Ketersediaan"].min())
                if not top_defisit.empty else 1
            )
    
            for i, (_, row) in enumerate(top_defisit.iterrows(), start=1):
                nilai = row["Selisih Ketersediaan"]
                persen = abs(nilai) / max_d * 100
    
                
                st.markdown(f"""
                <div class="top5-row">
                    <div class="top5-rank"
                         style="background:#FCECEF;color:#C43D52">
                        {i:02d}
                    </div>
                    <div class="top5-track" style="background:#F4EDF0">
                        <div class="top5-bar"
                             style="width:{persen}%;background:#E95D70;color:#FFFFFF;">
                            <span style="padding-left:10px;">{row['Fakultas']}</span>
                        </div>
                    </div>
                    <div class="top5-value" style="color:#C43D52">
                        {nilai:,.0f}
                    </div>
                    <div class="top5-unit">sesi</div>
                </div>
                """, unsafe_allow_html=True)

    
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")

# MENU UTAMA

    st.markdown("""
    <style>
    

    
    .menu-main-header {
        background: linear-gradient(115deg, #19395F, #244B78);
        border-bottom: 4px solid #F6C744;
        border-radius: 12px;
        padding: 12px 22px;
        margin: 8px 0 18px;
        box-shadow: 0 5px 16px rgba(25, 57, 95, 0.08);
    }

    .menu-main-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 6px;
    }

    .menu-main-subtitle {
        color: #DCE7F5;
        font-size: 14px;
        line-height: 1.5;
    }

    .menu-main-description {
        color: #FFFFFF;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.18);
    }

    .menu-card {
    background: #FFFFFF;
    border: 1px solid #DCE5F1;
    border-top: 4px solid #F6C744;
    border-radius: 14px;
    padding: 16px 14px;
    min-height: 185px;
    height: 185px;
    box-shadow: 0 4px 14px rgba(25, 57, 95, 0.06);
    margin-bottom: 8px;
    box-sizing: border-box;
    }

    .menu-icon {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    margin-bottom: 12px;
    }

    .icon-blue {
    background: #E6EEFF;
    }

    .icon-yellow {
    background: #FFF3D4;
    }

    .menu-title {
    color: #19395F;
    font-size: 15px;
    font-weight: 750;
    line-height: 1.4;
    margin-bottom: 8px;
    }

    .menu-desc {
    color: #718096;
    font-size: 12px;
    line-height: 1.5;
    }

    </style>
    """, unsafe_allow_html=True)

    
    st.markdown("""
    <div class="menu-main-header">
        <div class="menu-main-title">
            Menu Utama
        </div>
        <div class="menu-main-description">
            Pilih modul untuk menganalisis kondisi ruang,
            memvalidasi data, menjalankan optimasi,
            atau melihat rekomendasi alokasi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    features = [
    {
        "icon": "📊",
        "title": "Analisis Kondisi",
        "desc": "Evaluasi penggunaan ruang berdasarkan fakultas, hari, dan sesi.",
        "color": "blue",
        "key": "Analisis Kondisi"
    },
    {
        "icon": "📁",
        "title": "Data dan Validasi",
        "desc": "Kelola jadwal kuliah dan periksa kelengkapan data.",
        "color": "yellow",
        "key": "Data dan Validasi"
    },
    {
        "icon": "⚙️",
        "title": "Optimasi Alokasi",
        "desc": "Simulasikan alokasi ruang berdasarkan kapasitas dan jadwal.",
        "color": "blue",
        "key": "Optimasi Alokasi"
    },
    {
        "icon": "📋",
        "title": "Hasil Rekomendasi",
        "desc": "Tinjau hasil optimasi dan ekspor rekomendasi ke Excel.",
        "color": "yellow",
        "key": "Hasil Rekomendasi"
    }
    ]

    
# =========================
# FUNGSI PINDAH MENU
# =========================
    def pindah_menu(nama_menu):
        st.session_state["menu_navigasi"] = nama_menu

    
    # Tampilkan 4 menu sejajar dalam 1 baris
    cols = st.columns(4, gap="medium")

    for col, item in zip(cols, features):
        with col:
            icon_class = (
                "icon-blue" if item["color"] == "blue"
                else "icon-yellow"
            )

            st.markdown(f"""
                <div class="menu-card">
                    <div class="menu-icon {icon_class}">
                        {item["icon"]}
                    </div>
                    <div class="menu-title">
                        {item["title"]}
                    </div>
                    <div class="menu-desc">
                        {item["desc"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.button(
                f"Buka {item['title']} →",
                key=f"buka_{item['key']}",
                on_click=pindah_menu,
                args=(item["key"],),
                use_container_width=True
            )
            


   

# HALAMAN ANALISIS KONDISI
elif menu == "Analisis Kondisi":
    if df_jadwal.empty or df_rekap.empty:
        st.warning("Data jadwal dan rekap untuk semester aktif belum lengkap. Buka Data dan Validasi untuk mengunggah keduanya.")
    else:
        st.markdown("""
    <style>
    .analysis-page-header {
        background: linear-gradient(115deg, #19395F, #244B78);
        border-bottom: 4px solid #F6C744;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 8px 0 22px;
        box-shadow: 0 4px 12px rgba(25, 57, 95, 0.08);
    }

    .analysis-page-title {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 800;
        line-height: 1.3;
        margin: 0 0 7px;
    }

    .analysis-page-subtitle {
        color: #DCE7F5;
        font-size: 13px;
        line-height: 1.5;
        margin: 0;
    }
    </style>

    <div class="analysis-page-header">
        <div class="analysis-page-title">
            Analisis Kondisi Ruang Kuliah
        </div>
        <div class="analysis-page-subtitle">
            Evaluasi kebutuhan, penggunaan, dan peminjaman ruang kuliah antar fakultas.
        </div>
    </div>
    """, unsafe_allow_html=True)


        # -------------------------
        # SIAPKAN DATA REKAP
        # -------------------------
        df_rekap_kondisi = df_rekap.copy()
        df_rekap_kondisi.columns = (
            df_rekap_kondisi.columns.astype(str).str.strip()
        )

        # Pastikan kolom fakultas tersedia
        if "Fakultas" not in df_rekap_kondisi.columns:
            df_rekap_kondisi = df_rekap_kondisi.rename(
                columns={"Unnamed: 0": "Fakultas"}
            )

        # Urutan fakultas yang diinginkan
        urutan_fakultas = [
            "FAPERTA", "SKHB", "FPIK", "FAPET", "FAHUTAN",
            "FTT", "FMIPA", "FEM", "FISEMA", "SB",
            "FKGiz", "Satari", "SSMI", "PPKU"
        ]

        fakultas_tersedia = (
            df_rekap_kondisi["Fakultas"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        daftar_fakultas = [
            f for f in urutan_fakultas
            if f in fakultas_tersedia
        ]

    
    # ==============================
    # KPI ANALISIS KONDISI
    # ==============================

    # Hitung KPI berdasarkan data rekap semester aktif
        total_kebutuhan = df_rekap["Kebutuhan"].sum()
        total_dipakai = df_rekap["Dipakai"].sum()
        total_meminjam = df_rekap["Meminjam"].sum()
        total_dipinjamkan = df_rekap["Dipinjamkan"].sum()

    # Format angka Indonesia
        def format_kpi(nilai):
            return f"{nilai:,.0f}"


    # CSS desain KPI
        st.markdown("""
    <style>
    .kpi-custom {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FBFF 100%);
        border: 1px solid #C9D8EF;
        border-left: 5px solid #2B5597;
        border-radius: 18px;
        padding: 16px 22px;
        min-height: 0;
        box-shadow: 0 4px 12px rgba(25, 57, 95, 0.04);
        box-sizing: border-box;
        margin-bottom: 12px;
    }

    .kpi-custom-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
    }

    .kpi-custom-icon {
        width: 46px;
        height: 46px;
        min-width: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 700;
        color: #19395F;
    }

    .kpi-icon-blue {
        background: #E5EDFF;
    }

    .kpi-icon-yellow {
        background: #FFF2D2;
    }

    .kpi-icon-green {
        background: #DDF5ED;
    }

    .kpi-custom-label {
        color: #244A7D;
        font-size: 15px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.35px;
        line-height: 1.4;
    }

    .kpi-custom-value {
        color: #19395F;
        font-size: 29px;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 7px;
    }

    .kpi-custom-desc {
        color: #7086A6;
        font-size: 12px;
        line-height: 1.4;
    }

    .kpi-activity-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 22px;
    }

    .kpi-activity-divider {
        border-left: 1px solid #DCE5F2;
        padding-left: 22px;
    }

    @media (max-width: 600px) {
        .kpi-custom {
            padding: 18px;
        }
        .kpi-custom-label {
            font-size: 12px;
        }
        .kpi-activity-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .kpi-activity-divider {
            border-left: none;
            border-top: 1px solid #DCE5F2;
            padding-left: 0;
            padding-top: 16px;
        }
    }


    .kpi-activity-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FBFF 100%);
        border: 1px solid #C9D8EF;
        border-left: 5px solid #2B5597;
        border-radius: 18px;
        padding: 12px 22px;
        box-shadow: 0 4px 12px rgba(25, 57, 95, 0.04);
        box-sizing: border-box;
        margin-bottom: 10px;
    }

    /* Header aktivitas */
    .kpi-activity-card .kpi-custom-header {
        margin-bottom: 6px;
    }

    /* Ikon aktivitas */
    .kpi-activity-card .kpi-custom-icon {
        width: 42px;
        height: 42px;
        min-width: 42px;
        border-radius: 13px;
        font-size: 20px;
    }

    /* Jarak antara header dan angka */
    .kpi-activity-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 8px;
    }

    /* Pembatas dua indikator */
    .kpi-activity-item + .kpi-activity-item {
        border-left: 1px solid #DCE5F2;
        padding-left: 20px;
    }

    /* Angka di kartu aktivitas */
    .kpi-activity-card .kpi-custom-value {
        font-size: 27px;
        line-height: 1.1;
        margin: 6px 0;
    }

    /* Keterangan */
    .kpi-activity-card .kpi-custom-desc {
        font-size: 12px;
        line-height: 1.3;
    }

    .kpi-activity-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 14px;
    }

    .kpi-activity-item + .kpi-activity-item {
        border-left: 1px solid #DCE5F2;
        padding-left: 20px;
    }

    .kpi-activity-card .kpi-custom-desc {
        color: #7086A6;
        font-size: 13px;
        line-height: 1.5;
    }

    .kpi-activity-card .kpi-custom-value {
        color: #19395F;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.2;
        margin: 10px 0;
    }
    </style>
        """, unsafe_allow_html=True)



    # BARIS 1: TOTAL KEBUTUHAN DAN TOTAL DIPAKAI
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(f"""
        <div class="kpi-custom">
            <div class="kpi-custom-header">
                <div class="kpi-custom-icon kpi-icon-blue">▦</div>
                <div class="kpi-custom-label">Total Kebutuhan Sesi</div>
            </div>
            <div class="kpi-custom-value">
                {format_kpi(total_kebutuhan)}
            </div>
            <div class="kpi-custom-desc">
                Jumlah sesi yang dibutuhkan seluruh fakultas
            </div>
        </div>
        """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
        <div class="kpi-custom">
            <div class="kpi-custom-header">
                <div class="kpi-custom-icon kpi-icon-green">✓</div>
                <div class="kpi-custom-label">Total Sesi Dipakai</div>
            </div>
            <div class="kpi-custom-value">
                {format_kpi(total_dipakai)}
            </div>
            <div class="kpi-custom-desc">
                Jumlah sesi menggunakan ruang milik fakultas sendiri
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BARIS 2: AKTIVITAS PEMINJAMAN DALAM SATU KOTAK
    
        # BARIS 2: AKTIVITAS PEMINJAMAN RUANG
    
       
        # BARIS 2: AKTIVITAS PEMINJAMAN SELEBAR HALAMAN

    
        # BARIS 2: AKTIVITAS PEMINJAMAN SELEBAR HALAMAN

        html_aktivitas = f"""
        <div class="kpi-activity-card">
            <div class="kpi-custom-header">
                <div class="kpi-custom-icon kpi-icon-yellow">⇄</div>
                <div class="kpi-custom-label">
                    AKTIVITAS PEMINJAMAN RUANG
                </div>
            </div>
            <div class="kpi-activity-content">
                <div class="kpi-activity-item">
                    <div class="kpi-custom-desc">Total Sesi Meminjam</div>
                    <div class="kpi-custom-value">{format_kpi(total_meminjam)}</div>
                    <div class="kpi-custom-desc">
                        Menggunakan ruang fakultas lain
                    </div>
                </div>
                <div class="kpi-activity-item">
                    <div class="kpi-custom-desc">Total Sesi Dipinjamkan</div>
                    <div class="kpi-custom-value">{format_kpi(total_dipinjamkan)}</div>
                    <div class="kpi-custom-desc">
                        Ruang digunakan fakultas lain
                    </div>
                </div>
            </div>
        </div>
        """

        st.markdown(html_aktivitas, unsafe_allow_html=True)

        # GRAFIK 1 & 2: BERSEBELAHAN

        col1, col2 = st.columns(2, gap="medium")

        # GRAFIK 1: PENGGUNAAN RUANG
        with col1:
            st.markdown("""
            <div class="chart-header">
                <div class="chart-title" style="font-size: 21px;">
                    1. Penggunaan Ruang Kuliah
                </div>
                <div class="chart-subtitle">
                    Perbandingan sesi ruang sendiri dan sesi meminjam.
                </div>
            </div>
            """, unsafe_allow_html=True)

            kolom_penggunaan = ["Dipakai", "Meminjam"]

            df_penggunaan = df_rekap_kondisi[
                ["Fakultas"] + kolom_penggunaan
            ].copy()

            df_penggunaan[kolom_penggunaan] = (
                df_penggunaan[kolom_penggunaan]
                .apply(pd.to_numeric, errors="coerce")
                .fillna(0)
            )

            df_penggunaan_long = df_penggunaan.melt(
                id_vars="Fakultas",
                value_vars=kolom_penggunaan,
                var_name="Kategori",
                value_name="Jumlah Sesi"
            )

            fig1 = px.bar(
                df_penggunaan_long,
                x="Fakultas",
                y="Jumlah Sesi",
                color="Kategori",
                barmode="stack",
                text="Jumlah Sesi",
                color_discrete_map={
                    "Dipakai": "#294F91",
                    "Meminjam": "#F6C744"
                }
            )

            fig1.update_traces(
                textposition="inside",
                textfont_size=10,
                cliponaxis=False
            )

            fig1.update_layout(
                template="plotly_white",
                height=480,
                autosize=True,
                xaxis_title="Fakultas",
                yaxis_title="Jumlah Sesi",
                 legend_title_text="",
                legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
                ),
            margin=dict(t=65, b=45, l=35, r=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#142D4E", size=10)
            )

            fig1.update_xaxes(
                tickangle=0,
                showgrid=False,
                tickfont=dict(size=10),
                automargin=True
    )
            fig1.update_yaxes(gridcolor="#E3EAF3", rangemode="tozero")

            st.plotly_chart(
                fig1,
                use_container_width=True,
                config={"responsive": True}
            )

        # GRAFIK 2: KEBUTUHAN & DIPINJAMKAN
        with col2:
            st.markdown("""
            <div class="chart-header">
                <div class="chart-title" style="font-size: 21px;">
                    2. Kebutuhan dan Ruang Dipinjamkan
                </div>
                <div class="chart-subtitle">
                    Perbandingan kebutuhan sesi dan sesi yang dipinjamkan.
                </div>
            </div>
            """, unsafe_allow_html=True)

            kolom_kebutuhan = ["Kebutuhan", "Dipinjamkan"]

            df_kebutuhan = df_rekap_kondisi[
                ["Fakultas"] + kolom_kebutuhan
            ].copy()

            df_kebutuhan[kolom_kebutuhan] = (
                df_kebutuhan[kolom_kebutuhan]
                .apply(pd.to_numeric, errors="coerce")
                .fillna(0)
            )

            df_kebutuhan_long = df_kebutuhan.melt(
                id_vars="Fakultas",
                value_vars=kolom_kebutuhan,
                var_name="Kategori",
                value_name="Jumlah Sesi"
            )

            fig2 = px.bar(
                df_kebutuhan_long,
                x="Fakultas",
                y="Jumlah Sesi",
                color="Kategori",
                barmode="stack",
                text="Jumlah Sesi",
                color_discrete_map={
                    "Kebutuhan": "#294F91",
                    "Dipinjamkan": "#F6C744"
                }
            )

            fig2.update_traces(
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(size=10),
                cliponaxis=False
            )

            fig2.update_layout(
                template="plotly_white",
                height=480,
                autosize=True,
                xaxis_title="Fakultas",
                yaxis_title="Jumlah Sesi",
                legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=65, b=45, l=35, r=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#142D4E", size=10)
            )

            fig2.update_xaxes(
                tickangle=0,
                showgrid=False,
                tickfont=dict(size=10),
                automargin=True
    )
            fig2.update_yaxes(gridcolor="#E3EAF3", rangemode="tozero")

            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={"responsive": True}
            )

        st.divider()

        # BAGIAN GRAFIK DETAIL
        def load_data_detail():
            # Gunakan data jadwal semester aktif agar grafik mengikuti upload terbaru.
            return df_jadwal.copy()

        df_detail = load_data_detail().copy()

        # Rapikan nama kolom
        df_detail.columns = (
            df_detail.columns.astype(str).str.strip()
        )

        # Filter fakultas akan digunakan di bagian ini
    
        # Filter fakultas untuk grafik detail
        col_info, col_filter = st.columns([2, 1])

        with col_info:
            st.caption(
                "Pilih fakultas untuk melihat grafik detail kebutuhan, "
                "penggunaan, dan peminjaman ruang."
            )

        with col_filter:
            fakultas_pilihan = st.selectbox(
                "Pilih Fakultas untuk Grafik Detail",
                daftar_fakultas,
                index=None,
                placeholder="Pilih fakultas...",
                key="filter_fakultas_kondisi"
            )

    
        st.markdown("""
        <div class="chart-header">
            <div class="chart-title">
                3. Analisis Detail Fakultas
            </div>
            <div class="chart-subtitle">
                Analisis kebutuhan, penggunaan, dan peminjaman ruang
                berdasarkan hari dan sesi perkuliahan.
            </div>
        </div>
        """, unsafe_allow_html=True)


    
        if fakultas_pilihan == "Semua Fakultas":
            df_fakultas = df_detail.copy()
        else:
            df_fakultas = df_detail[
                df_detail["Fakultas Asal MK"]
                .astype(str).str.strip()
                == fakultas_pilihan
            ].copy()

    
        # Siapkan kolom hari dan sesi untuk grafik detail
    
        urutan_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

        df_detail["Hari"] = (
            df_detail["Hari"].astype(str).str.strip()
        )

        df_detail["Kategori Sesi"] = pd.to_numeric(
            df_detail["Kategori Sesi"], errors="coerce"
        )

        df_detail = df_detail[
            df_detail["Hari"].isin(urutan_hari)
            & df_detail["Kategori Sesi"].isin([1, 2, 3, 4])
        ].copy()

        df_detail["Sesi"] = (
            "Sesi " + df_detail["Kategori Sesi"].astype(int).astype(str)
        )

        df_detail["Hari-Sesi"] = (
            df_detail["Hari"] + " - " + df_detail["Sesi"]
        )


        df_detail["Sesi"] = (
            "Sesi "
            + df_detail["Kategori Sesi"].astype(int).astype(str)
        )

        df_detail["Hari-Sesi"] = (
            df_detail["Hari"] + " - " + df_detail["Sesi"]
        )

        # Perbarui data fakultas setelah kolom Hari-Sesi dibuat
        if fakultas_pilihan == "Semua Fakultas":
            df_fakultas = df_detail.copy()
        else:
            df_fakultas = df_detail[
                df_detail["Fakultas Asal MK"]
                .astype(str).str.strip()
                == fakultas_pilihan
            ].copy()



        # kode grafik g1, g2, g3 ...

            # Data jadwal detail berdasarkan fakultas terpilih
            # Akan digunakan untuk membuat tiga grafik detail.
        
    # ==========================================
    # 3. ANALISIS DETAIL FAKULTAS DARI DATA MENTAH
    # ==========================================

        def load_data_detail():
            # Gunakan data jadwal semester aktif agar grafik mengikuti upload terbaru.
            return df_jadwal.copy()

        df_detail = load_data_detail().copy()

    # Bersihkan nama kolom dan data kategori
        df_detail.columns = df_detail.columns.astype(str).str.strip()

        for col in [
        "Fakultas Asal MK",
        "Fakultas Pemilik Ruang",
        "Hari",
        "Status"
    ]:
            df_detail[col] = df_detail[col].astype(str).str.strip()

        df_detail["Kategori Sesi"] = pd.to_numeric(
            df_detail["Kategori Sesi"], errors="coerce"
    )

        df_detail = df_detail[
            df_detail["Hari"].isin(
            ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        )
        & df_detail["Kategori Sesi"].isin([1, 2, 3, 4])
        ].copy()

    # Urutan hari dan sesi
        urutan_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        urutan_sesi = [1, 2, 3, 4]

    # Label sumbu grafik
        df_detail["Sesi"] = (
        "Sesi " + df_detail["Kategori Sesi"].astype(int).astype(str)
        )

        urutan_x = [
        f"{hari} - Sesi {sesi}"
        for hari in urutan_hari
        for sesi in urutan_sesi
        ]

        df_detail["Hari-Sesi"] = (
            df_detail["Hari"] + " - " + df_detail["Sesi"]
    )

    # Filter fakultas
        if fakultas_pilihan == "Semua Fakultas":
            st.info("Pilih satu fakultas untuk menampilkan grafik detail.")
        else:
            fakultas = fakultas_pilihan

            df_fakultas = df_detail[
            df_detail["Fakultas Asal MK"] == fakultas
        ].copy()

        # --------------------------------------
        # GRAFIK 1: KEBUTUHAN SESI PER HARI
        # --------------------------------------
        if fakultas_pilihan == "Semua Fakultas":
            st.info("Pilih satu fakultas untuk menampilkan grafik detail.")

        else:
            df_fakultas = df_detail[
                df_detail["Fakultas Asal MK"] == fakultas_pilihan
            ].copy()

    
        st.markdown("""
        <div class="subchart-header">
            <div class="subchart-title">
                Kebutuhan Sesi Kuliah per Hari dan Sesi
            </div>
            <div class="subchart-subtitle">
                Sebaran kebutuhan ruang kuliah dari Senin sampai Jumat
                pada setiap sesi perkuliahan.
            </div>
        </div>
        """, unsafe_allow_html=True)




        g1 = df_fakultas[
            df_fakultas["Status"].isin(
                ["Ruang Sendiri", "Ruang Fakultas Lain"]
            )
        ].copy()

        g1["Kategori"] = g1["Status"].map({
            "Ruang Sendiri": "Ruangan Sendiri",
            "Ruang Fakultas Lain": "Meminjam Ruang Fakultas Lain"
        })

        plot1 = (
            g1.groupby(["Hari-Sesi", "Kategori"])
            .size()
            .reset_index(name="Jumlah")
        )

        fig1_detail = px.bar(
            plot1,
            x="Hari-Sesi",
            y="Jumlah",
            color="Kategori",
            barmode="stack",
            text="Jumlah",
            category_orders={
                "Hari-Sesi": urutan_x,
                "Kategori": [
                    "Ruangan Sendiri",
                    "Meminjam Ruang Fakultas Lain"
                ]
            },
            color_discrete_map={
                "Ruangan Sendiri": "#294F91",
                "Meminjam Ruang Fakultas Lain": "#FF9F2E"
            }
        )

    
    
        # Atur urutan hari dan sesi
        urutan_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        urutan_sesi = [1, 2, 3, 4]

        label_x = [
            f"{hari} - Sesi {sesi}"
            for hari in urutan_hari
            for sesi in urutan_sesi
        ]

        # Pengaturan tampilan grafik
        fig1_detail.update_layout(
            template="plotly_white",
            height=490,
            xaxis_title="Hari dan Sesi",
            xaxis_title_standoff=15,
            yaxis_title="Jumlah Sesi Kuliah",
            legend_title="Kategori",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=65, b=145, l=55, r=25),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="#29415F"
            ),
            bargap=0.18
        )

        # Label sesi mendatar, tanpa nama hari pada setiap label
        fig1_detail.update_xaxes(
            tickangle=0,
            tickmode="array",
            tickvals=label_x,
            ticktext=[
                f"Sesi {sesi}"
                for hari in urutan_hari
                for sesi in urutan_sesi
            ],
            tickfont=dict(size=11, color="#294F85"),
            showgrid=False,
            automargin=True
        )

        # Tampilan sumbu Y
        fig1_detail.update_yaxes(
            rangemode="tozero",
            gridcolor="#E4EAF2",
            zeroline=False
        )

        # Label angka di dalam batang
        fig1_detail.update_traces(
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11),
            cliponaxis=False
        )

    
        # Nama hari tepat di tengah kelompok 4 sesi
        for i, hari in enumerate(urutan_hari):
            fig1_detail.add_annotation(
                x=(i * 4) + 1.5,
                y=-0.12,
                xref="x",
                yref="paper",
                text=f"<b>{hari}</b>",
                showarrow=False,
                font=dict(
                    size=12,
                    color="#19395F",
                    family="Arial, sans-serif"
                ),
                xanchor="center",
                yanchor="top"
            )
        fig1_detail.update_layout(
            xaxis_title=dict(
            text="Hari dan Sesi",
            standoff=35
        )
        )
        st.plotly_chart(fig1_detail, use_container_width=True)




   
        # --------------------------------------
        # GRAFIK 2 & 3: PENGGUNAAN DAN PEMINJAMAN
        # --------------------------------------

        col_grafik2, col_grafik3 = st.columns(2, gap="medium")

        urutan_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

        urutan_x = [
            f"{hari} - Sesi {sesi}"
            for hari in urutan_hari
            for sesi in range(1, 5)
        ]

        label_sesi = [
            f"Sesi {sesi}"
            for hari in urutan_hari
            for sesi in range(1, 5)
        ]

        # ======================================
        # GRAFIK 2: PENGGUNAAN RUANG FAKULTAS
        # ======================================
        with col_grafik2:
        
            st.markdown("""
        <div class="side-chart-header">
        <div class="side-chart-title">
            Penggunaan Ruang Fakultas dan Ruang Dipinjamkan
        </div>
        <div class="side-chart-subtitle">
            Perbandingan sesi yang digunakan sendiri dan sesi yang dipinjamkan.
        </div>
        </div>
        """, unsafe_allow_html=True)


            g2 = df_detail[
                (df_detail["Fakultas Pemilik Ruang"] == fakultas)
                & df_detail["Status"].isin(
                    ["Ruang Sendiri", "Ruang Fakultas Lain"]
                )
            ].copy()

            g2["Kategori"] = g2["Fakultas Asal MK"].apply(
                lambda x: "Dipakai" if x == fakultas else "Dipinjamkan"
            )

            plot2 = (
                g2.groupby(["Hari-Sesi", "Kategori"])
                .size()
                .reset_index(name="Jumlah")
            )

            indeks2 = pd.MultiIndex.from_product(
                [urutan_x, ["Dipakai", "Dipinjamkan"]],
                names=["Hari-Sesi", "Kategori"]
            )

            plot2 = (
                plot2.set_index(["Hari-Sesi", "Kategori"])
                .reindex(indeks2, fill_value=0)
                .reset_index()
            )

            fig2_detail = px.bar(
                plot2,
                x="Hari-Sesi",
                y="Jumlah",
                color="Kategori",
                barmode="stack",
                text=plot2["Jumlah"].where(plot2["Jumlah"] > 0, ""),
                category_orders={
                    "Hari-Sesi": urutan_x,
                    "Kategori": ["Dipakai", "Dipinjamkan"]
                },
                color_discrete_map={
                    "Dipakai": "#294F91",
                    "Dipinjamkan": "#FFA12B"
                }
            )

            fig2_detail.update_traces(
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(size=10),
                cliponaxis=False
            )

            fig2_detail.update_layout(
                template="plotly_white",
                height=460,
                xaxis_title=dict(text="Hari dan Sesi", standoff=65),
                yaxis_title="Jumlah Sesi Penggunaan",
                legend=dict(
                    title_text="Kategori",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=65, b=150, l=45, r=15),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Arial, sans-serif",
                    size=10,
                    color="#29415F"
                ),
                bargap=0.18
            )

            fig2_detail.update_xaxes(
                tickangle=0,
                tickmode="array",
                tickvals=urutan_x,
                ticktext=label_sesi,
                tickfont=dict(size=9, color="#294F85"),
                showgrid=False,
                automargin=True
            )

            fig2_detail.update_yaxes(
                rangemode="tozero",
                gridcolor="rgba(41,79,145,0.12)",
                zeroline=False
            )

            # Nama hari di bawah kelompok sesi
            for i, hari in enumerate(urutan_hari):
                fig2_detail.add_annotation(
                    x=i * 4 + 1.5,
                    y=-0.19,
                    xref="x",
                    yref="paper",
                    text=f"<b>{hari}</b>",
                    showarrow=False,
                    font=dict(size=10, color="#19395F"),
                    xanchor="center",
                    yanchor="top"
                )

            st.plotly_chart(
                fig2_detail,
                use_container_width=True,
                config={"responsive": True}
            )

        # ======================================
        # GRAFIK 3: PEMINJAMAN RUANG
        # ======================================
        with col_grafik3:
        
            st.markdown("""
    <div class="side-chart-header">
        <div class="side-chart-title">
            Peminjaman Ruang dari Fakultas Lain
        </div>
        <div class="side-chart-subtitle">
            Sebaran sesi peminjaman berdasarkan hari dan fakultas pemberi ruang.
        </div>
    </div>
    """, unsafe_allow_html=True)


            g3 = df_fakultas[
                (df_fakultas["Status"] == "Ruang Fakultas Lain")
                & (df_fakultas["Fakultas Pemilik Ruang"] != fakultas)
                & (
                    ~df_fakultas["Fakultas Pemilik Ruang"]
                    .isin(["0", "nan", ""])
                )
            ].copy()

            plot3 = (
                g3.groupby(["Hari-Sesi", "Fakultas Pemilik Ruang"])
                .size()
                .reset_index(name="Jumlah")
                .rename(columns={
                    "Fakultas Pemilik Ruang": "Fakultas Pemberi Ruang"
                })
            )

            if plot3.empty:
                st.info(
                    f"Tidak ada peminjaman ruang dari fakultas lain untuk {fakultas}."
                )

                # Tetap tampilkan ruang grafik kosong dengan sumbu yang konsisten
                plot3 = pd.DataFrame({
                    "Hari-Sesi": urutan_x,
                    "Jumlah": [0] * len(urutan_x),
                    "Fakultas Pemberi Ruang": ["Tidak ada data"] * len(urutan_x)
                })

            fakultas_pemberi = sorted(
                plot3["Fakultas Pemberi Ruang"].dropna().unique()
            )

            indeks3 = pd.MultiIndex.from_product(
                [urutan_x, fakultas_pemberi],
                names=["Hari-Sesi", "Fakultas Pemberi Ruang"]
            )

            plot3 = (
                plot3.groupby(["Hari-Sesi", "Fakultas Pemberi Ruang"])["Jumlah"]
                .sum()
                .reindex(indeks3, fill_value=0)
                .reset_index()
            )

            fig3_detail = px.bar(
                plot3,
                x="Hari-Sesi",
                y="Jumlah",
                color="Fakultas Pemberi Ruang",
                barmode="stack",
                text=plot3["Jumlah"].where(plot3["Jumlah"] > 0, ""),
                category_orders={
                    "Hari-Sesi": urutan_x,
                    "Fakultas Pemberi Ruang": fakultas_pemberi
                },
                color_discrete_sequence=[
                    "#FF9F2E", "#294F91", "#F6C744",
                    "#6A8DCE", "#D97835", "#5A9A75"
                ]
            )

            fig3_detail.update_traces(
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(size=10),
                cliponaxis=False
            )

            fig3_detail.update_layout(
                template="plotly_white",
                height=460,
                xaxis_title=dict(text="Hari dan Sesi", standoff=65),
                yaxis_title="Jumlah Sesi Peminjaman",
                legend=dict(
                    title_text="Fakultas Pemberi Ruang",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=65, b=150, l=45, r=15),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Arial, sans-serif",
                    size=10,
                    color="#29415F"
                ),
                bargap=0.18
            )

            fig3_detail.update_xaxes(
                tickangle=0,
                tickmode="array",
                tickvals=urutan_x,
                ticktext=label_sesi,
                tickfont=dict(size=9, color="#294F85"),
                showgrid=False,
                automargin=True
            )

            fig3_detail.update_yaxes(
                rangemode="tozero",
                gridcolor="rgba(41,79,145,0.12)",
                zeroline=False
            )

            for i, hari in enumerate(urutan_hari):
                fig3_detail.add_annotation(
                    x=i * 4 + 1.5,
                    y=-0.19,
                    xref="x",
                    yref="paper",
                    text=f"<b>{hari}</b>",
                    showarrow=False,
                    font=dict(size=10, color="#19395F"),
                    xanchor="center",
                    yanchor="top"
                )

            st.plotly_chart(
                fig3_detail,
                use_container_width=True,
                config={"responsive": True}
            )





# HALAMAN DATA DAN VALIDASI
elif menu == "Data dan Validasi":
    st.markdown("## Upload Data Semester Aktif")
    st.caption(
        f"Unggah file jadwal dan rekap untuk semester **{semester}**. "
        "Data berlaku selama sesi aplikasi berjalan dan perlu diunggah ulang "
        "setelah aplikasi dimulai ulang."
    )

    up_jadwal, up_rekap = st.columns(2, gap="large")
    with up_jadwal:
        file_jadwal = st.file_uploader(
            "File Excel Jadwal Kuliah (.xlsx)",
            type=["xlsx", "xls"],
            key=f"upload_jadwal_{semester}"
        )
    with up_rekap:
        file_rekap = st.file_uploader(
            "File Excel Rekap Fakultas (.xlsx)",
            type=["xlsx", "xls"],
            key=f"upload_rekap_{semester}"
        )

    if st.button("Terapkan Data Upload", type="primary", use_container_width=True):
        if file_jadwal is None or file_rekap is None:
            st.error("Unggah kedua file terlebih dahulu: jadwal kuliah dan rekap fakultas.")
        else:
            try:
                jadwal_baru = pd.read_excel(file_jadwal)
                rekap_baru = pd.read_excel(file_rekap)
                jadwal_baru.columns = jadwal_baru.columns.astype(str).str.strip()
                rekap_baru.columns = rekap_baru.columns.astype(str).str.strip()
                if jadwal_baru.empty:
                    raise ValueError("File jadwal tidak memiliki baris data.")
                if rekap_baru.empty:
                    raise ValueError("File rekap tidak memiliki baris data.")
                rekap_baru = rekap_baru.rename(columns={"Unnamed: 0": "Fakultas"})
                if "Fakultas" not in rekap_baru.columns:
                    rekap_baru = rekap_baru.rename(columns={rekap_baru.columns[0]: "Fakultas"})
                st.session_state["data_semester"][semester] = {
                    "jadwal": jadwal_baru,
                    "rekap": rekap_baru,
                }
                st.session_state.pop("hasil_optimasi", None)
                st.success(f"Data untuk {semester} berhasil diterapkan pada sesi ini.")
                st.rerun()
            except Exception as exc:
                st.error(f"Data belum bisa diterapkan. Periksa format file Excel. Detail: {exc}")

    if semester not in st.session_state["data_semester"] and semester != "Genap 2025/2026":
        st.info("Belum ada data untuk semester ini. Unggah jadwal dan rekap, lalu klik Terapkan Data Upload.")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Baris Data Jadwal", len(df_jadwal))
    with c2:
        st.metric("Baris Data Rekap", len(df_rekap))

    if not df_jadwal.empty:
        st.markdown("### Pratinjau Jadwal Kuliah")
        st.dataframe(df_jadwal.head(20), use_container_width=True)
    else:
        st.warning("Data jadwal belum tersedia untuk semester aktif.")

    if not df_rekap.empty:
        st.markdown("### Pratinjau Rekap")
        st.dataframe(df_rekap, use_container_width=True)
    else:
        st.warning("Data rekap belum tersedia untuk semester aktif.")

# HALAMAN OPTIMASI ALOKASI
elif menu == "Optimasi Alokasi":
    st.subheader("Simulasi Optimasi Alokasi Ruang")
    st.caption("Optimasi menggunakan data semester aktif dari halaman Data dan Validasi.")

    st.info(f"Semester aktif: **{semester}**")
    col_a, col_b = st.columns(2)
    with col_a:
        kapasitas_wajib = st.checkbox("Kapasitas ruang harus mencukupi", value=True, key="opt_kapasitas")
        ruang_sendiri = st.checkbox("Utamakan ruang fakultas sendiri", value=True, key="opt_sendiri")
    with col_b:
        fakultas_terdekat = st.checkbox("Gunakan pemetaan fakultas terdekat", value=True, key="opt_terdekat")
        pindah_sesi = st.checkbox("Izinkan pindah ke sesi berikutnya jika penuh", value=True, key="opt_pindah_sesi")

    # Fakultas defisit -> fakultas pemberi yang telah ditentukan pengguna.
    pemetaan_peminjaman = {
        "FEM": ["FPIK"],
        "FMIPA": ["FAPERTA"],
        "SSMI": ["FAPERTA", "FAHUTAN"],
        "FKGIZ": ["SATARI"],
        "FISEMA": ["FAPERTA"],
    }

    def _norm_fac(x):
        return str(x).strip().upper() if pd.notna(x) else ""

    def _to_minutes(x):
        # File jadwal bisa menyimpan waktu sebagai angka desimal (mis. 9.4 = 09:40)
        # atau teks (mis. 09:40 / 09.40).
        if pd.isna(x):
            return None
        if isinstance(x, (int, float)):
            jam = int(x)
            menit = int(round((float(x) - jam) * 100))
            if menit >= 60:
                menit = int(round((float(x) - jam) * 60))
            return jam * 60 + menit
        teks = str(x).strip().replace('.', ':')
        try:
            bagian = teks.split(':')
            return int(bagian[0]) * 60 + int(bagian[1]) if len(bagian) > 1 else int(float(teks)) * 60
        except (ValueError, TypeError):
            return None

    def _optimasi_greedy(data, kapasitas_wajib=True, ruang_sendiri=True,
                         fakultas_terdekat=True, pindah_sesi=True):
        """Alokasi berbasis Hari + Kategori Sesi (1-4), bukan jam-menit."""
        wajib = ["Hari", "Kategori Sesi", "Kode Ruang", "Nama Ruangan",
                 "Fakultas Asal MK", "Fakultas Pemilik Ruang",
                 "Jumlah Mahasiswa", "Kapasitas Ruang"]
        hilang = [c for c in wajib if c not in data.columns]
        if hilang:
            raise ValueError("Kolom wajib tidak ditemukan: " + ", ".join(hilang))

        d = data.copy().reset_index(drop=True)
        d["_sesi"] = pd.to_numeric(d["Kategori Sesi"], errors="coerce")
        d["_peserta"] = pd.to_numeric(d["Jumlah Mahasiswa"], errors="coerce").fillna(0)
        d["_kapasitas"] = pd.to_numeric(d["Kapasitas Ruang"], errors="coerce").fillna(0)
        d["_asal_norm"] = d["Fakultas Asal MK"].map(_norm_fac)
        d["_hari_norm"] = d["Hari"].astype(str).str.strip().str.upper()
        # Hanya sesi 1-4; data mentah tetap utuh untuk halaman lain.
        d = d[d["_sesi"].isin([1, 2, 3, 4])].copy()
        if "Peran Optimasi" in d.columns:
            # Baris tanpa alokasi ruang fisik tidak dimasukkan jika kolom ini menandainya.
            peran = d["Peran Optimasi"].astype(str).str.strip().str.upper()
            d = d[~peran.isin(["TANPA RUANG", "ONLINE", "TIDAK PERLU RUANG"])]
        if d.empty:
            raise ValueError("Tidak ada kelas dengan Kategori Sesi 1-4 yang perlu diproses.")

        # Kandidat ruang dari seluruh ruang yang tercatat pada jadwal semester aktif.
        # Master ruang tidak memiliki kolom kapasitas, sehingga kapasitas tidak direka.
        rooms = d[["Kode Ruang", "Nama Ruangan", "Fakultas Pemilik Ruang", "Kapasitas Ruang"]].copy()
        rooms["_kap"] = pd.to_numeric(rooms["Kapasitas Ruang"], errors="coerce").fillna(0)
        rooms["_pemilik"] = rooms["Fakultas Pemilik Ruang"].map(_norm_fac)
        rooms["_kode"] = rooms["Kode Ruang"].astype(str).str.strip()
        rooms = rooms[rooms["_kode"].ne("") & rooms["_kode"].ne("nan")]
        rooms = rooms.sort_values("_kap", ascending=False).drop_duplicates("_kode").to_dict("records")
        if not rooms:
            raise ValueError("Tidak ditemukan ruang kandidat pada kolom Kode Ruang.")

        hari_urut = {h: i for i, h in enumerate(["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"])}
        d["_hari_order"] = d["_hari_norm"].map(hari_urut).fillna(99)
        d = d.sort_values(["_hari_order", "_sesi", "_peserta"], ascending=[True, True, False]).reset_index(drop=True)
        occupancy = set()
        output = []

        for _, row in d.iterrows():
            asal, hari = row["_asal_norm"], row["_hari_norm"]
            sesi_awal = int(row["_sesi"])
            peserta = int(row["_peserta"])
            pilihan_pemberi = pemetaan_peminjaman.get(asal, []) if fakultas_terdekat else []
            kode_awal = str(row["Kode Ruang"]).strip() if pd.notna(row["Kode Ruang"]) else ""

            def room_score(room):
                pemilik = room["_pemilik"]
                if ruang_sendiri and pemilik == asal:
                    prioritas = 0
                elif pemilik in pilihan_pemberi:
                    prioritas = 1 + pilihan_pemberi.index(pemilik)
                elif pemilik == asal:
                    prioritas = 0
                else:
                    prioritas = 50
                return (prioritas, max(room["_kap"] - peserta, 0), str(room["_kode"]))

            sesi_candidates = [sesi_awal]
            if pindah_sesi:
                sesi_candidates += [s for s in range(sesi_awal + 1, 5)]
            chosen = None
            for sesi in sesi_candidates:
                candidates = []
                for room in rooms:
                    if kapasitas_wajib and room["_kap"] < peserta:
                        continue
                    pemilik = room["_pemilik"]
                    if asal in pemetaan_peminjaman and fakultas_terdekat and pemilik != asal and pemilik not in pilihan_pemberi:
                        continue
                    if (room["_kode"], hari, sesi) in occupancy:
                        continue
                    candidates.append(room)
                if candidates:
                    chosen = (sorted(candidates, key=room_score)[0], sesi)
                    break

            nama_mk = row.get("Nama MK", "")
            base = {
                "Kode MK": row.get("Kode MK", ""), "Nama MK": nama_mk,
                "Fakultas Asal": row.get("Fakultas Asal MK", ""), "Hari": row.get("Hari", ""),
                "Sesi Awal": sesi_awal, "Label Sesi Awal": row.get("Label", f"Sesi {sesi_awal}"),
                "Peserta": peserta, "Ruang Awal": kode_awal,
            }
            if chosen:
                room, sesi = chosen
                occupancy.add((room["_kode"], hari, sesi))
                pemilik = room["_pemilik"]
                pindah_ruang = room["_kode"] != kode_awal
                pindah_waktu = sesi != sesi_awal
                status = "Diubah" if pindah_ruang or pindah_waktu else "Tetap"
                if pemilik == asal:
                    alasan = "Ruang fakultas sendiri tersedia"
                elif pemilik in pilihan_pemberi:
                    alasan = "Ruang pemberi sesuai pemetaan fakultas"
                else:
                    alasan = "Ruang alternatif tersedia"
                base.update({
                    "Sesi Rekomendasi": sesi, "Label Sesi Rekomendasi": f"Sesi {sesi}",
                    "Ruang Rekomendasi": room["_kode"], "Nama Ruang Rekomendasi": room.get("Nama Ruangan", ""),
                    "Fakultas Pemilik": room.get("Fakultas Pemilik Ruang", ""), "Status": status,
                    "Alasan": alasan, "_pinjam": int(pemilik != asal), "_teralokasi": 1,
                })
            else:
                base.update({
                    "Sesi Rekomendasi": "Belum tersedia", "Label Sesi Rekomendasi": "Belum tersedia",
                    "Ruang Rekomendasi": "Belum teralokasi", "Nama Ruang Rekomendasi": "",
                    "Fakultas Pemilik": "-", "Status": "Belum teralokasi",
                    "Alasan": "Tidak ada ruang yang memenuhi kapasitas, sesi, dan aturan peminjaman",
                    "_pinjam": 0, "_teralokasi": 0,
                })
            output.append(base)
        return pd.DataFrame(output)

    data_tersedia = not df_jadwal.empty
    if not data_tersedia:
        st.warning("Data jadwal semester aktif belum tersedia. Upload data terlebih dahulu pada menu Data dan Validasi.")
    else:
        st.markdown("### Data yang akan diproses")
        m1, m2 = st.columns(2)
        m1.metric("Baris jadwal", f"{len(df_jadwal):,}")
        m2.metric("Ruang unik terdeteksi", f"{df_jadwal['Kode Ruang'].nunique():,}" if "Kode Ruang" in df_jadwal.columns else "Kolom tidak ditemukan")

        if st.button("Jalankan Optimasi", type="primary", use_container_width=True):
            try:
                with st.spinner("Mencari alokasi ruang yang memenuhi kapasitas dan menghindari bentrok..."):
                    hasil = _optimasi_greedy(
                        df_jadwal,
                        kapasitas_wajib=kapasitas_wajib,
                        ruang_sendiri=ruang_sendiri,
                        fakultas_terdekat=fakultas_terdekat,
                        pindah_sesi=pindah_sesi,
                    )
                st.session_state["hasil_optimasi"] = hasil
                st.session_state["semester_hasil_optimasi"] = semester
                st.success("Proses pencarian alokasi selesai. Periksa jumlah yang berhasil dialokasikan dan yang belum teralokasi.")
            except Exception as exc:
                st.error(f"Optimasi belum dapat dijalankan: {exc}")

        hasil = st.session_state.get("hasil_optimasi")
        if hasil is not None and st.session_state.get("semester_hasil_optimasi") == semester:
            st.markdown("### Ringkasan Hasil Optimasi")
            total = len(hasil)
            teralokasi = int(hasil["_teralokasi"].sum())
            pinjam = int(hasil.loc[hasil["_teralokasi"] == 1, "_pinjam"].sum())
            berubah = int((hasil["Status"] == "Diubah").sum())
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total kelas", f"{total:,}")
            k2.metric("Berhasil dialokasikan", f"{teralokasi:,}")
            k3.metric("Peminjaman ruang", f"{pinjam:,}")
            k4.metric("Alokasi berubah", f"{berubah:,}")

            st.markdown("### Rekomendasi Alokasi Mata Kuliah")
            filter_hasil = st.radio(
                "Tampilkan",
                ["Semua kelas", "Hanya peminjaman", "Perubahan alokasi", "Belum teralokasi"],
                horizontal=True,
                key="filter_hasil_opt"
            )
            tampil = hasil.copy()
            if filter_hasil == "Hanya peminjaman":
                tampil = tampil[(tampil["_pinjam"] == 1) & (tampil["_teralokasi"] == 1)]
            elif filter_hasil == "Perubahan alokasi":
                tampil = tampil[tampil["Status"] == "Diubah"]
            elif filter_hasil == "Belum teralokasi":
                tampil = tampil[tampil["_teralokasi"] == 0]
            kolom_tampil = ["Kode MK", "Nama MK", "Fakultas Asal", "Hari", "Sesi Awal", "Sesi Rekomendasi", "Peserta", "Ruang Awal", "Ruang Rekomendasi", "Fakultas Pemilik", "Status", "Alasan"]
            st.dataframe(tampil[kolom_tampil], use_container_width=True, hide_index=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Status alokasi")
                status_count = hasil["Status"].value_counts().rename_axis("Status").reset_index(name="Jumlah")
                st.plotly_chart(px.bar(status_count, x="Status", y="Jumlah", color="Status", title="Distribusi Status Alokasi"), use_container_width=True)
            with c2:
                st.markdown("#### Peminjaman per fakultas asal")
                pinjam_df = hasil[hasil["_pinjam"] == 1].groupby("Fakultas Asal").size().reset_index(name="Jumlah Peminjaman").sort_values("Jumlah Peminjaman", ascending=False)
                if pinjam_df.empty:
                    st.info("Belum ada peminjaman pada hasil ini.")
                else:
                    st.plotly_chart(px.bar(pinjam_df, x="Fakultas Asal", y="Jumlah Peminjaman", title="Jumlah Sesi Meminjam"), use_container_width=True)

            st.download_button(
                "Unduh Hasil Optimasi (CSV)",
                data=hasil.drop(columns=["_pinjam", "_teralokasi"]).to_csv(index=False).encode("utf-8-sig"),
                file_name=f"hasil_optimasi_{semester.replace(' ', '_').replace('/', '-')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# HALAMAN HASIL REKOMENDASI
elif menu == "Hasil Rekomendasi":
    st.subheader("Hasil Rekomendasi Alokasi Ruang")
    st.caption("Hasil perubahan alokasi akan ditampilkan setelah optimasi dijalankan.")
    st.info("Belum ada hasil optimasi untuk ditampilkan.")



# FOOTER SIDEBAR
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="footer-directorate">
                Direktorat Perencanaan dan Pengembangan
            </div>
            <div class="footer-program">
                Kampus Berkelanjutan
            </div>
            <div class="footer-university">
                IPB UNIVERSITY
            </div>
        </div>  
        """,
        unsafe_allow_html=True
    )
