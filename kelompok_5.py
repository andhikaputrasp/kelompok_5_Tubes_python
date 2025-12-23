from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__, template_folder="frontend")

FILE_NAME = "StudentsPerformance.csv"

# LOAD & SAVE
def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# ML
def train_model():
    df = load_data()

    encoder = LabelEncoder()
    df["gender"] = encoder.fit_transform(df["gender"])
    df["lunch"] = encoder.fit_transform(df["lunch"])
    df["test preparation course"] = encoder.fit_transform(
        df["test preparation course"]
    )

    X = df[
        [
            "reading score",
            "writing score",
            "gender",
            "lunch",
            "test preparation course",
        ]
    ]
    y = df["math score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model


model = train_model()

# ROUTES
@app.route("/")
def index():
    df = load_data()
    return render_template("index.html", data=df.iterrows())


@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        df = load_data()

        data_baru = {
            "gender": request.form["gender"],
            "race/ethnicity": request.form["race"],
            "parental level of education": request.form["parental"],
            "lunch": request.form["lunch"],
            "test preparation course": request.form["test"],
            "math score": int(request.form["math"]),
            "reading score": int(request.form["reading"]),
            "writing score": int(request.form["writing"]),
        }

        df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
        save_data(df)

        return redirect(url_for("index"))

    return render_template("tambah.html")


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    df = load_data()
    data = df.loc[index]

    if request.method == "POST":
        df.at[index, "math score"] = int(request.form["math"])
        df.at[index, "reading score"] = int(request.form["reading"])
        df.at[index, "writing score"] = int(request.form["writing"])
        save_data(df)

        return redirect(url_for("index"))

    return render_template("edit.html", data=data, index=index)


@app.route("/hapus/<int:index>")
def hapus(index):
    df = load_data()
    df = df.drop(index)
    save_data(df)

    return redirect(url_for("index"))


# PREDIKSI mL
@app.route("/predict", methods=["GET", "POST"])
def predict():
    hasil = None

    if request.method == "POST":
        reading = int(request.form["reading"])
        writing = int(request.form["writing"])
        gender = int(request.form["gender"])
        lunch = int(request.form["lunch"])
        test = int(request.form["test"])

        hasil = model.predict(
            [[reading, writing, gender, lunch, test]]
        )[0]

    return render_template("predict.html", hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)
