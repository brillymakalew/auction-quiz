import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import glob

# ----------------------------------------------------
# STREAMLIT CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Auction Pertanyaan Kelompok",
    layout="wide",
)

# ----------------------------------------------------
# GLOBAL STYLE (THEME)
# ----------------------------------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #222b3f 0, #0b1020 45%, #050712 100%);
        color: #f7f7ff;
    }
    [data-testid="stHeader"] { background: transparent; }

    /* Sedikit rapikan padding utama */
    [data-testid="stAppViewContainer"] > .main {
        padding: 1.4rem 2.4rem 2.2rem 2.4rem;
    }

    [data-testid="stSidebar"] {
        background: #0f172a;
        color: #e5e7eb;
    }

    h1, h2, h3, h4, h5 {
        color: #e5e7ff;
        font-weight: 700;
    }
    p, label, span, div { color: #e5e7eb; }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #f97316, #facc15, #22c55e);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #cbd5f5;
        opacity: 0.85;
        margin-bottom: 1.0rem;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.94), rgba(15,23,42,0.78));
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        border: 1px solid rgba(148,163,184,0.35);
        box-shadow:
            0 16px 30px rgba(15,23,42,0.8),
            0 0 0 1px rgba(148,163,184,0.12);
        backdrop-filter: blur(16px);
        margin-bottom: 1.1rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #9ca3ff;
        margin-bottom: 0.4rem;
    }

    .score-card {
        min-width: 150px;
        padding: 0.7rem 0.9rem;
        border-radius: 14px;
        background: radial-gradient(circle at top left, rgba(249,115,22,0.20), rgba(15,23,42,0.96));
        border: 1px solid rgba(248,250,252,0.12);
        box-shadow: 0 10px 22px rgba(0,0,0,0.45);
        margin-bottom: 0.6rem;
    }
    .score-name {
        font-size: 0.86rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #e5e7eb;
        opacity: 0.85;
        margin-bottom: 0.15rem;
    }
    .score-points {
        font-size: 1.6rem;
        font-weight: 800;
        color: #facc15;
    }

    .stTable thead tr th {
        background: rgba(15,23,42,0.9) !important;
        color: #e5e7eb !important;
    }

    .stButton>button {
        border-radius: 999px;
        padding: 0.5rem 1.4rem;
        border: 1px solid rgba(248,250,252,0.16);
        background: linear-gradient(135deg, #f97316, #eab308);
        color: #111827;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 12px 25px rgba(234,179,8,0.5);
    }
    .stButton>button:hover {
        filter: brightness(1.05);
        transform: translateY(-1px);
    }

    .stNumberInput input,
    .stSelectbox div[role="combobox"] {
        background: rgba(15,23,42,0.92) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(148,163,184,0.7) !important;
        color: #e5e7eb !important;
    }

    /* dropdown selectbox dark */
    div[data-baseweb="select"] > div {
        background-color: rgba(15,23,42,0.92) !important;
        color: #e5e7eb !important;
    }
    div[data-baseweb="popover"] {
        background-color: #020617 !important;
        color: #e5e7eb !important;
        border-radius: 12px !important;
        border: 1px solid rgba(148,163,184,0.7) !important;
    }
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] li {
        background-color: #020617 !important;
        color: #e5e7eb !important;
    }
    div[data-baseweb="popover"] [role="option"][aria-selected="true"],
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #1f2937 !important;
    }
    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="popover"] li:hover {
        background-color: #111827 !important;
    }

    .info-badge {
        display:inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        background: rgba(56,189,248,0.1);
        border: 1px solid rgba(56,189,248,0.4);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: .08em;
        color: #7dd3fc;
        margin-left: 0.3rem;
    }

    .progress-label {
        font-size: 0.85rem;
        color: #cbd5f5;
        margin-bottom: 0.3rem;
    }

    .question-card {
        margin: 0.9rem auto 0.4rem auto;
        max-width: 900px;
        text-align: center;
        padding: 1.6rem 2.2rem;
        border-radius: 22px;
        background: radial-gradient(circle at top, rgba(59,130,246,0.25), rgba(15,23,42,0.96));
        border: 1px solid rgba(129,140,248,0.65);
        box-shadow: 0 20px 40px rgba(15,23,42,0.9);
    }
    .question-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #a5b4fc;
    }
    .question-main {
        font-size: 1.9rem;
        font-weight: 800;
        margin-top: 0.35rem;
        color: #e5e7ff;
    }
    .question-base {
        margin-top: 0.65rem;
        font-size: 1.05rem;
        color: #e5e7eb;
    }
    .question-base-pill {
        display:inline-block;
        margin-left:0.35rem;
        padding:0.2rem 0.9rem;
        border-radius:999px;
        background:linear-gradient(135deg,#22c55e,#a3e635);
        color:#0f172a;
        font-weight:700;
    }

    /* Tombol HAPUS BID: pure icon, no background */
    div[class^="st-key-del_bid_"] button,
    div[class*=" st-key-del_bid_"] button {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        color: #ffffff !important;
        font-size: 20px !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
    }
    div[class^="st-key-del_bid_"] button:hover,
    div[class*=" st-key-del_bid_"] button:hover {
        background: transparent !important;
        color: #ffffff !important;
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# CLASS / DB HELPERS
# ----------------------------------------------------
def class_label_to_safe(label: str) -> str:
    label = (label or "").strip()
    if not label:
        return "default"
    safe = "".join(c if c.isalnum() else "_" for c in label)
    return safe or "default"


def safe_to_label(safe: str) -> str:
    if safe == "default":
        return "Default"
    return safe.replace("_", " ")


def list_existing_classes():
    files = glob.glob("auction_*.db")
    labels = []
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]  # auction_xxx
        if not base.startswith("auction_"):
            continue
        safe = base[len("auction_") :]
        labels.append(safe_to_label(safe))
    return sorted(set(labels))


def get_db_path():
    cls = st.session_state.get("current_class_name", "").strip()
    safe = class_label_to_safe(cls)
    return f"auction_{safe}.db"


# ----------------------------------------------------
# DB FUNCTIONS
# ----------------------------------------------------
def init_db(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            initial_points INTEGER
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_index INTEGER,
            question TEXT,
            base_cost INTEGER
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_index INTEGER,
            group_name TEXT,
            bid INTEGER,
            ts TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_index INTEGER,
            group_name TEXT,
            bid INTEGER,
            ts TEXT
        )
        """
    )
    conn.commit()
    return conn


def get_db_conn():
    db_path = get_db_path()
    if "db_conn" not in st.session_state:
        st.session_state.db_conn = init_db(db_path)
    return st.session_state.db_conn


def load_groups_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT name, initial_points FROM groups ORDER BY id")
    rows = c.fetchall()
    return [{"name": r[0], "initial_points": r[1]} for r in rows]


def save_groups_to_db(groups, conn):
    c = conn.cursor()
    c.execute("DELETE FROM groups")
    c.execute("DELETE FROM bids")
    c.execute("DELETE FROM winners")
    for g in groups:
        c.execute(
            "INSERT INTO groups (name, initial_points) VALUES (?, ?)",
            (g["name"], int(g.get("initial_points", 0))),
        )
    conn.commit()


def load_questions_from_db(conn):
    c = conn.cursor()
    c.execute(
        "SELECT question_index, question, base_cost FROM questions ORDER BY question_index"
    )
    rows = c.fetchall()
    return [{"question": r[1], "base_cost": r[2]} for r in rows]


def save_questions_to_db(questions, conn):
    c = conn.cursor()
    c.execute("DELETE FROM questions")
    c.execute("DELETE FROM bids")
    c.execute("DELETE FROM winners")
    for idx, q in enumerate(questions):
        c.execute(
            "INSERT INTO questions (question_index, question, base_cost) VALUES (?, ?, ?)",
            (idx, q["question"], int(q.get("base_cost", 0))),
        )
    conn.commit()


def save_bid_to_db(question_index, group_name, bid, conn):
    c = conn.cursor()
    c.execute(
        "INSERT INTO bids (question_index, group_name, bid, ts) VALUES (?, ?, ?, ?)",
        (question_index, group_name, bid, datetime.utcnow().isoformat()),
    )
    conn.commit()


def delete_bids_for_group(question_index, group_name, conn):
    c = conn.cursor()
    c.execute(
        "DELETE FROM bids WHERE question_index = ? AND group_name = ?",
        (question_index, group_name),
    )
    conn.commit()


def delete_all_bids_for_question(question_index, conn):
    c = conn.cursor()
    c.execute("DELETE FROM bids WHERE question_index = ?", (question_index,))
    conn.commit()


def save_winner_to_db(question_index, group_name, bid, conn):
    c = conn.cursor()
    c.execute(
        "INSERT INTO winners (question_index, group_name, bid, ts) VALUES (?, ?, ?, ?)",
        (question_index, group_name, bid, datetime.utcnow().isoformat()),
    )
    conn.commit()


def load_winners_from_db(conn):
    c = conn.cursor()
    c.execute(
        "SELECT question_index, group_name, bid FROM winners ORDER BY question_index"
    )
    rows = c.fetchall()
    return [{"question_index": r[0], "winner_group": r[1], "bid": r[2]} for r in rows]


def compute_scores_from_db(conn):
    groups = load_groups_from_db(conn)
    scores = {g["name"]: g["initial_points"] for g in groups}
    c = conn.cursor()
    c.execute("SELECT group_name, SUM(bid) FROM winners GROUP BY group_name")
    for name, total in c.fetchall():
        if name in scores and total is not None:
            scores[name] -= total
    return scores


def get_current_q_index_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT MAX(question_index) FROM winners")
    row = c.fetchone()
    if row is None or row[0] is None:
        return 0
    return row[0] + 1


def load_current_bids_for_question(question_index, conn):
    c = conn.cursor()
    c.execute(
        """
        SELECT group_name, MAX(bid) as max_bid
        FROM bids
        WHERE question_index = ?
        GROUP BY group_name
        """,
        (question_index,),
    )
    rows = c.fetchall()
    return [{"group": r[0], "bid": r[1]} for r in rows]


def get_max_bid_for_group(question_index, group_name, conn):
    c = conn.cursor()
    c.execute(
        "SELECT MAX(bid) FROM bids WHERE question_index = ? AND group_name = ?",
        (question_index, group_name),
    )
    row = c.fetchone()
    return row[0] if row and row[0] is not None else None


# ----------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------
if "groups" not in st.session_state:
    st.session_state.groups = []
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "current_bids" not in st.session_state:
    st.session_state.current_bids = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "show_clear_confirm" not in st.session_state:
    st.session_state.show_clear_confirm = False
if "confirm_delete_class" not in st.session_state:
    st.session_state.confirm_delete_class = None

# ----------------------------------------------------
# SIDEBAR: CLASS SELECTION & MANAGEMENT
# ----------------------------------------------------
st.sidebar.title("🏫 Kelas")

existing_classes = list_existing_classes()
current_class = st.session_state.get("current_class_name", "")

if existing_classes:
    options = ["(Kelas baru)"] + existing_classes
    default_index = 0
    if current_class and current_class in existing_classes:
        default_index = existing_classes.index(current_class) + 1

    selected = st.sidebar.selectbox(
        "Pilih kelas tersimpan:",
        options,
        index=default_index,
    )

    if selected == "(Kelas baru)":
        class_input = st.sidebar.text_input(
            "Nama kelas baru:",
            value=current_class,
            placeholder="Misal: IF401 Pagi",
        )
    else:
        class_input = selected
else:
    class_input = st.sidebar.text_input(
        "Nama kelas:",
        value=current_class,
        placeholder="Misal: IF401 Pagi",
    )

# ganti kelas -> reset koneksi & init ulang
if class_input != current_class:
    st.session_state["current_class_name"] = class_input.strip()
    if "db_conn" in st.session_state:
        try:
            st.session_state["db_conn"].close()
        except Exception:
            pass
        del st.session_state["db_conn"]
    st.session_state.pop("initialized_from_db", None)
    st.rerun()

# Kelola kelas (rename / delete)
st.sidebar.markdown("### Kelola kelas")
if existing_classes:
    manage_selected = st.sidebar.selectbox(
        "Pilih kelas untuk diubah / hapus",
        existing_classes,
        key="manage_class_select",
    )

    new_name = st.sidebar.text_input(
        "Nama baru untuk kelas ini:",
        value=manage_selected,
        key="manage_class_name",
    )

    col_m1, col_m2 = st.sidebar.columns(2)
    with col_m1:
        if st.button("💾 Rename kelas"):
            old_safe = class_label_to_safe(manage_selected)
            new_safe = class_label_to_safe(new_name)
            old_path = f"auction_{old_safe}.db"
            new_path = f"auction_{new_safe}.db"
            if old_path != new_path and os.path.exists(new_path):
                st.sidebar.error("Nama kelas baru sudah dipakai kelas lain.")
            else:
                try:
                    os.rename(old_path, new_path)
                except FileNotFoundError:
                    st.sidebar.error("File DB kelas lama tidak ditemukan.")
                else:
                    if st.session_state.get("current_class_name", "") == manage_selected:
                        st.session_state["current_class_name"] = new_name
                        if "db_conn" in st.session_state:
                            try:
                                st.session_state["db_conn"].close()
                            except Exception:
                                pass
                            del st.session_state["db_conn"]
                        st.session_state.pop("initialized_from_db", None)
                    st.sidebar.success("Nama kelas berhasil diubah.")
                    st.rerun()

    with col_m2:
        if st.button("🗑 Hapus kelas ini"):
            st.session_state.confirm_delete_class = manage_selected

    if st.session_state.confirm_delete_class:
        del_name = st.session_state.confirm_delete_class
        st.sidebar.warning(
            f"Yakin ingin menghapus kelas '{del_name}'? "
            "Semua data bid & pemenang untuk kelas ini akan hilang."
        )
        c1, c2 = st.sidebar.columns(2)
        with c1:
            if st.button("✅ Ya, hapus", key="confirm_delete_yes"):
                safe = class_label_to_safe(del_name)
                path = f"auction_{safe}.db"
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception as e:
                    st.sidebar.error(f"Gagal menghapus file DB: {e}")
                else:
                    if st.session_state.get("current_class_name", "") == del_name:
                        st.session_state["current_class_name"] = ""
                        if "db_conn" in st.session_state:
                            try:
                                st.session_state["db_conn"].close()
                            except Exception:
                                pass
                            del st.session_state["db_conn"]
                        st.session_state.pop("initialized_from_db", None)
                    st.sidebar.success(f"Kelas '{del_name}' dihapus.")
                st.session_state.confirm_delete_class = None
                st.rerun()
        with c2:
            if st.button("❌ Batal", key="confirm_delete_no"):
                st.session_state.confirm_delete_class = None

mode = st.sidebar.radio("🎮 Mode Game", ["Setup", "Auction", "Jawaban Kelompok"])
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Tips:**\n"
    "- Set / pilih kelas di atas\n"
    "- Atur kelompok & pertanyaan di *Setup*\n"
    "- Gunakan *Auction* saat bidding berlangsung\n"
    "- Lihat rincian tugas jawaban di *Jawaban Kelompok*"
)

# ----------------------------------------------------
# DB CONNECTION & FIRST LOAD
# ----------------------------------------------------
conn = get_db_conn()

if "initialized_from_db" not in st.session_state:
    st.session_state.groups = load_groups_from_db(conn)
    st.session_state.questions = load_questions_from_db(conn)
    st.session_state.winners = load_winners_from_db(conn)
    st.session_state.scores = compute_scores_from_db(conn)

    if st.session_state.questions:
        st.session_state.current_q_idx = get_current_q_index_from_db(conn)
    else:
        st.session_state.current_q_idx = 0

    if (
        st.session_state.questions
        and st.session_state.current_q_idx < len(st.session_state.questions)
    ):
        st.session_state.current_bids = load_current_bids_for_question(
            st.session_state.current_q_idx, conn
        )
    else:
        st.session_state.current_bids = []

    st.session_state.initialized_from_db = True


def reset_auction_state_from_db():
    st.session_state.scores = compute_scores_from_db(conn)
    st.session_state.winners = load_winners_from_db(conn)
    st.session_state.current_q_idx = 0
    if st.session_state.questions:
        st.session_state.current_bids = load_current_bids_for_question(0, conn)
    else:
        st.session_state.current_bids = []
    st.session_state.show_clear_confirm = False


def get_highest_bid():
    if not st.session_state.current_bids:
        return None
    return max(st.session_state.current_bids, key=lambda x: x["bid"])


def upsert_bid(group_name, bid_value):
    for b in st.session_state.current_bids:
        if b["group"] == group_name:
            b["bid"] = bid_value
            return
    st.session_state.current_bids.append({"group": group_name, "bid": bid_value})


# ----------------------------------------------------
# HERO HEADER
# ----------------------------------------------------
st.markdown(
    """
    <div class="glass-card" style="margin-bottom: 1.2rem;">
        <div class="hero-title">Digital Question Auction Arena</div>
        <div class="hero-subtitle">
            Kelompok mengelola poin, melakukan bidding, dan merebut hak menjawab pertanyaan.
            Cocok untuk kelas interaktif & diskusi yang rame tapi terstruktur.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
#                       MODE SETUP
# =========================================================
if mode == "Setup":
    col_left, col_right = st.columns([1.1, 1])

    # ---------- Kelompok ----------
    with col_left:
        st.markdown(
            '<div class="section-title">Pengaturan Kelompok</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        num_groups = st.number_input(
            "Jumlah kelompok (untuk generate default)",
            min_value=1,
            max_value=30,
            value=len(st.session_state.groups) if st.session_state.groups else 4,
            step=1,
        )

        default_points = st.number_input(
            "Default initial point per kelompok (bisa diubah per kelompok nanti)",
            min_value=0,
            value=100,
            step=5,
        )

        if st.button("🎲 Generate kelompok default"):
            st.session_state.groups = [
                {"name": f"Kelompok {i+1}", "initial_points": default_points}
                for i in range(num_groups)
            ]
            save_groups_to_db(st.session_state.groups, conn)
            reset_auction_state_from_db()
            st.success("Kelompok default dibuat & disimpan ke DB. Silakan edit jika perlu.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown(
            '<div class="section-title">Edit Nama & Poin Awal</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if not st.session_state.groups:
            st.info("Belum ada kelompok. Klik **Generate kelompok default** di atas dulu.")

        groups_df = pd.DataFrame(
            st.session_state.groups
            or [{"name": "Kelompok 1", "initial_points": default_points}]
        )
        edited_groups_df = st.data_editor(
            groups_df,
            num_rows="dynamic",
            key="groups_editor",
            use_container_width=True,
        )

        if st.button("💾 Simpan pengaturan kelompok"):
            new_groups = []
            for _, row in edited_groups_df.iterrows():
                name = str(row.get("name", "")).strip()
                if name:
                    pts = int(row.get("initial_points", 0))
                    new_groups.append({"name": name, "initial_points": pts})
            st.session_state.groups = new_groups
            save_groups_to_db(new_groups, conn)
            reset_auction_state_from_db()
            st.success("Kelompok & poin awal disimpan ke DB. Auction di-reset.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Pertanyaan ----------
    with col_right:
        st.markdown(
            '<div class="section-title">Daftar Pertanyaan</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if not st.session_state.questions:
            st.session_state.questions = [
                {"question": "Jelaskan konsep utama materi hari ini.", "base_cost": 10},
                {"question": "Berikan contoh penerapan konsep ini di dunia nyata.", "base_cost": 15},
            ]

        questions_df = pd.DataFrame(st.session_state.questions)
        edited_q_df = st.data_editor(
            questions_df,
            num_rows="dynamic",
            key="questions_editor",
            use_container_width=True,
        )

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("💾 Simpan daftar pertanyaan (manual)"):
                new_questions = []
                for _, row in edited_q_df.iterrows():
                    qtext = str(row.get("question", "")).strip()
                    if qtext:
                        try:
                            cost = int(row.get("base_cost", 0))
                        except Exception:
                            cost = 0
                        new_questions.append({"question": qtext, "base_cost": cost})
                st.session_state.questions = new_questions
                save_questions_to_db(new_questions, conn)
                reset_auction_state_from_db()
                st.success("Pertanyaan disimpan ke DB & auction kembali ke awal.")

        with col_q2:
            if st.button("🔁 Reset poin & posisi auction (config tetap)"):
                c = conn.cursor()
                c.execute("DELETE FROM bids")
                c.execute("DELETE FROM winners")
                conn.commit()
                reset_auction_state_from_db()
                st.success("Poin & posisi auction di-reset. Config kelompok/pertanyaan tetap.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown(
            '<div class="section-title">Import Pertanyaan dari Excel</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload file Excel dengan kolom: question, base_cost",
            type=["xlsx", "xls"],
        )
        if uploaded is not None:
            df_import = pd.read_excel(uploaded)
            st.write("Preview data:")
            st.dataframe(df_import.head())

            if st.button("📥 Gunakan data dari Excel ini"):
                if "question" not in df_import.columns or "base_cost" not in df_import.columns:
                    st.error("File harus punya kolom 'question' dan 'base_cost'.")
                else:
                    new_questions = []
                    for _, row in df_import.iterrows():
                        qtext = str(row["question"]).strip()
                        if qtext:
                            try:
                                cost = int(row["base_cost"])
                            except Exception:
                                cost = 0
                            new_questions.append({"question": qtext, "base_cost": cost})
                    st.session_state.questions = new_questions
                    save_questions_to_db(new_questions, conn)
                    reset_auction_state_from_db()
                    st.success("Pertanyaan dari Excel disimpan ke DB & siap di-auction.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Ringkasan
        st.markdown("")
        st.markdown(
            '<div class="section-title">Ringkasan</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Kelompok:**")
            if st.session_state.groups:
                st.table(pd.DataFrame(st.session_state.groups))
            else:
                st.write("Belum ada kelompok.")
        with col_b:
            st.markdown("**Pertanyaan:**")
            if st.session_state.questions:
                st.table(pd.DataFrame(st.session_state.questions))
            else:
                st.write("Belum ada pertanyaan.")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
#                       MODE AUCTION
# =========================================================
elif mode == "Auction":
    if not st.session_state.groups or not st.session_state.questions:
        st.error("Kelompok atau pertanyaan belum diset. Masuk ke mode **Setup** dulu.")
        st.stop()

    st.session_state.scores = compute_scores_from_db(conn)

    # ---------- SCOREBOARD ----------
    st.markdown(
        '<div class="section-title">Scoreboard Kelompok <span class="info-badge">Live</span></div>',
        unsafe_allow_html=True,
    )

    groups_in_order = load_groups_from_db(conn)
    scores_dict = st.session_state.scores
    score_items = [
        {"name": g["name"], "points": scores_dict.get(g["name"], g["initial_points"])}
        for g in groups_in_order
    ]

    n = len(score_items)
    if n == 0:
        st.write("Belum ada kelompok.")
    else:
        if n <= 7:
            cols = st.columns(n)
            for i, item in enumerate(score_items):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-name">{item['name']}</div>
                            <div class="score-points">{item['points']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            top_count = (n + 1) // 2
            bottom_count = n - top_count
            top_items = score_items[:top_count]
            bottom_items = score_items[top_count:]

            cols_top = st.columns(len(top_items))
            for i, item in enumerate(top_items):
                with cols_top[i]:
                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-name">{item['name']}</div>
                            <div class="score-points">{item['points']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            cols_bottom = st.columns(len(bottom_items))
            for i, item in enumerate(bottom_items):
                with cols_bottom[i]:
                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-name">{item['name']}</div>
                            <div class="score-points">{item['points']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.markdown("")

    # ---------- CURRENT QUESTION ----------
    idx = st.session_state.current_q_idx
    total_q = len(st.session_state.questions)

    # sync current_bids dari DB setiap rerun
    if idx < total_q:
        st.session_state.current_bids = load_current_bids_for_question(idx, conn)
    else:
        st.session_state.current_bids = []

    if idx >= total_q:
        st.success("🎉 Semua pertanyaan sudah selesai di-auction.")
        st.markdown(
            '<div class="section-title">Rekap Pemenang</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        winners_db = load_winners_from_db(conn)
        if winners_db:
            rows = []
            for i, w in enumerate(winners_db, start=1):
                q_idx = w["question_index"]
                q_text = (
                    st.session_state.questions[q_idx]["question"]
                    if q_idx < len(st.session_state.questions)
                    else "(Pertanyaan tidak ditemukan)"
                )
                rows.append(
                    {
                        "No": i,
                        "Pertanyaan": q_text,
                        "Pemenang": w["winner_group"],
                        "Bid": w["bid"],
                    }
                )
            df = pd.DataFrame(rows)
            st.dataframe(
                df.style.set_properties(
                    subset=["No", "Pemenang", "Bid"], **{"text-align": "center"}
                ).set_properties(
                    subset=["Pertanyaan"],
                    **{"text-align": "left", "white-space": "normal"},
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("Belum ada pemenang.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    current_q = st.session_state.questions[idx]

    st.markdown(
        '<div class="section-title">Pertanyaan Berjalan</div>',
        unsafe_allow_html=True,
    )

    progress = (idx + 1) / total_q
    st.markdown(
        f'<div class="progress-label">Pertanyaan {idx+1} dari {total_q}</div>',
        unsafe_allow_html=True,
    )
    st.progress(progress)

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">PERTANYAAN AKTIF</div>
            <div class="question-main">{current_q['question']}</div>
            <div class="question-base">
                Biaya awal (minimum bid):
                <span class="question-base-pill">{current_q['base_cost']} poin</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ---------- AUCTION AREA ----------
    col_bid, col_table = st.columns([1.4, 1])

    with col_bid:
        st.markdown(
            '<div class="section-title">Auction: Input Bid</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        group_names = [g["name"] for g in st.session_state.groups]
        selected_group = st.selectbox("Pilih kelompok yang akan bid:", group_names)

        max_points_group = st.session_state.scores.get(selected_group, 0)
        base_cost = int(current_q.get("base_cost", 0))

        bid_value = st.number_input(
            f"Masukkan nilai bid (min {base_cost}, max {max_points_group}):",
            min_value=0,
            value=base_cost if max_points_group >= base_cost else max_points_group,
            step=1,
        )

        if st.button("💰 Simpan / Update Bid untuk Kelompok Ini"):
            prev_bid = get_max_bid_for_group(idx, selected_group, conn)

            if max_points_group <= 0:
                st.warning(f"{selected_group} tidak punya poin untuk bid.")
            elif bid_value < base_cost:
                st.warning(f"Bid harus minimal {base_cost} poin.")
            elif bid_value > max_points_group:
                st.warning(
                    f"Bid tidak boleh melebihi poin yang dimiliki ({max_points_group})."
                )
            elif prev_bid is not None and bid_value <= prev_bid:
                st.warning(
                    f"Bid baru harus lebih besar dari bid sebelumnya untuk {selected_group} "
                    f"({prev_bid} poin)."
                )
            else:
                upsert_bid(selected_group, int(bid_value))
                save_bid_to_db(idx, selected_group, int(bid_value), conn)
                st.success(
                    f"Bid {bid_value} poin disimpan untuk {selected_group} "
                    f"(juga tercatat di DB sebagai history)."
                )

        st.markdown("---")
        if st.button("🧹 Clear semua bid untuk pertanyaan ini"):
            st.session_state.show_clear_confirm = True

        if st.session_state.show_clear_confirm:
            st.warning(
                "Yakin mau menghapus **semua bid** untuk pertanyaan ini? "
                "Tindakan ini tidak bisa dibatalkan."
            )
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("✅ Ya, hapus semua", key="confirm_clear_yes"):
                    st.session_state.current_bids = []
                    delete_all_bids_for_question(idx, conn)
                    st.session_state.show_clear_confirm = False
                    st.rerun()
            with cc2:
                if st.button("❌ Batal", key="confirm_clear_no"):
                    st.session_state.show_clear_confirm = False

        st.markdown("</div>", unsafe_allow_html=True)

    with col_table:
        st.markdown(
            '<div class="section-title">Bid Saat Ini</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if not st.session_state.current_bids:
            st.info("Belum ada bid untuk pertanyaan ini.")
        else:
            sorted_bids = sorted(
                st.session_state.current_bids,
                key=lambda x: x["bid"],
                reverse=True,
            )

            st.markdown("**Daftar Bid:**")
            for idx_row, b in enumerate(sorted_bids):
                c_g, c_b, c_del = st.columns([3, 2, 1])
                with c_g:
                    st.write(b["group"])
                with c_b:
                    st.write(f"{b['bid']} poin")
                with c_del:
                    if st.button(
                        "🗑", key=f"del_bid_{idx}_{idx_row}", help="Hapus bid grup ini"
                    ):
                        st.session_state.current_bids = [
                            bb
                            for bb in st.session_state.current_bids
                            if bb["group"] != b["group"]
                        ]
                        delete_bids_for_group(idx, b["group"], conn)
                        st.rerun()

            highest = get_highest_bid()
            if highest:
                st.markdown(
                    f"🔥 <b>Bid tertinggi sementara:</b> {highest['group']} "
                    f"dengan <b>{highest['bid']} poin</b>",
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    # ---------- CONFIRM WINNER ----------
    st.markdown(
        '<div class="section-title">Tutup Auction & Tetapkan Pemenang</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    if st.button("✅ Tutup Auction Pertanyaan Ini & Tetapkan Pemenang"):
        if not st.session_state.current_bids:
            st.warning("Belum ada bid. Tidak bisa menentukan pemenang.")
        else:
            highest = get_highest_bid()
            winner_group = highest["group"]
            bid_amount = highest["bid"]

            save_winner_to_db(idx, winner_group, bid_amount, conn)

            st.session_state.scores = compute_scores_from_db(conn)
            st.session_state.winners = load_winners_from_db(conn)

            st.success(
                f"Pemenang pertanyaan {idx+1}: **{winner_group}** dengan bid **{bid_amount}** poin."
            )
            st.info(
                f"Sisa poin {winner_group}: {st.session_state.scores[winner_group]} poin."
            )

            st.session_state.current_q_idx += 1
            st.session_state.current_bids = []
            st.session_state.show_clear_confirm = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- HISTORY (REKAP SEMENTARA) ----------
    st.markdown("")
    st.markdown(
        '<div class="section-title">Rekap Pemenang Sementara</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    winners_db = load_winners_from_db(conn)
    if winners_db:
        rows = []
        for i, w in enumerate(winners_db, start=1):
            q_idx = w["question_index"]
            q_text = (
                st.session_state.questions[q_idx]["question"]
                if q_idx < len(st.session_state.questions)
                else "(Pertanyaan tidak ditemukan)"
            )
            rows.append(
                {
                    "No": i,
                    "Pertanyaan": q_text,
                    "Pemenang": w["winner_group"],
                    "Bid": w["bid"],
                }
            )
        df = pd.DataFrame(rows)
        st.dataframe(
            df.style.set_properties(
                subset=["No", "Pemenang", "Bid"], **{"text-align": "center"}
            ).set_properties(
                subset=["Pertanyaan"],
                **{"text-align": "left", "white-space": "normal"},
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.write("Belum ada pertanyaan yang selesai di-auction.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
#                MODE JAWABAN KELOMPOK (VIEW ONLY)
# =========================================================
else:  # Jawaban Kelompok
    if not st.session_state.groups or not st.session_state.questions:
        st.error("Kelompok atau pertanyaan belum diset. Masuk ke mode **Setup** dulu.")
        st.stop()

    st.session_state.scores = compute_scores_from_db(conn)
    winners_db = load_winners_from_db(conn)

    st.markdown(
        '<div class="section-title">Rangkuman Tugas Jawaban per Kelompok</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="glass-card">
            Halaman ini menampilkan daftar pertanyaan yang dimenangkan tiap kelompok,
            lengkap dengan nilai bid yang sudah mereka keluarkan. Cocok ditampilkan
            setelah sesi auction selesai, saat kelompok mulai menyusun jawaban.
        </div>
        """,
        unsafe_allow_html=True,
    )

    groups_in_order = load_groups_from_db(conn)
    scores_dict = st.session_state.scores

    # ---------- Summary card ----------
    st.markdown(
        '<div class="section-title">Ringkasan Singkat</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    summary_rows = []
    for g in groups_in_order:
        name = g["name"]
        won = [w for w in winners_db if w["winner_group"] == name]
        total_bid = sum(w["bid"] for w in won)
        remaining = scores_dict.get(name, g["initial_points"])
        summary_rows.append(
            {
                "Kelompok": name,
                "Jumlah Pertanyaan": len(won),
                "Total Bid": total_bid,
                "Sisa Poin": remaining,
            }
        )

    if summary_rows:
        df_sum = pd.DataFrame(summary_rows)
        st.dataframe(
            df_sum.style.set_properties(
                subset=["Jumlah Pertanyaan", "Total Bid", "Sisa Poin"],
                **{"text-align": "center"},
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Belum ada pemenang. Jalankan auction terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Detail per group ----------
    st.markdown(
        '<div class="section-title">Detail Pertanyaan per Kelompok</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="glass-card" style="padding-bottom: 0.6rem;">
            Gunakan tab di bawah untuk melihat daftar pertanyaan yang harus dijawab
            masing-masing kelompok.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not winners_db:
        st.info("Belum ada data pemenang untuk ditampilkan.")
        st.stop()

    tab_labels = [g["name"] for g in groups_in_order]
    tabs = st.tabs(tab_labels)

    for tab, group in zip(tabs, groups_in_order):
        name = group["name"]
        with tab:
            st.markdown(
                f'<div class="section-title">Kelompok: {name}</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            wins = [w for w in winners_db if w["winner_group"] == name]

            if not wins:
                st.info("Kelompok ini belum memenangkan pertanyaan apa pun.")
            else:
                rows = []
                for i, w in enumerate(wins, start=1):
                    q_idx = w["question_index"]
                    q_text = (
                        st.session_state.questions[q_idx]["question"]
                        if q_idx < len(st.session_state.questions)
                        else "(Pertanyaan tidak ditemukan)"
                    )
                    rows.append(
                        {
                            "No": i,
                            "Pertanyaan": q_text,
                            "Bid": w["bid"],
                        }
                    )
                df = pd.DataFrame(rows)
                st.dataframe(
                    df.style.set_properties(
                        subset=["No", "Bid"], **{"text-align": "center"}
                    ).set_properties(
                        subset=["Pertanyaan"],
                        **{"text-align": "left", "white-space": "normal"},
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
