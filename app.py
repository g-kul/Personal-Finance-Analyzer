import base64
import io
import json
import os
from collections import defaultdict
from datetime import date, datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, flash, redirect, render_template, request, url_for

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")

EXPENSE_CATEGORIES = ["Food", "Entertainment", "Travel", "Personal", "Miscellaneous"]
INCOME_CATEGORIES = ["salary", "others"]

# Same palette used throughout the app and charts, so a category always
# reads as the same color everywhere it appears.
CATEGORY_COLORS = {
    "Food": "#FF9500",
    "Entertainment": "#AF52DE",
    "Travel": "#30B0C7",
    "Personal": "#007AFF",
    "Miscellaneous": "#8E8E93",
}

app = Flask(__name__)
app.secret_key = "dev-only-secret-key"  # fine for local/personal use


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
def seed_demo_data():
    """Populate a small, realistic dataset on first run so the dashboard and
    charts have something to show right away."""
    demo_transactions = [
        {"id": 1, "date": "2026-06-01", "type": "income", "category": "salary", "amount": 55000, "description": "June salary"},
        {"id": 2, "date": "2026-06-03", "type": "expense", "category": "Food", "amount": 4200, "description": "Groceries"},
        {"id": 3, "date": "2026-06-08", "type": "expense", "category": "Entertainment", "amount": 1500, "description": "Movies"},
        {"id": 4, "date": "2026-06-14", "type": "expense", "category": "Travel", "amount": 3200, "description": "Cab fares"},
        {"id": 5, "date": "2026-06-20", "type": "expense", "category": "Personal", "amount": 1800, "description": "Haircut & essentials"},
        {"id": 6, "date": "2026-07-01", "type": "income", "category": "salary", "amount": 55000, "description": "July salary"},
        {"id": 7, "date": "2026-07-02", "type": "income", "category": "others", "amount": 2000, "description": "Freelance work"},
        {"id": 8, "date": "2026-07-05", "type": "expense", "category": "Food", "amount": 5100, "description": "Groceries"},
        {"id": 9, "date": "2026-07-11", "type": "expense", "category": "Entertainment", "amount": 2200, "description": "Concert tickets"},
        {"id": 10, "date": "2026-07-16", "type": "expense", "category": "Travel", "amount": 2600, "description": "Fuel"},
        {"id": 11, "date": "2026-07-22", "type": "expense", "category": "Miscellaneous", "amount": 900, "description": "Gift"},
        {"id": 12, "date": "2026-08-01", "type": "income", "category": "salary", "amount": 56000, "description": "August salary"},
        {"id": 13, "date": "2026-08-04", "type": "expense", "category": "Food", "amount": 3800, "description": "Groceries"},
        {"id": 14, "date": "2026-08-09", "type": "expense", "category": "Entertainment", "amount": 1200, "description": "Streaming subscriptions"},
        {"id": 15, "date": "2026-08-15", "type": "expense", "category": "Travel", "amount": 4100, "description": "Weekend trip"},
        {"id": 16, "date": "2026-08-19", "type": "expense", "category": "Personal", "amount": 2200, "description": "Gym membership"},
    ]
    save_transactions(demo_transactions)

    current_month = datetime.today().strftime("%Y-%m")
    save_budgets({
        current_month: {
            "Food": 6000,
            "Entertainment": 2500,
            "Travel": 4000,
            "Personal": 2500,
            "Miscellaneous": 1500,
        }
    })


def load_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    with open(TRANSACTIONS_FILE) as f:
        return json.load(f)


def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions, f, indent=2)


def load_budgets():
    if not os.path.exists(BUDGETS_FILE):
        return {}
    with open(BUDGETS_FILE) as f:
        return json.load(f)


def save_budgets(budgets):
    with open(BUDGETS_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(TRANSACTIONS_FILE) or not os.path.exists(BUDGETS_FILE):
    seed_demo_data()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def next_id(transactions):
    return max((t["id"] for t in transactions), default=0) + 1


def month_key(iso_date):
    """'2026-08-15' -> '2026-08'"""
    return iso_date[:7]


def filter_by_month(transactions, ym):
    return [t for t in transactions if month_key(t["date"]) == ym]


def compute_totals(transactions):
    totals = {"income": 0.0, "expense": 0.0, "salary": 0.0, "others": 0.0}
    counts = {}
    for c in EXPENSE_CATEGORIES:
        totals[c] = 0.0
        counts[c] = 0
    for t in transactions:
        if t["type"] == "income":
            totals["income"] += t["amount"]
            if t["category"] in INCOME_CATEGORIES:
                totals[t["category"]] += t["amount"]
        elif t["type"] == "expense" and t["category"] in EXPENSE_CATEGORIES:
            totals["expense"] += t["amount"]
            totals[t["category"]] += t["amount"]
            counts[t["category"]] += 1
    return totals, counts


def available_months(transactions, budgets):
    months = {month_key(t["date"]) for t in transactions} | set(budgets.keys())
    return sorted(months, reverse=True)


def fig_to_base64():
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=170, transparent=True)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


