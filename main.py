from datetime import datetime
import json
import os
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Data & constants
# ---------------------------------------------------------------------------
all_transactions_list = []
budgets = {}

EXPENSE_CATEGORIES = ["Food", "Entertainment", "Travel", "Personal", "Miscellaneous"]
INCOME_CATEGORIES = ["salary", "others"]

# Professional, muted palette for charts (kept consistent everywhere a category
# needs a color).
CATEGORY_COLORS = {
    "Food": "#EA4335",
    "Entertainment": "#FBBC04",
    "Travel": "#34A853",
    "Personal": "#4285F4",
    "Miscellaneous": "#A142F4",
}

# Data files live next to this script, not in whatever directory the user
# happens to launch it from.
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "all_transactions_list.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------
def get_int_choice(prompt):
    try:
        return int(input(prompt))
    except (ValueError, TypeError):
        return -1


def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a valid number.")


def get_datetime_input():
    while True:
        date_str = input('Enter the date in "dd/mm/yyyy" format: ')
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            print("Enter a valid date in the specified format")


def get_month():
    while True:
        month_str = input('Enter the month in "mm/yyyy" format: ')
        try:
            return datetime.strptime(month_str, "%m/%Y")
        except ValueError:
            print("Enter a valid month in the specified format")


def user_menu_input():
    return get_int_choice("Enter your choice: ")


# ---------------------------------------------------------------------------
# Aggregation helper (shared by summary / budget status / reports so the
# same category totals aren't computed with copy-pasted if/elif chains)
# ---------------------------------------------------------------------------
def compute_totals(transactions):
    totals = {"income": 0.0, "expense": 0.0, "salary": 0.0, "others": 0.0}
    counts = {}
    for category in EXPENSE_CATEGORIES:
        totals[category] = 0.0
        counts[category] = 0

    for entry in transactions:
        t_type, amount, category = entry[1], entry[2], entry[3]
        if t_type == "income":
            totals["income"] += amount
            if category in INCOME_CATEGORIES:
                totals[category] += amount
        elif t_type == "expense" and category in EXPENSE_CATEGORIES:
            totals["expense"] += amount
            totals[category] += amount
            counts[category] += 1

    return totals, counts


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
def main_menu():
    menu = [
        "Add Transaction",
        "View all transaction",
        "View Transactions by Category",
        "View Summary & Statistics",
        "Set Budget for Category",
        "Check Budget Status",
        "Generate Monthly Report",
        "Exit",
    ]
    for i, n in enumerate(menu, start=1):
        print(i, ". ", n)


# ---------------------------------------------------------------------------
# Add transaction
# ---------------------------------------------------------------------------
def add_transactions():
    while True:
        choice = get_int_choice("Enter 0 to exit or 1 to enter a transaction data: ")
        if choice == 0:
            break
        if choice != 1:
            print("Enter a valid choice!!!")
            continue

        print(
            "Enter your transaction below, it follows the format "
            "Transaction = (date, transaction type, amount, category, description)"
        )
        date = get_datetime_input()
        t_type = get_int_choice(
            "Enter the type of transaction: \n\n1. Enter 1 for income\n2. Enter 2 for expense: "
        )

        category = None
        if t_type == 1:
            transaction_type = "income"
            inc_ctgry = get_int_choice(
                "Enter the type of income: \n\n1. Enter 1 for salary\n2. Enter 2 for others: "
            )
            category = {1: "salary", 2: "others"}.get(inc_ctgry)
        elif t_type == 2:
            transaction_type = "expense"
            exp_ctgry = get_int_choice(
                "Enter the type of expense: \n\n"
                "1. Enter 1 for Food\n"
                "2. Enter 2 for Entertainment\n"
                "3. Enter 3 for Travel\n"
                "4. Enter 4 for Personal\n"
                "5. Enter 5 for Miscellaneous: "
            )
            category = {
                1: "Food",
                2: "Entertainment",
                3: "Travel",
                4: "Personal",
                5: "Miscellaneous",
            }.get(exp_ctgry)
        else:
            print("Enter a valid choice!!!")
            continue

        if category is None:
            print("Enter a valid choice!!!")
            continue

        amount = get_float_input("Enter the amount of transaction: ")
        description = input("Enter the description for your transaction: ")
        entry = [date, transaction_type, amount, category, description]

        # Only expenses are checked against a budget - income has no budget
        # entry, so checking it used to crash with a KeyError.
        over_budget = False
        budget_key = None
        if transaction_type == "expense":
            for dte in budgets:
                if dte.month == entry[0].month and dte.year == entry[0].year:
                    budget_key = dte
                    break

        if budget_key is not None:
            # Only sum this category's spending for the SAME month, not
            # all-time (the original summed every month together).
            category_total = entry[2]
            for i in all_transactions_list:
                if (
                    i[3] == entry[3]
                    and i[0].month == entry[0].month
                    and i[0].year == entry[0].year
                ):
                    category_total += i[2]
            if category_total > budgets[budget_key].get(entry[3], 0):
                over_budget = True

        if over_budget:
            print(
                f"You will go over budget for category {entry[3]} for month {entry[0].month}"
            )
            option = get_int_choice(
                "Do you want to still continue with adding this and editing the "
                "monthly budget? Press 1 to continue OR enter 0 to cancel this entry: "
            )
            if option == 1:
                all_transactions_list.append(tuple(entry))
                set_budget()
            else:
                print("Entry cancelled.")
        else:
            all_transactions_list.append(tuple(entry))


