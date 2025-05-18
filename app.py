from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        try:
            wage = float(request.form.get("wage", 0))
        except ValueError:
            error = "Invalid wage entered."
        
        try:
            tax_input = request.form.get("tax", "0").replace(",", ".")  # handle commas
            tax_rate = float(tax_input) / 100
        except ValueError:
            error = "Invalid tax rate entered."
        
        try:
            days = int(request.form.get("days", 5))
            if days < 1 or days > 7:
                error = "Days must be between 1 and 7."
        except ValueError:
            error = "Invalid number of days."

        if error:
            return render_template("index.html", error=error,
                                   wage=request.form.get("wage", ""),
                                   tax=request.form.get("tax", ""),
                                   days=request.form.get("days", ""),
                                   )

        total_hours = 0
        for i in range(1, days + 1):
            try:
                hours = float(request.form.get(f"day{i}", 0))
            except ValueError:
                hours = 0
            total_hours += hours

        gross_pay = wage * total_hours
        net_pay = gross_pay * (1 - tax_rate)

        return render_template("result.html", hours=total_hours, gross=gross_pay, net=net_pay, tax=tax_rate * 100)

    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
