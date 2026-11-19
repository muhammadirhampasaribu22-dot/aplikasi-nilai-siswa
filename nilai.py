import streamlit as st
import pandas as pd

# ====== Pengaturan nilai ======
BOBOT_HARIAN = 0.30
BOBOT_ULANGAN = 0.30
BOBOT_UAS = 0.40
KKM = 70

st.set_page_config(page_title="Aplikasi Penghitung Nilai Siswa", page_icon="🎓", layout="centered")

if "data_siswa" not in st.session_state:
    st.session_state.data_siswa = []

def tentukan_grade(nilai):
    """Logika grade: mengembalikan (grade, warna, pesan)."""
    if nilai >= 85:
        return "A", "#2ecc71", "Luar biasa! Pertahankan prestasimu 🌟"
    elif nilai >= 75:
        return "B", "#3498db", "Bagus! Sedikit lagi menuju A 👍"
    elif nilai >= 65:
        return "C", "#f1c40f", "Cukup baik, ayo tingkatkan lagi 💪"
    elif nilai >= 50:
        return "D", "#e67e22", "Perlu belajar lebih giat 📚"
    else:
        return "E", "#e74c3c", "Jangan menyerah, ayo remedial! 🔥"

def susun_data():
    """Mengurutkan data dan menghitung peringkat otomatis."""
    data_urut = sorted(st.session_state.data_siswa, key=lambda x: x["Akhir"], reverse=True)
    medali = {1: "🥇 1", 2: "🥈 2", 3: "🥉 3"}
    peringkat = 0
    nilai_sebelumnya = None
    
    hasil = []
    for posisi, item in enumerate(data_urut):
        if item["Akhir"] != nilai_sebelumnya:
            peringkat = posisi + 1
            nilai_sebelumnya = item["Akhir"]
        baris = item.copy()
        baris["Peringkat"] = medali.get(peringkat, str(peringkat))
        hasil.append(baris)
    return hasil

# ====== Header ======
st.markdown(f"""
<div style="background-color:#1f2a44; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
    <h1 style="color:white; margin:0; font-size:28px;">🎓 HITUNG NILAI SISWA</h1>
    <p style="color:#bdc3c7; margin:5px 0 0 0; font-size:14px;">
        Harian {int(BOBOT_HARIAN*100)}% &nbsp;•&nbsp; Ulangan {int(BOBOT_ULANGAN*100)}% &nbsp;•&nbsp; 
        UAS {int(BOBOT_UAS*100)}% &nbsp;•&nbsp; KKM {KKM}
    </p>
</div>
""", unsafe_allow_html=True)

