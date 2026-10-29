
from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

data = {
    "url_length": [20, 75, 65, 18, 80, 22, 60, 25, 70, 19],
    "has_at": [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    "num_dots": [1, 5, 4, 2, 6, 1, 4, 2, 5, 1],
    "has_https": [1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    "num_hyphens": [0, 4, 3, 0, 5, 0, 2, 0, 3, 0],
    "label": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if (
            not url
            or len(url) > 2048
            or " " in url
            or "." not in url
            or "://" not in url
        ):
            error = "Please enter a valid-looking URL."

        elif not url.lower().startswith(
            ("http://", "https://")
        ):
            error = "Use a URL starting with http:// or https://."

        else:
            features = [[
                len(url),
                int("@" in url),
                url.count("."),
                int(url.lower().startswith("https://")),
                url.count("-")
            ]]

            prediction = int(model.predict(features)[0])
            probability = float(
                model.predict_proba(features)[0][1] * 100
            )
            risk_score = round(probability / 20, 1)

            result = {
                "url": url,
                "length": len(url),
                "has_at": "Yes" if "@" in url else "No",
                "dots": url.count("."),
                "https": (
                    "Yes"
                    if url.lower().startswith("https://")
                    else "No"
                ),
                "hyphens": url.count("-"),
                "probability": round(probability, 2),
                "risk": risk_score,
                "prediction": prediction
            }

    return render_template(
        "index.html", result=result, error=error
    )


if __name__ == "__main__":
    app.run(debug=False)
              
