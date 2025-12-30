import streamlit as st
import random

st.set_page_config(page_title="රූප ප්‍රහේලිකා අභියෝගය", layout="wide")

# CSS - රූප කැබලි සහ පෙනුම සැකසීමට
st.markdown("""
    <style>
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 2px;
        width: 480px;
        margin: auto;
        border: 5px solid #333;
        background-color: #f0f0f0;
    }
    .tile {
        width: 80px;
        height: 80px;
        background-color: #bdc3c7; /* නොවිසඳූ කොටස් අළු පාටයි */
        border: 0.1px solid #eee;
        background-size: 480px 480px; /* රූපයේ මුළු ප්‍රමාණය */
    }
    .question-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# රූපයේ URL එක (ඔබට කැමති රූපයක් මෙතැනට දැමිය හැක)
img_url = "https://images.unsplash.com/photo-1501854140801-50d01674af3e?w=480&h=480&fit=crop"

def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ප්‍රශ්න සහ බහුවරණ පිළිතුරු 36ක්
if 'puzzle_data' not in st.session_state:
    questions = []
    for i in range(1, 37):
        a, b = random.randint(1, 12), random.randint(1, 12)
        correct = a * b
        wrong = random.sample([x for x in range(1, 144) if x != correct], 3)
        options = wrong + [correct]
        random.shuffle(options)
        questions.append({"q": f"{a} x {b} කීයද?", "options": options, "ans": correct})
    
    st.session_state.puzzle_data = questions
    st.session_state.solved_tiles = [] # විසඳූ කොටු ලැයිස්තුව
    st.session_state.current_tile = None

st.title("🧩 රූප කැබලි ගළපන ප්‍රහේලිකාව")
st.write("අංකයක් තෝරා ප්‍රශ්නයට පිළිතුරු දී රූපය සම්පූර්ණ කරන්න!")

# වම සහ දකුණ ලෙස කොටස් දෙකකට බෙදීම
col1, col2 = st.columns([1, 1])

with col1:
    # Puzzle Grid එක නිර්මාණය
    html_grid = '<div class="puzzle-grid">'
    for i in range(36):
        row = i // 6
        col = i % 6
        pos_x = col * 80
        pos_y = row * 80
        
        if i in st.session_state.solved_tiles:
            # විසඳූ කොටු සඳහා රූපයේ කොටස පෙන්වීම
            html_grid += f'<div class="tile" style="background-image: url(\'{img_url}\'); background-position: -{pos_x}px -{pos_y}px; background-color: transparent;"></div>'
        else:
            # නොවිසඳූ කොටු සඳහා අංකය පෙන්වීම
            html_grid += f'<div class="tile" style="display:flex; align-items:center; justify-content:center; font-weight:bold; color:#7f8c8d;">{i+1}</div>'
    html_grid += '</div>'
    st.markdown(html_grid, unsafe_allow_html=True)

with col2:
    # අංක තේරීමේ බොත්තම්
    st.write("### කැබැල්ලක් තෝරන්න:")
    tile_cols = st.columns(6)
    for i in range(36):
        with tile_cols[i % 6]:
            if i not in st.session_state.solved_tiles:
                if st.button(f"{i+1}", key=f"btn_{i}"):
                    st.session_state.current_tile = i
                    play_sound("https://www.soundjay.com/buttons/button-3.mp3")

    # ප්‍රශ්නය පෙන්වීම
    if st.session_state.current_tile is not None:
        idx = st.session_state.current_tile
        q_item = st.session_state.puzzle_data[idx]
        
        st.markdown(f"""
            <div class="question-card">
                <h4>අංක {idx+1} සඳහා ප්‍රශ්නය:</h4>
                <h2>{q_item['q']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # බහුවරණ පිළිතුරු (Radio Buttons)
        choice = st.radio("නිවැරදි පිළිතුර තෝරන්න:", q_item['options'], key=f"choice_{idx}", horizontal=True)
        
        if st.button("පිළිතුර තහවුරු කරන්න ✅"):
            if choice == q_item['ans']:
                st.session_state.solved_tiles.append(idx)
                st.session_state.current_tile = None
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.success("නිවැරදියි! රූප කැබැල්ල එකතු වුණා.")
                st.rerun()
            else:
                play_sound("https://www.soundjay.com/buttons/button-10.mp3")
                st.error("වැරදියි! නැවත උත්සාහ කරන්න.")

if len(st.session_state.solved_tiles) == 36:
    st.balloons()
    st.success("🎉 සුභ පැතුම්! ඔබ සම්පූර්ණ රූපයම නිම කළා!")
