"""
Akıllı Enerji Takip ve Analiz Sistemi
Streamlit MVP - Hackathon Ready
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# SAYFA YAPILANDIRMASI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Enerji Takip Sistemi",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Eco-Tech Tema
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ---- RESET & BASE ---- */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080f1a !important;
    color: #e2f0e8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0d1826 !important;
    border-right: 1px solid #1a3a2a !important;
}

[data-testid="stSidebar"] * { color: #b8d4c0 !important; }

/* ---- HEADER ---- */
.hero-header {
    background: linear-gradient(135deg, #0a2a1a 0%, #0d2b3e 50%, #0a1f2e 100%);
    border: 1px solid #1e4d35;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(34,197,94,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(56,189,248,0.10) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4ade80, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 6px 0;
    line-height: 1.2;
}
.hero-sub {
    font-size: 1.0rem;
    color: #7fb89a;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(74,222,128,0.12);
    border: 1px solid rgba(74,222,128,0.35);
    color: #4ade80;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    text-transform: uppercase;
}

/* ---- METRIC CARDS ---- */
.metric-card {
    background: linear-gradient(145deg, #0d1f2d, #0a1a28);
    border: 1px solid #1a3a4a;
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: #2a6a5a; }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4ade80, #38bdf8);
    border-radius: 14px 14px 0 0;
}
.metric-icon { font-size: 1.6rem; margin-bottom: 8px; }
.metric-label {
    font-size: 0.75rem;
    color: #6b9e80;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 600;
    color: #e2f0e8;
    line-height: 1.1;
}
.metric-unit { font-size: 0.85rem; color: #7fb89a; margin-left: 4px; }
.metric-delta {
    font-size: 0.78rem;
    margin-top: 6px;
    padding: 2px 8px;
    border-radius: 8px;
    display: inline-block;
}
.delta-up { background: rgba(248,113,113,0.15); color: #f87171; }
.delta-down { background: rgba(74,222,128,0.15); color: #4ade80; }
.delta-neutral { background: rgba(251,191,36,0.15); color: #fbbf24; }

/* ---- SECTION HEADERS ---- */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2f0e8;
    margin: 28px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1a3a4a, transparent);
}

/* ---- INPUT PANEL ---- */
.input-panel {
    background: linear-gradient(145deg, #0d1f2d, #0a1a28);
    border: 1px solid #1a3a4a;
    border-radius: 14px;
    padding: 24px;
}

/* ---- AI INSIGHT CARDS ---- */
.insight-card {
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    border-left: 4px solid;
}
.insight-warning {
    background: rgba(251,191,36,0.08);
    border-color: #fbbf24;
}
.insight-success {
    background: rgba(74,222,128,0.08);
    border-color: #4ade80;
}
.insight-info {
    background: rgba(56,189,248,0.08);
    border-color: #38bdf8;
}
.insight-danger {
    background: rgba(248,113,113,0.08);
    border-color: #f87171;
}
.insight-emoji { font-size: 1.4rem; flex-shrink: 0; }
.insight-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 3px; }
.insight-body { font-size: 0.82rem; color: #8ab4a0; line-height: 1.5; }

/* ---- BUTTONS ---- */
.stButton > button {
    background: linear-gradient(135deg, #14532d, #0c4a6e) !important;
    color: #e2f0e8 !important;
    border: 1px solid #1a5c3a !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 18px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #16643c, #0e5a82) !important;
    border-color: #4ade80 !important;
    color: #4ade80 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(74,222,128,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Primary action button */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #166534, #15803d) !important;
    border-color: #4ade80 !important;
}

/* ---- SELECTBOX & INPUTS ---- */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider > div { 
    background: #0d1f2d !important; 
    border-color: #1a3a4a !important;
    color: #e2f0e8 !important;
}

/* ---- DATA TABLE ---- */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ---- DIVIDER ---- */
hr { border-color: #1a3a4a !important; }

/* ---- REPORT PANEL ---- */
.report-box {
    background: linear-gradient(145deg, #0d1f2d, #091825);
    border: 1px solid #1a3a4a;
    border-radius: 14px;
    padding: 24px;
}
.report-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1a2e3a;
    font-size: 0.88rem;
}
.report-item:last-child { border-bottom: none; }
.report-key { color: #7fb89a; }
.report-val { font-family: 'JetBrains Mono', monospace; color: #e2f0e8; font-weight: 600; }

/* ---- STATUS BADGE ---- */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4ade80;
    margin-right: 6px;
    box-shadow: 0 0 8px #4ade80;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080f1a; }
::-webkit-scrollbar-thumb { background: #1a3a4a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2a5a6a; }

/* ---- TAB OVERRIDES ---- */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1826 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b9e80 !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #14532d, #0c4a6e) !important;
    color: #4ade80 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# OTURUM DURUMU BAŞLATMA
# ─────────────────────────────────────────────
def init_session():
    if "tuketim_verisi" not in st.session_state:
        # Demo için son 14 günlük sahte veri
        bugun = datetime.now()
        st.session_state["tuketim_verisi"] = []
        cihazlar = ["Klima", "Bilgisayar", "TV", "Buzdolabı", "Diğer"]
        for i in range(14):
            gun = bugun - timedelta(days=13 - i)
            for _ in range(random.randint(1, 3)):
                cihaz = random.choice(cihazlar)
                sure = round(random.uniform(1, 8), 1)
                kwh = round(random.uniform(0.5, 4.5), 2)
                st.session_state["tuketim_verisi"].append({
                    "tarih": gun.strftime("%Y-%m-%d"),
                    "saat": random.randint(7, 23),
                    "cihaz": cihaz,
                    "sure": sure,
                    "kwh": kwh,
                })
    if "aktif_panel" not in st.session_state:
        st.session_state["aktif_panel"] = "gunluk"
    if "son_eklenen" not in st.session_state:
        st.session_state["son_eklenen"] = None

init_session()


# ─────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────
def veri_ozeti():
    veriler = st.session_state["tuketim_verisi"]
    if not veriler:
        return {"bugun": 0, "haftalik": 0, "aylik": 0, "ortalama": 0}
    bugun = datetime.now().strftime("%Y-%m-%d")
    bugun_kwh = sum(v["kwh"] for v in veriler if v["tarih"] == bugun)
    haftalik_bas = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    haftalik_kwh = sum(v["kwh"] for v in veriler if v["tarih"] >= haftalik_bas)
    aylik_bas = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    aylik_kwh = sum(v["kwh"] for v in veriler if v["tarih"] >= aylik_bas)
    tarihler = sorted(set(v["tarih"] for v in veriler))
    gunluk_toplamlar = []
    for t in tarihler:
        gunluk_toplamlar.append(sum(v["kwh"] for v in veriler if v["tarih"] == t))
    ortalama = round(sum(gunluk_toplamlar) / len(gunluk_toplamlar), 2) if gunluk_toplamlar else 0
    return {
        "bugun": round(bugun_kwh, 2),
        "haftalik": round(haftalik_kwh, 2),
        "aylik": round(aylik_kwh, 2),
        "ortalama": ortalama,
    }

def gunluk_grafik_verisi():
    veriler = st.session_state["tuketim_verisi"]
    tarihler = sorted(set(v["tarih"] for v in veriler))[-14:]
    toplamlar = [round(sum(v["kwh"] for v in veriler if v["tarih"] == t), 2) for t in tarihler]
    return tarihler, toplamlar

def cihaz_grafik_verisi():
    veriler = st.session_state["tuketim_verisi"]
    cihazlar = ["Klima", "TV", "Bilgisayar", "Buzdolabı", "Diğer"]
    toplamlar = {c: round(sum(v["kwh"] for v in veriler if v["cihaz"] == c), 2) for c in cihazlar}
    return toplamlar

def yapay_zeka_analizi(panel="gunluk"):
    ozet = veri_ozeti()
    cihaz_data = cihaz_grafik_verisi()
    insights = []
    veriler = st.session_state["tuketim_verisi"]
    gece_kullanim = sum(v["kwh"] for v in veriler if v.get("saat", 12) >= 22 or v.get("saat", 12) <= 6)

    if panel == "gunluk":
        if ozet["bugun"] == 0:
            insights.append(("info", "ℹ️", "Bugün Veri Yok",
                "Henüz bugün için veri girilmedi. Veri Girişi sekmesinden ekleme yapabilirsiniz."))
        elif ozet["bugun"] > ozet["ortalama"] * 1.3:
            insights.append(("danger", "🚨", "Yüksek Tüketim Uyarısı",
                f"Bugünkü tüketim ({ozet['bugun']} kWh) günlük ortalamanın ({ozet['ortalama']} kWh) %{int((ozet['bugun']/ozet['ortalama']-1)*100)} üzerinde!"))
        elif ozet["bugun"] > ozet["ortalama"] * 1.1:
            insights.append(("warning", "⚠️", "Yüksek Enerji Tüketimi",
                f"Bugün normalden biraz fazla tüketim var ({ozet['bugun']} kWh). Dikkatli olun."))
        else:
            insights.append(("success", "✅", "Enerji Kullanımı Dengeli",
                f"Bugünkü tüketim ({ozet['bugun']} kWh) normale uygun. Harika gidiyorsunuz!"))
        if gece_kullanim > 2:
            insights.append(("warning", "🌙", "Gece Kullanımı",
                f"Gece saatlerinde toplam {round(gece_kullanim,2)} kWh harcandı. Gereksiz cihazları kapatmayı düşünün."))

    elif panel == "haftalik":
        haftalik_hedef = ozet["ortalama"] * 7
        oran = (ozet["haftalik"] / haftalik_hedef * 100) if haftalik_hedef > 0 else 100
        if oran > 120:
            insights.append(("danger", "📈", "Haftalık Hedef Aşıldı",
                f"Bu haftaki tüketim ({ozet['haftalik']} kWh), beklenen haftalık değerin %{int(oran)}'ine ulaştı."))
        elif oran > 100:
            insights.append(("warning", "⚠️", "Hedef Yaklaşıyor",
                f"Bu haftaki tüketim ({ozet['haftalik']} kWh) haftalık hedefin %{int(oran)}'inde."))
        else:
            insights.append(("success", "🎯", "Haftalık Hedef Tutturuldu",
                f"Bu hafta {ozet['haftalik']} kWh harcadınız. Hedefin altındasınız, tebrikler!"))
        en_cok_cihaz = max(cihaz_data, key=cihaz_data.get)
        insights.append(("info", "🔌", f"En Çok Kullanan: {en_cok_cihaz}",
            f"Bu hafta en fazla enerji tüketen cihaz {en_cok_cihaz} ({cihaz_data[en_cok_cihaz]} kWh). Kullanımı optimize edin."))

    elif panel == "aylik":
        insights.append(("info", "📅", "Aylık Tüketim Özeti",
            f"Bu ay toplam {ozet['aylik']} kWh enerji harcandı. Geçen aya kıyasla %8 düşüş var (demo verisi)."))
        insights.append(("success", "💰", "Tahmini Maliyet",
            f"Bu ayki tüketiminizin tahmini maliyeti ≈ {round(ozet['aylik'] * 2.8, 1)} TL (0.28 TL/kWh birim fiyatıyla)."))
        if cihaz_data.get("Klima", 0) > 10:
            insights.append(("warning", "❄️", "Klima Tüketimi Yüksek",
                "Klimanın aylık tüketimi ortalamanın üzerinde. Termostatı 1°C düşürmek %6 tasarruf sağlar."))

    elif panel == "tasarruf":
        insights.append(("success", "💡", "LED Ampul Dönüşümü",
            "Tüm ampulleri LED ile değiştirerek aydınlatma harcamasını %75 azaltabilirsiniz."))
        insights.append(("success", "🌡️", "Klima Optimizasyonu",
            "Klima kullanım süresini azaltmayı düşünebilirsiniz. Termostatı 24°C'ye ayarlayın."))
        insights.append(("info", "🔋", "Standby Modu",
            "Enerji tasarrufu için cihazları standby modundan çıkarın. Yıllık %10 tasarruf sağlar."))
        insights.append(("info", "⏰", "Gece Tarifesi",
            "Çamaşır ve bulaşık makinelerini gece tarifesinde (22:00–06:00) çalıştırın."))
        insights.append(("warning", "🚿", "Su Isıtıcı",
            "Şofbenin gereksiz çalışmasını önlemek için termostatını 55°C'ye ayarlayın."))

    elif panel == "verimlilik":
        for cihaz, kwh in sorted(cihaz_data.items(), key=lambda x: -x[1]):
            if kwh == 0:
                continue
            if cihaz == "Klima":
                tip = "danger" if kwh > 15 else "warning"
                mesaj = f"Klima toplam {kwh} kWh tüketti. A+++ sınıfı bir klima ile %40 tasarruf mümkün."
            elif cihaz == "Buzdolabı":
                tip = "info"
                mesaj = f"Buzdolabı {kwh} kWh tüketti. Arka boşluğu açık tutmak verimliliği artırır."
            elif cihaz == "Bilgisayar":
                tip = "info"
                mesaj = f"Bilgisayar {kwh} kWh harcadı. Kullanmadığında uyku moduna alın."
            elif cihaz == "TV":
                tip = "warning" if kwh > 8 else "success"
                mesaj = f"TV {kwh} kWh harcadı. Parlaklığı düşürmek enerji tüketimini azaltır."
            else:
                tip = "info"
                mesaj = f"Diğer cihazlar toplam {kwh} kWh tüketti."
            insights.append((tip, "⚡", f"{cihaz} Verimliliği", mesaj))

    return insights

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#b8d4c0", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#1a3a4a", linecolor="#1a3a4a", tickcolor="#1a3a4a"),
    yaxis=dict(gridcolor="#1a3a4a", linecolor="#1a3a4a", tickcolor="#1a3a4a"),
)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px 0;'>
        <div style='font-size:2.8rem;'>⚡</div>
        <div style='font-size:1.05rem; font-weight:700; color:#4ade80; margin-top:6px;'>EnerjiTakip</div>
        <div style='font-size:0.72rem; color:#4a7a60; margin-top:4px; letter-spacing:0.1em;'>v1.0 MVP</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**⚡ Hızlı Analiz**")
    if st.button("📊 Günlük Analiz", use_container_width=True):
        st.session_state["aktif_panel"] = "gunluk"
    if st.button("📅 Haftalık Rapor", use_container_width=True):
        st.session_state["aktif_panel"] = "haftalik"
    if st.button("🗓️ Aylık Karşılaştırma", use_container_width=True):
        st.session_state["aktif_panel"] = "aylik"
    if st.button("💡 Tasarruf Önerileri", use_container_width=True):
        st.session_state["aktif_panel"] = "tasarruf"
    if st.button("🔌 Cihaz Verimliliği", use_container_width=True):
        st.session_state["aktif_panel"] = "verimlilik"

    st.markdown("---")
    ozet = veri_ozeti()
    st.markdown(f"""
    <div style='background:#0a1f2e; border-radius:10px; padding:14px; font-size:0.82rem;'>
        <div style='color:#6b9e80; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.08em; font-size:0.70rem;'>Anlık Durum</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
            <span style='color:#7fb89a;'>Bugün</span>
            <span style='color:#4ade80; font-family:monospace; font-weight:700;'>{ozet['bugun']} kWh</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
            <span style='color:#7fb89a;'>Bu Hafta</span>
            <span style='color:#38bdf8; font-family:monospace; font-weight:700;'>{ozet['haftalik']} kWh</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='color:#7fb89a;'>Bu Ay</span>
            <span style='color:#a78bfa; font-family:monospace; font-weight:700;'>{ozet['aylik']} kWh</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#4a7a60; text-align:center;'>
        <span class='status-dot'></span>Sistem Aktif &nbsp;|&nbsp; {datetime.now().strftime('%d.%m.%Y %H:%M')}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ANA ALAN
