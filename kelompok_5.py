from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__, template_folder="frontend")

file_kelompok_5 = "StudentsPerformance.csv"

# Load DATA
def load_data():
    try:
        return pd.read_csv(file_kelompok_5)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "gender", "race/ethnicity", "parental level of education",
            "lunch", "test preparation course",
            "math score", "reading score", "writing score"
        ])
        df.to_csv(file_kelompok_5, index=False)
        return df


def save_data(df):
    df.to_csv(file_kelompok_5, index=False)


# HALAMAN UTAMA
@app.route("/")
def index():
    df = load_data()

    gender = request.args.get("gender")
    show_all = request.args.get("show")

    # SEARCH GENDER
    if gender:
        df = df[df["gender"] == gender]

    # DEFAULT 10 DATA
    if show_all != "true":
        df = df.head(10)

    return render_template("index.html", data=df.iterrows())

# TAMBAH DATA
@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        df = load_data()

        data_baru = {
            "gender": request.form["gender"],
            "race/ethnicity": request.form["race"],
            "parental level of education": request.form["parent"],
            "lunch": request.form["lunch"],
            "test preparation course": request.form["prep"],
            "math score": int(request.form["math"]),
            "reading score": int(request.form["reading"]),
            "writing score": int(request.form["writing"])
        }

        df.loc[len(df)] = data_baru
        save_data(df)
        return redirect(url_for("index"))

    return render_template("tambah.html")


# EDIT DATA
@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    df = load_data()

    if request.method == "POST":
        df.loc[index, "math score"] = int(request.form["math"])
        df.loc[index, "reading score"] = int(request.form["reading"])
        df.loc[index, "writing score"] = int(request.form["writing"])
        save_data(df)
        return redirect(url_for("index"))

    return render_template("edit.html", data=df.loc[index], index=index)


# HAPUS DATA
@app.route("/hapus/<int:index>")
def hapus(index):
    df = load_data()
    df = df.drop(index).reset_index(drop=True)
    save_data(df)
    return redirect(url_for("index"))

# MACHINE LEARNING
@app.route("/predict", methods=["GET", "POST"])
def predict():
    hasil = None

    if request.method == "POST":
        df = load_data()

        enc = LabelEncoder()
        df["gender"] = enc.fit_transform(df["gender"])
        df["lunch"] = enc.fit_transform(df["lunch"])
        df["test preparation course"] = enc.fit_transform(df["test preparation course"])

        X = df[["gender", "reading score", "writing score"]]
        y = df["math score"]

        model = LinearRegression()
        model.fit(X, y)

        gender = enc.fit_transform([request.form["gender"]])[0]
        reading = int(request.form["reading"])
        writing = int(request.form["writing"])

        hasil = model.predict([[gender, reading, writing]])[0]

    return render_template("predict.html", hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)
