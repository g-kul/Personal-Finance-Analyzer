# global variables
all_transactions_list = []


# Main menu function
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
    i = 1
    for n in menu:
        print(i, ". ", n)
        i += 1


def user_menu_input():
    try:
        user_input = int(input("Enter your choice: "))
    except:
        user_input = -1
    return user_input
    # if else to check entry


def add_transactions():
    global all_transactions_list
    # day and moth for checking the reference in list so we can assign it correctly not sure just kept it here for now
    day = {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
    }
    month = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
    # each transaction is of format Transaction = (date, type, amount, category, description)
    while True:
        entry = []
        try:
            choice = int(input("Enter 0 to exit or 1 to enter a transaction data"))
        except:
            choice = -1
        if choice == 1:
            print(
                "Enter your transactions below, it follows the format Transaction = (date, type, amount, category, description)"
            )
            date = input("Enter the date of trasaction in format dd/mm/yyyy: ")
            t_type = int(
                input(
                    "Enter the type of transaction: \n\n1.Enter 1 for income\n2.Enter 2 for expense"
                )
            )
            if t_type == 1:
                transaction_type = "income"
            elif t_type == 2:
                transaction_type = "expense"
            amount = float(input("Enter the amount of transaction: "))
            ctgry = int(
                input(
                    "Enter 1 if category you wish to enter is income and 2 for expense"
                )
            )
            if ctgry == 1:
                inc_ctgry = input(
                    "Enter the type of income: \n\n1. Enter 1 for salary 2. Enter 2 for others"
                )
                if inc_ctgry == 1:
                    category = "salary"
                elif inc_ctgry == 2:
                    category = "others"
            elif ctgry == 2:
                exp_ctgry = input(
                    "Enter the type of expense: \n\n\
                                1. Enter 1 for Food\n\
                                2. Enter 2 for Entertainment\n\
                                3. Enter 3 for Travel\n\
                                4. Enter 4 for Personal\n\
                                5. Enter 5 for Miscellaneuos"
                )
                if exp_ctgry == 1:
                    category = "Food"
                elif exp_ctgry == 2:
                    category = "Entertainment"
                elif exp_ctgry == 3:
                    category = "Travel"
                elif exp_ctgry == 4:
                    category = "Personal"
                elif exp_ctgry == 5:
                    category = "Miscellaneuos"
            expense_description = input("Enter the description for your expense: ")
            entry = [
                date,
                transaction_type,
                amount,
                category,
                expense_description,
            ]
            result = tuple(entry)
            all_transactions_list.append(result)
        elif choice == 0:
            break
        elif choice not in {0, 1} or choice == -1:
            print("Enter a valid choice!!!")

    # iterate through entry and enter into list with sublist for each entry


def view_transactions():
    if all_transactions_list == []:
        print("You havent entered any transcations yet!")
    else:
        n = 1
        for i in all_transactions_list:
            print("Each transaction done by you are:  ")
            print(n, ". ", i)
            n += 1


def view_transactions_category():
    choice = int(
        input(
            "Enter the type of transaction you wish to see\n\n\
                    1. Enter 1 for seeing those under income\n\
                    2. Enter 2 for seeing those under expense\n"
        )
    )
    if choice == 1:
        ttype = "income"
        options = int(
            input(
                "Enter the choice of transaction in income: \n\n\
                         Enter 1 for seeing under 'salary'\n\
                         Enter 2 for seeing under 'others'\n"
            )
        )
        if options == 1:
            category = "salary"
        elif options == 2:
            category == "others"
    elif choice == 2:
        ttype = "expense"
        options = int(
            input(
                "Enter the choice of transaction in expense: \n\n\
                        1. Enter 1 seeing under Food\n\
                        2. Enter 2 seeing under Entertainment\n\
                        3. Enter 3 seeing under Travel\n\
                        4. Enter 4 seeing under Personal\n\
                        5. Enter 5 seeing under Miscellaneuos"
            )
        )
        if options == 1:
            category = "Food"
        elif options == 2:
            category = "Entertainment"
        elif options == 3:
            category = "Travel"
        elif options == 4:
            category = "Personal"
        elif options == 5:
            category = "Miscellaneuos"
    print("Your selected transactions are: \n\n")
    found = False
    for i in all_transactions_list:
        n = 0
        if i[1] == ttype and i[3] == category:
            print("Index: ", n, " ", i)
        found = True
        n += 1
    if not found:
        print("No entry has been found!")


def summary():
    print("The summary of your entire transactions are:  ")
    income = 0
    expense = 0
    salary = 0
    others = 0
    Food = 0
    Entertainment = 0
    Travel = 0
    Personal = 0
    Miscellaneuos = 0
    for i in all_transactions_list:
        if i[1] == "income" and i[3] == "salary":
            income += i[2]
            salary += i[2]
        elif i[1] == "income" and i[3] == "others":
            income += i[2]
            others += i[2]
        elif i[1] == "expense" and i[3] == "Food":
            expense += i[2]
            Food += i[2]
        elif i[1] == "expense" and i[3] == "Entertainment":
            expense += i[2]
            Entertainment += i[2]
        elif i[1] == "expense" and i[3] == "Travel":
            expense += i[2]
            Travel += i[2]
        elif i[1] == "expense" and i[3] == "Personal":
            expense += i[2]
            Personal += i[2]
        elif i[1] == "expense" and i[3] == "Miscellaneuos":
            expense += i[2]
            Miscellaneuos += i[2]

    print(
        "The summary of your transactions are: \n\n",
        f"Income: {income}\n",
        f"Salary: {salary}\n",
        f"Other_income: {others}\n",
        f"Expense: {expense}\n",
        f"Food: {Food}\n",
        f"Entertainment: {Entertainment}\n",
        f"Travel: {Travel}\n",
        f"Personal: {Personal}\n",
        f"Miscellaneuos: {Miscellaneuos}\n",
    )


def set_budget():
    budget = input("Enter the budget you want to set up for the month: ")


# def budget_status():


# def reports():


def main():
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
            break
        elif entry not in {1, 2, 3, 4, 5, 6, 7, 8} or entry == -1:
            print("Enter valid input!!!")


main()