# ---------------------------------------------------------------------------
# Template filters
# ---------------------------------------------------------------------------
app.jinja_env.filters["inr"] = lambda v: f"₹{v:,.2f}"
app.jinja_env.filters["prettydate"] = lambda d: datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y")
app.jinja_env.filters["monthlabel"] = lambda m: datetime.strptime(m, "%Y-%m").strftime("%B %Y")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def dashboard():
    transactions = load_transactions()
    budgets = load_budgets()
    totals, _ = compute_totals(transactions)
    net_balance = totals["income"] - totals["expense"]

    months = available_months(transactions, budgets)
    current_month = datetime.today().strftime("%Y-%m")
    this_month = current_month if (current_month in months or not months) else months[0]

    month_transactions = filter_by_month(transactions, this_month)
    month_totals, _ = compute_totals(month_transactions)

    recent = sorted(transactions, key=lambda t: t["date"], reverse=True)[:5]

    category_breakdown = [
        {"name": c, "amount": month_totals[c], "color": CATEGORY_COLORS[c]}
        for c in EXPENSE_CATEGORIES
        if month_totals[c] > 0
    ]
    max_cat_amount = max([c["amount"] for c in category_breakdown], default=0)

    return render_template(
        "index.html",
        active="dashboard",
        totals=totals,
        net_balance=net_balance,
        this_month=this_month,
        month_totals=month_totals,
        recent=recent,
        category_breakdown=category_breakdown,
        max_cat_amount=max_cat_amount,
        category_colors=CATEGORY_COLORS,
    )


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transactions = load_transactions()
        category = request.form.get("category", "")
        t_type = "income" if category in INCOME_CATEGORIES else "expense"
        try:
            amount = float(request.form.get("amount") or 0)
        except ValueError:
            amount = 0.0

        entry = {
            "id": next_id(transactions),
            "date": request.form.get("date") or date.today().isoformat(),
            "type": t_type,
            "category": category,
            "amount": amount,
            "description": (request.form.get("description") or "").strip(),
        }
        transactions.append(entry)
        save_transactions(transactions)
        flash("Transaction added.")
        return redirect(url_for("transactions"))

    return render_template(
        "add_transaction.html",
        active="add",
        expense_categories=EXPENSE_CATEGORIES,
        income_categories=INCOME_CATEGORIES,
        today=date.today().isoformat(),
    )


@app.route("/transactions")
def transactions():
    all_t = load_transactions()
    budgets = load_budgets()
    months = available_months(all_t, budgets)

    selected_month = request.args.get("month", "")
    selected_category = request.args.get("category", "")
    selected_type = request.args.get("type", "")

    filtered = all_t
    if selected_month:
        filtered = [t for t in filtered if month_key(t["date"]) == selected_month]
    if selected_category:
        filtered = [t for t in filtered if t["category"] == selected_category]
    if selected_type:
        filtered = [t for t in filtered if t["type"] == selected_type]

    filtered = sorted(filtered, key=lambda t: t["date"], reverse=True)

    return render_template(
        "transactions.html",
        active="transactions",
        transactions=filtered,
        months=months,
        expense_categories=EXPENSE_CATEGORIES,
        income_categories=INCOME_CATEGORIES,
        selected_month=selected_month,
        selected_category=selected_category,
        selected_type=selected_type,
        category_colors=CATEGORY_COLORS,
    )


