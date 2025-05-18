from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        errors = []
        form = request.form

        # Wage
        try:
            wage = float(form.get("wage", 0))
        except ValueError:
            errors.append("Invalid wage entered.")

        # Tax
        try:
            tax_input = form.get("tax", "0").replace(",", ".")
            tax_rate = float(tax_input) / 100
        except ValueError:
            errors.append("Invalid tax rate entered.")

        # Days
        try:
            days = int(form.get("days", 5))
            if days < 1 or days > 7:
                errors.append("Days must be between 1 and 7.")
        except ValueError:
            errors.append("Invalid number of days.")

        if errors:
            return render_template("index.html", error=", ".join(errors), form=form)

        total_hours = 0
        for i in range(1, days + 1):
            try:
                hours = float(form.get(f"day{i}", 0))
            except ValueError:
                hours = 0
            total_hours += hours

        gross_pay = wage * total_hours
        net_pay = gross_pay * (1 - tax_rate)

        return render_template("result.html", hours=total_hours,
                               gross=gross_pay, net=net_pay,
                               tax=tax_rate * 100)

    return render_template("index.html", error=None, form={})

if __name__ == "__main__":
    app.run(debug=True)