# ─────────────────────────────────────────────

# HERO HEADER
st.markdown("""
<div class='hero-header'>
    <div class='hero-badge'>⚡ Akıllı Enerji Sistemi</div>
    <h1 class='hero-title'>Akıllı Enerji Takip ve Analiz Sistemi</h1>
    <p class='hero-sub'>Enerji tüketiminizi takip edin, analiz edin ve tasarruf önerileri alın.</p>
</div>
""", unsafe_allow_html=True)

# ---- METRİK KARTLARI ----
ozet = veri_ozeti()
tarihler, toplamlar = gunluk_grafik_verisi()
bugun_delta = round(ozet["bugun"] - ozet["ortalama"], 2)
delta_class = "delta-up" if bugun_delta > 0 else ("delta-down" if bugun_delta < 0 else "delta-neutral")
delta_icon = "↑" if bugun_delta > 0 else ("↓" if bugun_delta < 0 else "→")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>⚡</div>
        <div class='metric-label'>Günlük Tüketim</div>
        <div class='metric-value'>{ozet['bugun']}<span class='metric-unit'>kWh</span></div>
        <div class='metric-delta {delta_class}'>{delta_icon} {abs(bugun_delta)} kWh ortalamaya göre</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>📅</div>
        <div class='metric-label'>Haftalık Toplam</div>
        <div class='metric-value'>{ozet['haftalik']}<span class='metric-unit'>kWh</span></div>
        <div class='metric-delta delta-neutral'>→ Son 7 gün</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>🗓️</div>
        <div class='metric-label'>Aylık Toplam</div>
        <div class='metric-value'>{ozet['aylik']}<span class='metric-unit'>kWh</span></div>
        <div class='metric-delta delta-down'>↓ Son 30 gün</div>
    </div>""", unsafe_allow_html=True)
with col4:
    maliyet = round(ozet["aylik"] * 2.8, 0)
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>💰</div>
        <div class='metric-label'>Tahmini Maliyet</div>
        <div class='metric-value'>{int(maliyet)}<span class='metric-unit'>TL</span></div>
        <div class='metric-delta delta-neutral'>→ 0.28 TL/kWh birim fiyat</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ANA SEKMELİ YAPISI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Grafikler", "📝 Veri Girişi", "🤖 YZ Analizi", "📋 Kayıtlar"])

# ─────────────────── TAB 1: GRAFİKLER ───────────────────
with tab1:
    st.markdown("<div class='section-title'>📈 Günlük Enerji Tüketimi (Son 14 Gün)</div>", unsafe_allow_html=True)

    tarihler, toplamlar = gunluk_grafik_verisi()
    avg_line = [ozet["ortalama"]] * len(tarihler)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=tarihler, y=toplamlar,
        mode="lines+markers",
        name="Günlük Tüketim",
        line=dict(color="#4ade80", width=2.5),
        marker=dict(color="#4ade80", size=7, symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(74,222,128,0.07)",
    ))
    fig1.add_trace(go.Scatter(
        x=tarihler, y=avg_line,
        mode="lines",
        name="Ortalama",
        line=dict(color="#fbbf24", width=1.5, dash="dot"),
    ))
    fig1.update_layout(**PLOTLY_LAYOUT,
        title="kWh / Gün",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#b8d4c0")),
        height=320,
    )
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-title'>🔌 Cihaz Bazlı Tüketim</div>", unsafe_allow_html=True)
        cihaz_data = cihaz_grafik_verisi()
        fig2 = go.Figure(go.Bar(
            x=list(cihaz_data.keys()),
            y=list(cihaz_data.values()),
            marker=dict(
                color=["#4ade80", "#38bdf8", "#a78bfa", "#fbbf24", "#f87171"],
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            text=[f"{v} kWh" for v in cihaz_data.values()],
            textposition="outside",
            textfont=dict(color="#b8d4c0", size=11),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=300, title="Toplam kWh / Cihaz")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown("<div class='section-title'>🥧 Tüketim Dağılımı</div>", unsafe_allow_html=True)
        cihaz_data = cihaz_grafik_verisi()
        aktif_cihazlar = {k: v for k, v in cihaz_data.items() if v > 0}
        fig3 = go.Figure(go.Pie(
            labels=list(aktif_cihazlar.keys()),
            values=list(aktif_cihazlar.values()),
            hole=0.5,
            marker=dict(colors=["#4ade80", "#38bdf8", "#a78bfa", "#fbbf24", "#f87171"],
                        line=dict(color="#080f1a", width=2)),
            textfont=dict(color="#e2f0e8", size=12),
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=300, title="% Dağılım",
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#b8d4c0"), orientation="h", y=-0.15))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # Saatlik dağılım
    st.markdown("<div class='section-title'>🕐 Saatlik Kullanım Dağılımı</div>", unsafe_allow_html=True)
    veriler = st.session_state["tuketim_verisi"]
    saatlik = {h: 0.0 for h in range(24)}
    for v in veriler:
        s = v.get("saat", 12)
        saatlik[s] = round(saatlik[s] + v["kwh"], 2)
    saat_labels = [f"{h:02d}:00" for h in range(24)]
    saat_values = [saatlik[h] for h in range(24)]
    colors_h = ["#f87171" if (h >= 22 or h <= 5) else "#38bdf8" if (6 <= h <= 9 or 17 <= h <= 21) else "#4ade80" for h in range(24)]

    fig4 = go.Figure(go.Bar(
        x=saat_labels, y=saat_values,
        marker_color=colors_h,
        name="kWh",
    ))
    fig4.update_layout(**PLOTLY_LAYOUT, height=220, title="kWh / Saat  (🔴 Gece  🔵 Yoğun  🟢 Normal)")
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})


# ─────────────────── TAB 2: VERİ GİRİŞİ ───────────────────
with tab2:
    st.markdown("<div class='section-title'>📝 Yeni Tüketim Verisi Ekle</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='input-panel'>", unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            kwh_giris = st.number_input("⚡ Günlük Enerji Tüketimi (kWh)",
                                         min_value=0.1, max_value=100.0, value=2.5, step=0.1,
                                         help="Cihazın bu kullanım için harcadığı kWh değeri")
        with r1c2:
            cihaz_secim = st.selectbox("🔌 Cihaz Seçimi",
                                        ["Klima", "TV", "Bilgisayar", "Buzdolabı", "Diğer"],
                                        help="Enerji tüketen cihazı seçin")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            sure_giris = st.number_input("⏱️ Kullanım Süresi (Saat)",
                                          min_value=0.5, max_value=24.0, value=2.0, step=0.5,
                                          help="Cihazın kaç saat kullanıldığı")
        with r2c2:
            saat_giris = st.number_input("🕐 Kullanım Saati (0–23)",
                                          min_value=0, max_value=23, value=datetime.now().hour,
                                          help="Kullanımın başladığı saat")

        tarih_giris = st.date_input("📅 Tarih", value=datetime.now().date())

        st.markdown("</div>", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        if st.button("➕ Veri Ekle", use_container_width=True):
            st.session_state["tuketim_verisi"].append({
                "tarih": str(tarih_giris),
                "saat": int(saat_giris),
                "cihaz": cihaz_secim,
                "sure": float(sure_giris),
                "kwh": float(kwh_giris),
            })
            st.session_state["son_eklenen"] = cihaz_secim
            st.success(f"✅ {cihaz_secim} verisi başarıyla eklendi! ({kwh_giris} kWh, {sure_giris} saat)")
            st.rerun()
    with bc2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            st.session_state["tuketim_verisi"] = []
            st.warning("⚠️ Tüm veriler temizlendi.")
            st.rerun()
    with bc3:
        if st.button("🤖 Analiz Et", use_container_width=True):
            st.session_state["aktif_panel"] = "gunluk"
            st.info("YZ Analizi sekmesine geçin veya sol menüden seçin.")

    if st.session_state.get("son_eklenen"):
        st.markdown(f"""
        <div style='background:rgba(74,222,128,0.08); border:1px solid rgba(74,222,128,0.3); 
             border-radius:10px; padding:12px 18px; margin-top:12px; font-size:0.85rem;'>
            <strong style='color:#4ade80;'>Son Eklenen:</strong>
            <span style='color:#b8d4c0;'> {st.session_state['son_eklenen']} — {kwh_giris} kWh / {sure_giris} saat</span>
        </div>
        """, unsafe_allow_html=True)

    # Toplu veri önizlemesi
    st.markdown("<div class='section-title'>📋 Son Girilen Veriler</div>", unsafe_allow_html=True)
    veriler = st.session_state["tuketim_verisi"]
    if veriler:
        son_10 = veriler[-10:][::-1]
        import pandas as pd
        df = pd.DataFrame(son_10)[["tarih", "cihaz", "sure", "kwh", "saat"]]
        df.columns = ["Tarih", "Cihaz", "Süre (saat)", "Tüketim (kWh)", "Saat"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Henüz veri girilmedi.")


# ─────────────────── TAB 3: YZ ANALİZİ ───────────────────
with tab3:
    panel = st.session_state.get("aktif_panel", "gunluk")

    panel_adi = {
        "gunluk": "📊 Günlük Analiz",
        "haftalik": "📅 Haftalık Rapor",
        "aylik": "🗓️ Aylık Karşılaştırma",
        "tasarruf": "💡 Tasarruf Önerileri",
        "verimlilik": "🔌 Cihaz Verimliliği",
    }
    st.markdown(f"<div class='section-title'>{panel_adi.get(panel, '🤖 Yapay Zekâ Analizi')}</div>", unsafe_allow_html=True)

    # Butonlar tekrar burada da
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        if st.button("📊 Günlük", use_container_width=True):
            st.session_state["aktif_panel"] = "gunluk"; st.rerun()
    with b2:
        if st.button("📅 Haftalık", use_container_width=True):
            st.session_state["aktif_panel"] = "haftalik"; st.rerun()
    with b3:
        if st.button("🗓️ Aylık", use_container_width=True):
            st.session_state["aktif_panel"] = "aylik"; st.rerun()
    with b4:
        if st.button("💡 Tasarruf", use_container_width=True):
            st.session_state["aktif_panel"] = "tasarruf"; st.rerun()
    with b5:
        if st.button("🔌 Verimlilik", use_container_width=True):
            st.session_state["aktif_panel"] = "verimlilik"; st.rerun()

    st.markdown("")

    insights = yapay_zeka_analizi(panel)
    if insights:
        for tip, emoji, baslik, aciklama in insights:
            st.markdown(f"""
            <div class='insight-card insight-{tip}'>
                <div class='insight-emoji'>{emoji}</div>
                <div>
                    <div class='insight-title' style='color: {"#f87171" if tip=="danger" else "#fbbf24" if tip=="warning" else "#4ade80" if tip=="success" else "#38bdf8"};'>{baslik}</div>
                    <div class='insight-body'>{aciklama}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Bu panel için analiz üretildi.")

    # Özet tablo
    st.markdown("<div class='section-title'>📊 Özet İstatistikler</div>", unsafe_allow_html=True)
    ozet = veri_ozeti()
    cihaz_data = cihaz_grafik_verisi()
    en_fazla = max(cihaz_data, key=cihaz_data.get)
    toplam_sure = sum(v["sure"] for v in st.session_state["tuketim_verisi"])

    st.markdown(f"""
    <div class='report-box'>
        <div class='report-item'>
            <span class='report-key'>Bugünkü Tüketim</span>
            <span class='report-val'>{ozet['bugun']} kWh</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>Haftalık Toplam</span>
            <span class='report-val'>{ozet['haftalik']} kWh</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>Aylık Toplam</span>
            <span class='report-val'>{ozet['aylik']} kWh</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>Günlük Ortalama</span>
            <span class='report-val'>{ozet['ortalama']} kWh</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>En Fazla Tüketen Cihaz</span>
            <span class='report-val'>{en_fazla} ({cihaz_data[en_fazla]} kWh)</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>Toplam Kullanım Süresi</span>
            <span class='report-val'>{round(toplam_sure, 1)} saat</span>
        </div>
        <div class='report-item'>
            <span class='report-key'>Tahmini Aylık Maliyet</span>
            <span class='report-val'>{round(ozet["aylik"] * 2.8, 1)} TL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────── TAB 4: KAYITLAR ───────────────────
with tab4:
    st.markdown("<div class='section-title'>📋 Tüm Kayıtlar</div>", unsafe_allow_html=True)
    veriler = st.session_state["tuketim_verisi"]
    if veriler:
        import pandas as pd
        df_all = pd.DataFrame(veriler)
        df_all.columns = ["Tarih", "Saat", "Cihaz", "Süre (saat)", "Tüketim (kWh)"]
        df_all = df_all.sort_values("Tarih", ascending=False).reset_index(drop=True)

        # Filtreler
        fc1, fc2 = st.columns(2)
        with fc1:
            cihaz_filtre = st.selectbox("Cihaza Göre Filtrele",
                                         ["Tümü"] + list(df_all["Cihaz"].unique()))
        with fc2:
            sirala = st.selectbox("Sıralama", ["Tarihe Göre (Yeni→Eski)", "Tüketime Göre (Yüksek→Düşük)"])

        if cihaz_filtre != "Tümü":
            df_all = df_all[df_all["Cihaz"] == cihaz_filtre]
        if "Tüketime" in sirala:
            df_all = df_all.sort_values("Tüketim (kWh)", ascending=False)

        st.dataframe(df_all, use_container_width=True, hide_index=True, height=400)

        st.markdown(f"""
        <div style='font-size:0.82rem; color:#6b9e80; margin-top:8px; text-align:right;'>
            Toplam <strong style='color:#4ade80;'>{len(df_all)}</strong> kayıt |
            Toplam <strong style='color:#38bdf8;'>{round(df_all["Tüketim (kWh)"].sum(), 2)} kWh</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#4a7a60;'>
            <div style='font-size:3rem; margin-bottom:12px;'>📂</div>
            <div style='font-size:1rem;'>Henüz kayıt bulunmuyor.</div>
            <div style='font-size:0.85rem; margin-top:6px;'>Veri Girişi sekmesinden veri ekleyin.</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 16px 0; border-top:1px solid #1a3a4a; margin-top:32px;'>
    <div style='font-size:0.78rem; color:#4a7a60;'>
        ⚡ <strong style='color:#4ade80;'>Akıllı Enerji Takip ve Analiz Sistemi</strong> &nbsp;|&nbsp; 
        Hackathon MVP &nbsp;|&nbsp; Streamlit + Plotly &nbsp;|&nbsp; 2025
    </div>
    <div style='font-size:0.72rem; color:#2a4a35; margin-top:6px;'>
        Enerji tüketiminizi takip edin, analiz edin ve tasarruf önerileri alın.
    </div>
</div>
""", unsafe_allow_html=True)
