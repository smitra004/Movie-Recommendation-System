import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies = pickle.load(open(r'C:\Users\mitra\Downloads\movies.pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\mitra\Downloads\similarity.pkl', 'rb'))

# OMDb API setup
OMDB_API_KEY = "21b5b1ad"  # replace with your API key if needed

def fetch_omdb_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'poster': data.get('Poster', 'https://via.placeholder.com/500x750?text=No+Image'),
            'genre': data.get('Genre', 'N/A'),
            'year': data.get('Year', 'N/A'),
            'rating': data.get('imdbRating', 'N/A'),
            'plot': data.get('Plot', 'N/A')
        }
    else:
        return {
            'poster': 'https://via.placeholder.com/500x750?text=No+Image',
            'genre': 'N/A',
            'year': 'N/A',
            'rating': 'N/A',
            'plot': 'N/A'
        }

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_data = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        meta = fetch_omdb_data(title)
        recommended_data.append((title, meta))
    return recommended_data

# Streamlit app layout
st.set_page_config(page_title="Movie Recommender", layout="wide")
tabs = st.tabs(["🏠 Home", "📖 About Project"])

with tabs[0]:  # Home tab
    st.title('🎬 Movie Recommender System')
    selected_movie = st.selectbox("Select a movie to get recommendations:", movies['title'].values)

    if st.button('Recommend'):
        recommendations = recommend(selected_movie)
        st.subheader("Top 5 Recommendations")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(recommendations[i][1]['poster'])
                st.markdown(f"**{recommendations[i][0]}**")
                st.caption(f"🎞️ {recommendations[i][1]['genre']}")
                st.caption(f"⭐ {recommendations[i][1]['rating']} | 📅 {recommendations[i][1]['year']}")
                st.markdown(f"_{recommendations[i][1]['plot'][:150]}..._")

with tabs[1]:  # About Project
    st.title("📖 About the Project")
    st.markdown("""
    This project is a **content-based movie recommender system** using **cosine similarity**.
    
    - Uses **TF-IDF vectorization** on movie tags
    - Integrates **OMDb API** to enrich recommendations with posters, ratings, genres, plots
    - Built with **Python, scikit-learn, pandas, and Streamlit**
    - Deployable as a **web app** for end users
    """)