# ---------------------------------------------------------------------------
# View transactions
# ---------------------------------------------------------------------------
def view_transactions():
    choice = get_int_choice(
        "Enter the transactions you wish to view: \n"
        "Enter 1 to view all transactions you have entered so far\n"
        "Enter 2 to view transactions by month\n"
        "Enter 3 to show transactions for a range of dates: "
    )
    if choice == 1:
        if not all_transactions_list:
            print("You haven't entered any transactions yet!")
        else:
            print("Each transaction you have made:")
            for n, i in enumerate(all_transactions_list, start=1):
                print(n, ". ", i)
    elif choice == 2:
        month_option = get_month()
        found = False
        for n, i in enumerate(all_transactions_list, start=1):
            if i[0].month == month_option.month and i[0].year == month_option.year:
                print(n, ". ", i)
                found = True
        if not found:
            print("There are no entries for the selected month!")
    elif choice == 3:
        start_date = get_datetime_input()
        end_date = get_datetime_input()
        found = False
        for n, i in enumerate(all_transactions_list, start=1):
            if start_date <= i[0] <= end_date:
                print(n, ". ", i)
                found = True
        if not found:
            print("There are no entries entered for the selected dates!")
    else:
        print("Please enter a valid choice!!!")


def view_transactions_category():
    choice = get_int_choice(
        "Enter the type of transaction you wish to see\n\n"
        "1. Enter 1 for seeing those under income\n"
        "2. Enter 2 for seeing those under expense\n: "
    )
    category = None
    if choice == 1:
        ttype = "income"
        options = get_int_choice(
            "Enter the choice of transaction in income: \n\n"
            "1. Enter 1 for seeing under 'salary'\n"
            "2. Enter 2 for seeing under 'others'\n: "
        )
        category = {1: "salary", 2: "others"}.get(options)
    elif choice == 2:
        ttype = "expense"
        options = get_int_choice(
            "Enter the choice of transaction in expense: \n\n"
            "1. Enter 1 for seeing under Food\n"
            "2. Enter 2 for seeing under Entertainment\n"
            "3. Enter 3 for seeing under Travel\n"
            "4. Enter 4 for seeing under Personal\n"
            "5. Enter 5 for seeing under Miscellaneous: "
        )
        category = {
            1: "Food",
            2: "Entertainment",
            3: "Travel",
            4: "Personal",
            5: "Miscellaneous",
        }.get(options)
    else:
        print("Please enter a valid choice!!!")
        return

    if category is None:
        print("Please enter a valid choice!!!")
        return

    month_choice = get_month()
    print(
        f"Your selected transactions for the month {month_choice.month} in "
        f"{month_choice.year} are:\n"
    )
    found = False
    for n, i in enumerate(all_transactions_list):
        if (
            i[1] == ttype
            and i[3] == category
            and i[0].month == month_choice.month
            and i[0].year == month_choice.year
        ):
            print("Index: ", n, " ", i)
            found = True
    if not found:
        print("No entry has been found!")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def summary():
    choice = get_int_choice(
        "Enter the choice of viewing your transactions summary\n"
        "Enter 1 for viewing entire summary\n"
        "Enter 2 for viewing summary for month of choice: "
    )
    if choice == 1:
        transactions = all_transactions_list
        header = "The summary of your entire transactions are:"
    elif choice == 2:
        summary_month = get_month()
        transactions = [
            i
            for i in all_transactions_list
            if i[0].month == summary_month.month and i[0].year == summary_month.year
        ]
        header = (
            f"The summary of your transactions for the month "
            f"{summary_month.month} of year {summary_month.year} are:"
        )
    else:
        print("Please enter a valid choice!!!")
        return

    totals, _ = compute_totals(transactions)
    print(header)
    print(f"Income: {totals['income']}")
    print(f"Salary: {totals['salary']}")
    print(f"Other_income: {totals['others']}")
    print(f"Expense: {totals['expense']}")
    for category in EXPENSE_CATEGORIES:
        print(f"{category}: {totals[category]}")


