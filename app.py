from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        wage = float(request.form.get("wage", 0))
        tax_rate = float(request.form.get("tax", 0)) / 100  # convert percent to decimal
        total_hours = 0

        for i in range(1, 6):  # 5 days
            hours = float(request.form.get(f"day{i}", 0))
            total_hours += hours

        gross_pay = wage * total_hours
        net_pay = gross_pay * (1 - tax_rate)

        return render_template("result.html", hours=total_hours, gross=gross_pay, net=net_pay, tax=tax_rate * 100)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