# ====== Form Input & Pratinjau Langsung ======
with st.container(border=True):
    nama = st.text_input("👤 Nama Siswa", placeholder="Masukkan nama lengkap siswa...")
    col1, col2, col3 = st.columns(3)
    with col1:
        harian = st.number_input("📘 Nilai Harian", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    with col2:
        ulangan = st.number_input("📝 Nilai Ulangan", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    with col3:
        uas = st.number_input("🏆 Nilai UAS", min_value=0.0, max_value=100.0, value=0.0, step=1.0)

    akhir_preview = harian * BOBOT_HARIAN + ulangan * BOBOT_ULANGAN + uas * BOBOT_UAS
    grade_p, warna_p, pesan_p = tentukan_grade(akhir_preview)
    status_p = "LULUS ✔" if akhir_preview >= KKM else "TIDAK LULUS ✘"

    st.markdown("---")
    p_col1, p_col2, p_col3 = st.columns([1.2, 3, 0.8])
    with p_col1:
        st.markdown(f"<h1 style='color:{warna_p}; margin:0;'>{akhir_preview:.1f}</h1>", unsafe_allow_html=True)
    with p_col2:
        st.markdown(f"**{nama.strip() if nama.strip() else 'Pratinjau Nilai'}**")
        st.caption(f"{status_p}  •  {pesan_p}")
    with p_col3:
        st.markdown(f"""
        <div style='background-color:{warna_p}; color:white; font-size:24px; font-weight:bold; 
                    text-align:center; border-radius:8px; padding:8px;'>{grade_p}</div>
        """, unsafe_allow_html=True)
    
    st.progress(min(int(akhir_preview), 100))

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        if st.button("✔ Tambah & Hitung", type="primary", use_container_width=True):
            if not nama.strip():
                st.error("Nama siswa tidak boleh kosong!")
            else:
                st.session_state.data_siswa.append({
                    "Nama": nama.strip(),
                    "Harian": harian,
                    "Ulangan": ulangan,
                    "UAS": uas,
                    "Akhir": round(akhir_preview, 2),
                    "Grade": grade_p,
                    "Status": "✔ LULUS" if akhir_preview >= KKM else "✘ TIDAK LULUS"
                })
                st.rerun()
    with t_col2:
        if st.button("↺ Reset Semua Data", use_container_width=True):
            st.session_state.data_siswa = []
            st.rerun()

# ====== Statistik, Podium & Tabel ======
data_terurut = susun_data()

if data_terurut:
    daftar_akhir = [d["Akhir"] for d in data_terurut]
    lulus_count = sum(1 for n in daftar_akhir if n >= KKM)

    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("👥 Siswa", len(daftar_akhir))
    s2.metric("📊 Rata-rata", f"{sum(daftar_akhir)/len(daftar_akhir):.1f}")
    s3.metric("⬆ Tertinggi", f"{max(daftar_akhir):.1f}")
    s4.metric("⬇ Terendah", f"{min(daftar_akhir):.1f}")
    s5.metric("✔ Lulus", f"{lulus_count}/{len(daftar_akhir)}")

    st.markdown("### 🏆 Podium Top 3")
    pod_cols = st.columns(3)
    podium_style = [("🥇", "#f1c40f"), ("🥈", "#bdc3c7"), ("🥉", "#cd7f32")]
    for idx in range(3):
        medali_ikon, bg_warna = podium_style[idx]
        if idx < len(data_terurut):
            p_nama = data_terurut[idx]["Nama"]
            p_nilai = f"{data_terurut[idx]['Akhir']:.2f}"
        else:
            p_nama = "-"
            p_nilai = ""
        with pod_cols[idx]:
            st.markdown(f"""
            <div style="background-color:{bg_warna}; padding:12px; border-radius:8px; text-align:center; color:#2c3e50;">
                <div style="font-size:28px;">{medali_ikon}</div>
                <div style="font-weight:bold; font-size:16px;">{p_nama}</div>
                <div style="font-size:14px;">{p_nilai}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📋 Daftar Nilai & Peringkat")
    df = pd.DataFrame(data_terurut)[["Peringkat", "Nama", "Harian", "Ulangan", "UAS", "Akhir", "Grade", "Status"]]
    
    def warna_baris(row):
        warna_map = {"A": "#d5f5e3", "B": "#d6eaf8", "C": "#fcf3cf", "D": "#fae5d3", "E": "#f5b7b1"}
        return [f"background-color: {warna_map.get(row['Grade'], '#ffffff')}; color: #2c3e50"] * len(row)

    st.dataframe(df.style.apply(warna_baris, axis=1), use_container_width=True, hide_index=True)

    b_col1, b_col2 = st.columns([3, 1])
    with b_col1:
        daftar_nama = [f"{i+1}. {d['Nama']} ({d['Akhir']})" for i, d in enumerate(data_terurut)]
        pilih_hapus = st.selectbox("Pilih siswa untuk dihapus:", daftar_nama, label_visibility="collapsed")
    with b_col2:
        if st.button("🗑 Hapus Terpilih", use_container_width=True):
            idx_hapus = daftar_nama.index(pilih_hapus)
            target_item = data_terurut[idx_hapus]
            for i, asli in enumerate(st.session_state.data_siswa):
                if asli["Nama"] == target_item["Nama"] and asli["Akhir"] == target_item["Akhir"]:
                    st.session_state.data_siswa.pop(i)
                    break
            st.rerun()

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="💾 Simpan / Unduh CSV (Excel)",
        data=csv_data,
        file_name="nilai_siswa.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("Belum ada data siswa. Silakan isi form di atas dan klik **Tambah & Hitung**.")