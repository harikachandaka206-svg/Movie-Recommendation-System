from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

movies = pd.read_csv("movies.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    genre = request.form["genre"]
    person = request.form["actor"].strip()
    language = request.form["language"]

    recommendations = movies.copy()

    # Genre Filter
    if genre:
        recommendations = recommendations[
            recommendations["Genre"].str.lower() == genre.lower()
        ]

    # Language Filter
    if language:
        recommendations = recommendations[
            recommendations["Language"].str.lower() == language.lower()
        ]

    message = ""

    # Actor / Actress Filter
    if person != "":

        actor_movies = recommendations[
            recommendations["Cast"].str.contains(person, case=False, na=False)
        ]

        if not actor_movies.empty:
            recommendations = actor_movies
        else:
            message = f'No movies found for "{person}". Showing {genre} movies in {language} instead.'

    # Maximum 3 recommendations
    recommendations = recommendations.sample(
        min(3, len(recommendations)),
        random_state=42
    ) if not recommendations.empty else recommendations

    return render_template(
        "result.html",
        movies=recommendations.to_dict(orient="records"),
        searched_movie=genre,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)