import streamlit as st
import random

st.set_page_config(page_title="පිරිසිදු රූප ප්‍රහේලිකාව", layout="wide")

# CSS - Layout එක සහ අංක මැදට ගැනීමට
st.markdown("""
    <style>
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(6, 90px);
        grid-template-rows: repeat(6, 90px);
        gap: 2px;
        justify-content: center;
        background-color: #2c3e50;
        padding: 5px;
        border-radius: 8px;
        margin: auto;
        width: fit-content;
    }
    .tile {
        width: 90px;
        height: 90px;
        background-color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px; /* ඉලක්කම් වල ප්‍රමාණය */
        font-weight: bold;
        color: #34495e;
        border: 1px solid #dcdde1;
        box-sizing: border-box; /* ප්‍රමාණය වෙනස් වීම වැළැක්වීමට */
        line-height: 1; /* ඉලක්කම් ඉහළට යාම වැළැක්වීමට */
    }
    .solved-tile {
        background-size: 540px 540px; /* 90px * 6 = 540px */
        border: none !important;
        background-repeat: no-repeat;
    }
    .q-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #00a8ff;
    }
    </style>
""", unsafe_allow_html=True)

# රූපය සඳහා ඉතාමත් ස්ථාවර URL එකක් (Nature Image)
IMG_URL = "https://picsum.photos/id/10/540/540"

if 'solved' not in st.session_state:
    st.session_state.solved = []
    st.session_state.active = None
    # ප්‍රශ්න 36 ක් සකස් කිරීම
    q_data = []
    for i in range(1, 37):
        n1, n2 = random.randint(2, 9), random.randint(2, 9)
        ans = n1 * n2
        opts = random.sample([x for x in range(4, 100) if x != ans], 3) + [ans]
        random.shuffle(opts)
        q_data.append({"q": f"{n1} x {n2} කීයද?", "opts": opts, "ans": ans})
    st.session_state.q_data = q_data

st.markdown("<h1 style='text-align: center;'>🖼️ පිරිසිදු රූප ප්‍රහේලිකාව</h1>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])

with c1:
    # Puzzle Grid
    grid_html = '<div class="puzzle-grid">'
    for i in range(36):
        if i in st.session_state.solved:
            row, col = i // 6, i % 6
            x, y = col * 90, row * 90
            grid_html += f'<div class="tile solved-tile" style="background-image: url(\'{IMG_URL}\'); background-position: -{x}px -{y}px; background-color: transparent;"></div>'
        else:
            # ඉලක්කම් මැදට ගැනීමට tile class එක පමණක් ප්‍රමාණවත්
            grid_html += f'<div class="tile">{i+1}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

with c2:
    st.write("### අංකයක් තෝරන්න:")
    btns = st.columns(6)
    for i in range(36):
        with btns[i % 6]:
            if i not in st.session_state.solved:
                if st.button(f"{i+1}", key=f"b_{i}", use_container_width=True):
                    st.session_state.active = i

    if st.session_state.active is not None:
        idx = st.session_state.active
        item = st.session_state.q_data[idx]
        
        st.markdown(f"""
            <div class="q-container">
                <p style='color:gray;'>අංක {idx+1} ප්‍රහේලිකාව</p>
                <h2>{item['q']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        choice = st.radio("නිවැරදි පිළිතුර:", item['opts'], key=f"ans_{idx}", horizontal=True)
        
        if st.button("තහවුරු කරන්න", key="confirm"):
            if choice == item['ans']:
                st.session_state.solved.append(idx)
                st.session_state.active = None
                st.balloons()
                st.rerun()
            else:
                st.error("පිළිතුර වැරදියි!")

if len(st.session_state.solved) == 36:
    st.success("🎉 නියමයි! ඔබ රූපය සම්පූර්ණ කළා!")