@app.route("/budget", methods=["GET", "POST"])
def budget():
    all_t = load_transactions()
    budgets = load_budgets()

    if request.method == "POST":
        month = request.form.get("month")
        if month:
            budgets[month] = {
                c: float(request.form.get(c) or 0) for c in EXPENSE_CATEGORIES
            }
            save_budgets(budgets)
            flash(f"Budget saved for {datetime.strptime(month, '%Y-%m').strftime('%B %Y')}.")
        return redirect(url_for("budget", month=month))

    months = available_months(all_t, budgets)
    current_month = datetime.today().strftime("%Y-%m")
    selected_month = request.args.get("month") or (
        current_month if (current_month in months or not months) else months[0]
    )

    month_budget = budgets.get(selected_month, {})
    month_transactions = filter_by_month(all_t, selected_month)
    totals, _ = compute_totals(month_transactions)

    rows = []
    for c in EXPENSE_CATEGORIES:
        spent = totals[c]
        target = month_budget.get(c, 0)
        pct = min(int((spent / target) * 100), 100) if target else 0
        rows.append({
            "category": c,
            "spent": spent,
            "target": target,
            "pct": pct,
            "over": bool(target) and spent > target,
            "color": CATEGORY_COLORS[c],
        })

    return render_template(
        "budget.html",
        active="budget",
        months=months,
        selected_month=selected_month,
        current_month=current_month,
        month_budget=month_budget,
        rows=rows,
        expense_categories=EXPENSE_CATEGORIES,
    )


@app.route("/reports")
def reports():
    all_t = load_transactions()
    budgets_data = load_budgets()
    months = available_months(all_t, budgets_data)

    scope = request.args.get("scope", "all")
    if scope != "all" and scope in months:
        transactions_in_scope = filter_by_month(all_t, scope)
        relevant_budgets = {k: v for k, v in budgets_data.items() if k == scope}
        scope_label = datetime.strptime(scope, "%Y-%m").strftime("%B %Y")
    else:
        scope = "all"
        transactions_in_scope = all_t
        relevant_budgets = budgets_data
        scope_label = "All time"

    totals, counts = compute_totals(transactions_in_scope)
    categories = EXPENSE_CATEGORIES
    spending = [totals[c] for c in categories]
    breakdown_counts = [counts[c] for c in categories]
    colors = [CATEGORY_COLORS[c] for c in categories]

    budget_totals = [0.0] * len(categories)
    for targets in relevant_budgets.values():
        for i, c in enumerate(categories):
            budget_totals[i] += targets.get(c, 0)

    plt.rcParams.update({"font.size": 12, "font.family": "sans-serif"})

    bar_chart = None
    if sum(spending) > 0:
        plt.figure(figsize=(7.2, 4.8))
        plt.bar(categories, spending, color=colors)
        plt.ylabel("Amount spent")
        plt.title(f"Spending by category — {scope_label}")
        bar_chart = fig_to_base64()

    pie_chart = None
    if sum(spending) > 0:
        plt.figure(figsize=(6, 6))
        plt.pie(spending, labels=categories, colors=colors, autopct="%1.0f%%")
        plt.title(f"Expense breakdown — {scope_label}")
        pie_chart = fig_to_base64()

    budget_chart = None
    if any(budget_totals):
        x = list(range(len(categories)))
        width = 0.35
        plt.figure(figsize=(11, 4.6))
        plt.bar([i - width / 2 for i in x], spending, width, label="Spent", color="#0071e3")
        plt.bar([i + width / 2 for i in x], budget_totals, width, label="Budget", color="#c7c7cc")
        plt.xticks(x, categories)
        plt.legend()
        plt.title(f"Budget vs actual — {scope_label}")
        budget_chart = fig_to_base64()

    trend_chart = None
    if scope == "all":
        income_by_month = defaultdict(float)
        expense_by_month = defaultdict(float)
        for t in all_t:
            m = month_key(t["date"])
            if t["type"] == "income":
                income_by_month[m] += t["amount"]
            else:
                expense_by_month[m] += t["amount"]
        month_labels = sorted(set(income_by_month) | set(expense_by_month))
        if month_labels:
            plt.figure(figsize=(11, 4.6))
            plt.plot(month_labels, [income_by_month[m] for m in month_labels], label="Income", color="#34c759", marker="o")
            plt.plot(month_labels, [expense_by_month[m] for m in month_labels], label="Expense", color="#ff3b30", marker="o")
            plt.legend()
            plt.title("Income vs expense over time")
            plt.xticks(rotation=30, ha="right")
            trend_chart = fig_to_base64()

    return render_template(
        "reports.html",
        active="reports",
        months=months,
        scope=scope,
        scope_label=scope_label,
        bar_chart=bar_chart,
        pie_chart=pie_chart,
        budget_chart=budget_chart,
        trend_chart=trend_chart,
    )


if __name__ == "__main__":
    app.run(debug=True)
