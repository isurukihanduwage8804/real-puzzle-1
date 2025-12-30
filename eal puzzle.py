import streamlit as st
import random

st.set_page_config(page_title="රූප ප්‍රහේලිකා අභියෝගය", layout="wide")

# CSS - රූපය සහ Layout එක ලස්සන කිරීමට
st.markdown("""
    <style>
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(6, 110px);
        grid-template-rows: repeat(6, 110px);
        gap: 2px;
        justify-content: center;
        background-color: #333;
        padding: 5px;
        border-radius: 10px;
        width: fit-content;
        margin: auto;
    }
    .tile {
        width: 110px;
        height: 110px;
        background-color: #ecf0f1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: #bdc3c7;
        border: 1px solid #ddd;
    }
    .solved-tile {
        background-size: 660px 660px; /* 110px * 6 = 660px */
        border: none;
    }
    .q-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 10px solid #6c5ce7;
    }
    </style>
""", unsafe_allow_html=True)

# වඩාත් ස්ථාවර රූපයක් භාවිතා කිරීම (උදා: ලස්සන සතෙකුගේ රූපයක්)
IMG_URL = "https://images.unsplash.com/photo-1555169062-013468b47731?q=80&w=660&h=660&auto=format&fit=crop"

def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

if 'solved_indices' not in st.session_state:
    st.session_state.solved_indices = []
    st.session_state.active_index = None
    # ප්‍රශ්න 36 ක් සකස් කිරීම
    questions = []
    for i in range(1, 37):
        a, b = random.randint(2, 12), random.randint(2, 12)
        ans = a * b
        opts = random.sample([x for x in range(4, 144) if x != ans], 3) + [ans]
        random.shuffle(opts)
        questions.append({"q": f"{a} x {b} කීයද?", "opts": opts, "ans": ans})
    st.session_state.questions = questions

st.title("🧩 රූප කැබලි මතුකරන ගණිත ප්‍රහේලිකාව")

col1, col2 = st.columns([1.2, 1])

with col1:
    # Puzzle Grid එක නිර්මාණය
    grid_html = '<div class="puzzle-grid">'
    for i in range(36):
        if i in st.session_state.solved_indices:
            row = i // 6
            col = i % 6
            x = col * 110
            y = row * 110
            grid_html += f'<div class="tile solved-tile" style="background-image: url(\'{IMG_URL}\'); background-position: -{x}px -{y}px;"></div>'
        else:
            grid_html += f'<div class="tile">{i+1}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

with col2:
    st.subheader("අංකයක් තෝරා ප්‍රශ්නයට පිළිතුරු දෙන්න:")
    
    # අංක 1-36 සඳහා බොත්තම්
    btn_cols = st.columns(6)
    for i in range(36):
        with btn_cols[i % 6]:
            if i not in st.session_state.solved_indices:
                if st.button(f"{i+1}", key=f"btn_{i}"):
                    st.session_state.active_index = i
                    play_sound("https://www.soundjay.com/buttons/button-3.mp3")

    if st.session_state.active_index is not None:
        idx = st.session_state.active_index
        q_item = st.session_state.questions[idx]
        
        st.markdown(f"""
            <div class="q-container">
                <h4>අංක {idx+1} ප්‍රශ්නය:</h4>
                <h1 style="color:#6c5ce7;">{q_item['q']}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        user_choice = st.radio("නිවැරදි පිළිතුර තෝරන්න:", q_item['opts'], key=f"rad_{idx}", horizontal=True)
        
        if st.button("පිළිතුර තහවුරු කරන්න", key="confirm"):
            if user_choice == q_item['ans']:
                st.session_state.solved_indices.append(idx)
                st.session_state.active_index = None
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.success("නිවැරදියි! රූපය මතු වුණා.")
                st.rerun()
            else:
                play_sound("https://www.soundjay.com/buttons/button-10.mp3")
                st.error("පිළිතුර වැරදියි. නැවත උත්සාහ කරන්න!")

if len(st.session_state.solved_indices) == 36:
    st.balloons()
    st.success("🎊 විශිෂ්ටයි! ඔබ රූපය සම්පූර්ණයෙන්ම මතු කළා!")