# ---------------------------------------------------------------------------
# Budgets
# ---------------------------------------------------------------------------
def set_budget():
    print("Enter the month for which you wish to set the budget below")
    budget_month = get_month()
    budget_targets = {}
    for category in EXPENSE_CATEGORIES:
        budget_targets[category] = get_float_input(f"Enter the budget for {category}: ")
    budgets[budget_month] = budget_targets


def budget_status():
    status_month = get_month()
    budget_key = None
    for key in budgets:
        if key.month == status_month.month and key.year == status_month.year:
            budget_key = key
            break

    transactions = [
        i
        for i in all_transactions_list
        if i[0].month == status_month.month and i[0].year == status_month.year
    ]
    totals, _ = compute_totals(transactions)

    print(
        f"The budget status of your transactions for the month "
        f"{status_month.month} of year {status_month.year} are:"
    )
    print(f"Total Income for the month: {totals['income']}")
    print(f"Salary for the month: {totals['salary']}")
    print(f"Other_income for the month: {totals['others']}")

    if budget_key is None:
        # Previously this still tried to print budgets[status_month][...]
        # even when no budget existed, which crashed with a KeyError.
        print(f"Expense for the month: {totals['expense']}")
        print("There is no budget setup for the entered month!!!")
        return

    category_budgets = budgets[budget_key]
    total_budget = sum(category_budgets.values())
    print(
        f"Expense for the month: {totals['expense']} and budget for "
        f"expense for month {total_budget}"
    )
    for category in EXPENSE_CATEGORIES:
        print(
            f"{category} expense for the month is: {totals[category]} and "
            f"budget for {category} for month is {category_budgets.get(category, 0)}"
        )


# ---------------------------------------------------------------------------
# Save / load
# ---------------------------------------------------------------------------
def save_files():
    serializable_transactions = []
    for entry in all_transactions_list:
        entry_list = list(entry)
        entry_list[0] = entry_list[0].strftime("%d/%m/%Y")
        serializable_transactions.append(entry_list)
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(serializable_transactions, file, indent=4)

    serializable_budgets = {
        key.strftime("%m/%Y"): value for key, value in budgets.items()
    }
    with open(BUDGETS_FILE, "w") as file:
        json.dump(serializable_budgets, file, indent=4)


def load_files():
    global all_transactions_list, budgets

    all_transactions_list = []
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as file:
            raw_transactions = json.load(file)
        for entry in raw_transactions:
            entry[0] = datetime.strptime(entry[0], "%d/%m/%Y")
            all_transactions_list.append(tuple(entry))

    budgets = {}
    if os.path.exists(BUDGETS_FILE):
        with open(BUDGETS_FILE, "r") as file:
            raw_budgets = json.load(file)
        for key, value in raw_budgets.items():
            budgets[datetime.strptime(key, "%m/%Y")] = value


