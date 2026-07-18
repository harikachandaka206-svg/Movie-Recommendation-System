import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv("movies.csv")

movies["text"] = movies["Title"] + " " + movies["Genre"]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(movies["text"])

model = NearestNeighbors(metric="cosine")

model.fit(X)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully.")