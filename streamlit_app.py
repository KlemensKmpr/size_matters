import streamlit as st

#Überschrift
st.header("Size Matters!")
# Unterüberschrift
st.subheader("Guess the real size of the object!")

# dient für die navigation zwischen den Seiten Play und Sats
pg = st.navigation([st.Page("play.py", title="Play", icon="🎮"), st.Page("stats.py", title="Statistics", icon= "📊")])
pg.run()