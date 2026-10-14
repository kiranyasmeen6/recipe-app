import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(160deg, #FFF8F0 0%, #FFE3C4 100%);}
.block-container {position: relative; z-index: 1;}
.hero {background: linear-gradient(135deg, #E67E22, #F39C12); padding: 28px;
       border-radius: 18px; text-align: center; margin-bottom: 24px;
       box-shadow: 0 8px 24px rgba(230,126,34,0.35);}
.hero h1 {color: white; margin: 0;}
.hero p {color: white; margin: 6px 0 0 0;}
.wave {display: inline-block; animation: wave 2s ease-in-out infinite; transform-origin: 70% 80%;}
@keyframes wave {0%,100% {transform: rotate(0deg);} 25% {transform: rotate(14deg);} 75% {transform: rotate(-10deg);}}
[data-testid="stVerticalBlockBorderWrapper"] {background: rgba(255,255,255,0.65);
       backdrop-filter: blur(6px); border-radius: 16px;}
div.stButton > button {background: #E67E22; color: white; border: none; border-radius: 10px;
       padding: 0.6rem 1rem; font-weight: 600; width: 100%; transition: transform 0.15s;}
div.stButton > button:hover {background: #CF6D17; color: white; transform: scale(1.03);}
.float-bg {position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;}
.float-bg span {position: absolute; bottom: -60px; font-size: 36px; opacity: 0.2;
       animation: rise 16s linear infinite;}
@keyframes rise {from {transform: translateY(0) rotate(0deg);} to {transform: translateY(-115vh) rotate(360deg);}}
.chef {position: fixed; right: 22px; bottom: 14px; font-size: 84px; z-index: 2;
       pointer-events: none; animation: bob 2.6s ease-in-out infinite;}
@keyframes bob {0%,100% {transform: translateY(0) rotate(-5deg);} 50% {transform: translateY(-14px) rotate(5deg);}}
</style>
<div class="float-bg">
<span style="left:4%; animation-delay:0s">🍅</span>
<span style="left:16%; animation-delay:4s">🧀</span>
<span style="left:28%; animation-delay:8s">🥕</span>
<span style="left:42%; animation-delay:2s">🍳</span>
<span style="left:55%; animation-delay:6s">🌶️</span>
<span style="left:68%; animation-delay:10s">🥖</span>
<span style="left:80%; animation-delay:3s">🍋</span>
<span style="left:92%; animation-delay:7s">🥦</span>
</div>
<div class="chef">👨‍🍳</div>
<div class="hero">
<h1><span class="wave">👋</span> AI Recipe Generator</h1>
<p>Tell me what is in your kitchen, and our chef will cook up an idea.</p>
</div>
""", unsafe_allow_html=True)

EXAMPLES = {
    "🍳 Breakfast": "eggs, bread, butter, milk",
    "🍛 Dinner": "chicken, rice, onion, tomato",
    "🍰 Dessert": "milk, sugar, flour, butter",
}

def fill(text):
    st.session_state.ing = text

with st.sidebar:
    st.header("Settings")
    cuisine = st.selectbox("Cuisine", ["Any", "Pakistani", "Italian", "Chinese", "Fast food"])
    diet = st.selectbox("Diet", ["None", "Vegetarian", "Vegan", "High protein"])
    minutes = st.slider("Max cooking time (minutes)", 10, 90, 30)
    allergies = st.text_input("Allergies to avoid", placeholder="e.g. nuts, dairy")

left, right = st.columns([1, 1.3], gap="large")

with left:
    with st.container(border=True):
        st.subheader("Your ingredients")
        st.caption("Try an example:")
        cols = st.columns(3)
        for col, (name, text) in zip(cols, EXAMPLES.items()):
            col.button(name, on_click=fill, args=(text,))
        ingredients = st.text_area("Comma separated", key="ing", placeholder="eggs, rice, onion", height=130)
        go = st.button("✨ Generate Recipe")

if go:
    if go:
    if st.session_state.get("count", 0) >= 5:
        st.session_state.recipe = None
        st.error("You reached the free limit for this visit (5 recipes). Please come back later.")
    elif not ingredients.strip():
        st.session_state.recipe = None
        st.warning("Please enter at least one ingredient.")
    else:
        prompt = (f"You are a friendly chef. Create one recipe using mainly: {ingredients}. "
                  f"Cuisine: {cuisine}. Diet: {diet}. Max time: {minutes} minutes. "
                  f"Avoid these allergens: {allergies or 'none'}. "
                  "Give: recipe name, ingredients with quantities, numbered steps, servings.")
        try:
            with st.spinner("The chef is cooking..."):
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": prompt}],
                )
            st.session_state.recipe = res.choices[0].message.content
            st.session_state.count = st.session_state.get("count", 0) + 1
        except Exception:
            st.session_state.recipe = None
            st.error("The chef is busy right now. Please try again in a minute.")
with right:
    with st.container(border=True):
        st.subheader("Your recipe")
        recipe = st.session_state.get("recipe")
        if recipe:
            st.markdown(recipe)
            st.download_button("⬇️ Download recipe", recipe, file_name="recipe.txt")
        else:
            st.info("Your recipe will appear here. Pick an example or type your own ingredients.")

st.caption("Recipes are AI generated. Always check ingredients and allergens before cooking.")