# ---------------------------------------------------------------------------
# Reports / charts
# ---------------------------------------------------------------------------
def reports():
    option = get_int_choice(
        "Enter 1 for getting reports based on entire data\n"
        "Enter 2 for getting reports based on month of choice: "
    )

    if option == 1:
        choice = get_int_choice(
            "Enter 1 for spending by category and expense breakdown\n"
            "Enter 2 for expense vs budget by category\n"
            "Enter 3 for total income vs Expense: "
        )
        transactions = all_transactions_list
        month_label = ""
        relevant_budgets = budgets
    elif option == 2:
        choice = get_int_choice(
            "Enter 1 for spending by category and expense breakdown for the month\n"
            "Enter 2 for expense vs budget for month: "
        )
        month_choice = get_month()
        transactions = [
            i
            for i in all_transactions_list
            if i[0].month == month_choice.month and i[0].year == month_choice.year
        ]
        month_label = f" for the month {month_choice.month}/{month_choice.year}"
        if not transactions:
            print("Your entered month is not there in entered transactions")
        relevant_budgets = {
            k: v
            for k, v in budgets.items()
            if k.month == month_choice.month and k.year == month_choice.year
        }
        if not relevant_budgets:
            print("The entered month is not setup in your budgets")
    else:
        print("Please enter a valid choice!!!")
        return

    totals, counts = compute_totals(transactions)
    categories_list = EXPENSE_CATEGORIES
    spending_category = [totals[c] for c in categories_list]
    category_breakdown = [counts[c] for c in categories_list]
    colors = [CATEGORY_COLORS[c] for c in categories_list]

    total_budget_list = [0] * len(categories_list)
    for budget_targets in relevant_budgets.values():
        for idx, category in enumerate(categories_list):
            total_budget_list[idx] += budget_targets.get(category, 0)

    if choice == 1:
        plt.figure()
        plt.bar(categories_list, spending_category, color=colors)
        plt.xlabel("Expense Categories")
        plt.ylabel("Amount spent")
        plt.title(f"Total spending by category{month_label}")
        plt.tight_layout()
        plt.show()

        plt.figure()
        plt.pie(category_breakdown, labels=categories_list, colors=colors)
        plt.title(f"Expense breakdown by number of spending{month_label}")
        plt.show()

        plt.figure()
        plt.pie(spending_category, labels=categories_list, colors=colors)
        plt.title(f"Expense breakdown by amount of spending{month_label}")
        plt.show()
    elif choice == 2:
        x = list(range(len(categories_list)))
        width = 0.4
        plt.figure()
        plt.bar(
            [i - width / 2 for i in x],
            spending_category,
            width,
            label=f"total amount spent{month_label}",
            color="#4285F4",
        )
        plt.bar(
            [i + width / 2 for i in x],
            total_budget_list,
            width,
            label=f"total budget{month_label}",
            color="#FBBC04",
        )
        plt.xticks(x, categories_list)
        plt.legend()
        plt.tight_layout()
        plt.show()
    elif choice == 3 and option == 1:
        income_dict = {}
        expense_dict = {}
        for i in all_transactions_list:
            date_month = i[0].strftime("%m-%Y")
            if i[1] == "income":
                income_dict[date_month] = income_dict.get(date_month, 0) + i[2]
            elif i[1] == "expense":
                expense_dict[date_month] = expense_dict.get(date_month, 0) + i[2]
        months_sort = sorted(set(income_dict.keys()) | set(expense_dict.keys()))
        income_values_sort = [income_dict.get(m, 0) for m in months_sort]
        expense_values_sort = [expense_dict.get(m, 0) for m in months_sort]
        plt.figure()
        plt.plot(months_sort, income_values_sort, label="Income", color="#34A853")
        plt.plot(months_sort, expense_values_sort, label="Expense", color="#EA4335")
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("Please enter a valid choice!!!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    load_files()
    while True:
        main_menu()
        entry = user_menu_input()
        if entry == 1:
            add_transactions()
        elif entry == 2:
            view_transactions()
        elif entry == 3:
            view_transactions_category()
        elif entry == 4:
            summary()
        elif entry == 5:
            set_budget()
        elif entry == 6:
            budget_status()
        elif entry == 7:
            reports()
        elif entry == 8:
            save_files()
            break
        else:
            print("Enter valid input!!!")


if __name__ == "__main__":
    main()
