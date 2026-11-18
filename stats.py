# Die Statisktik Seite dient dafür verschiedene intresannte Werte von den vergangeneden gespielten Runden auszurchenen und anzuzeigen. 
import streamlit as st

# Zuerst wird Kontrolliert ob bisher überhaupt Runden gespielt wurden
if "games" not in st.session_state or len(st.session_state.games) == 0: 
    st.info("No games played yet. Play the game to see statistics!")
    st.stop()

# Die Anzahl der Versuche jeder Runde wird in der Liste gesammelt
count = []
for game in st.session_state.games:
    count.append(game["count"])
game_numbers = list(range(1, len(count) + 1)) # ohne die +1 wurde die X-Achse bei 0 anfangen
mean = sum(count) / len(count)
mean = round(mean, 1) # der Durchschnitt von den Rateversuchen pro Runde auf eine Nachkommastelle gerundet

# Anzahl der Spiele und durchschnittliche Versuche pro Spiel 
links, rechts = st.columns(2)
with links: 
    st.metric("Games played", len(count))
with rechts:
    st.metric("Average guesses per game", mean)
st.bar_chart({"Game": game_numbers, "Guesses": count}, x="Game", y="Guesses", height=300, x_label="Game", y_label="Guesses") # erstellung des Diagramms


# Folgendes gehört zu den Bereich der stats für die Zusatz benotung
# Unterüberschrift und eine kruze Erklärung um die Statistik besser zu verstehen 
st.subheader("Guess quality")
st.write("Each guess is compared to the real size of the object. The deviation is calculated as (guess − real size) / real size × 100. A negative value means the guess was too small, a positive value means it was too big. A guess within ±15 % counts as correct.")

# Der erste Versuch sagt viel aus wie gut man ist da man nach dem ersten Versuch bekommt man hilfe vom Chat
first_guesses = []
for game in st.session_state.games:
    first_guesses.append(abs(game["deviations"][0])) # erste abweichung der Runde, es wird nur geschaut wie weit weil sich sonst positve und negative Werte aufheben
first_guesses_mean = sum(first_guesses) / len(first_guesses)
first_guesses_mean = round(first_guesses_mean, 1)

# Rät der Spieler eher zu hoch oder zu niedrig
# Es gibt noch eine ungenauigkeit hier, der letzte Tipp auch wenn es correct ist wird mitgezählt
too_small = 0 
too_big = 0 
for game in st.session_state.games: 
    for d in game["deviations"]: 
        if d < 0: 
            too_small += 1
        else: 
            too_big += 1
together = too_small + too_big # Alle Tipps zusammen rechenen für den Prozent Anteil
together_too_small = too_small / together * 100
together_too_small = round(together_too_small, 1)
together_too_big = too_big / together * 100
together_too_big = round(together_too_big, 1)

# Die drei Kennzahlen zu der Schätzqualität nebeneinander
links, mitte, rechts = st.columns(3)
with links:
    st.metric("Avg. first guess off by", f"{first_guesses_mean} %")
with mitte:
    st.metric("Guesses too small", f"{together_too_small} %")
with rechts: 
    st.metric("Guesses too big", f"{together_too_big} %")


# Annäherung beim letzten Spiel 
# Das ist ein Liniendiagramm für die letzte Runde, wo man sieht wie man sich der Lösung Schritt für Schritt annähert 
st.write("How your guesses approached the real size in the last game (0 % = perfect)")
last_game_deviations = st.session_state.games[-1]["deviations"] 
guess_numbers = list(range(1, len(last_game_deviations) + 1))
st.line_chart({"Guess": guess_numbers, "Deviation (%)": last_game_deviations}, x="Guess", y="Deviation (%)", height=300)