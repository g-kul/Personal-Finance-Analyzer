from datetime import datetime


# global variables
all_transactions_list = []
budgets = {}

'''total_budget = 0
Food_budget = 0
Entertainment_budget = 0
Travel_budget = 0
Personal_budget = 0
Miscellaneous_budget = 0'''


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


def get_datetime_input():
    while True:
        date_str = input('Enter the date in "dd/mm/yyyy" format: ')
        try:
            date_formatted = datetime.strptime(date_str, "%d/%m/%Y")
            return date_formatted
            break
        except:
            print("Enter a valid date in the specified format")


def get_budget_month():
    while True:
        month_str = input('Enter the budget month in "mm/yyyy" format: ')
        try:
            month_formatted = datetime.strptime(month_str, "%m/%Y")
            return month_formatted
            break
        except:
            print("Enter a valid month in the specified format")


def add_transactions():
    global all_transactions_list
    while True:
        entry = []
        try:
            choice = int(input("Enter 0 to exit or 1 to enter a transaction data"))
        except:
            choice = -1
        if choice == 1:
            print(
                "Enter your transactions below, it follows the format Transaction = (date, transaction type, amount, category, description)"
            )
            date = get_datetime_input()
            t_type = int(
                input(
                    "Enter the type of transaction: \n\n1.Enter 1 for income\n2.Enter 2 for expense"
                )
            )
            if t_type == 1:
                transaction_type = "income"
                ctgry = 1
            elif t_type == 2:
                transaction_type = "expense"
                ctgry = 2
            if ctgry == 1:
                inc_ctgry = int(
                    input(
                        "Enter the type of income: \n\n1. Enter 1 for salary 2. Enter 2 for others"
                    )
                )
                if inc_ctgry == 1:
                    category = "salary"
                elif inc_ctgry == 2:
                    category = "others"
            elif ctgry == 2:
                exp_ctgry = int(
                    input(
                        "Enter the type of expense: \n\n\
                                1. Enter 1 for Food\n\
                                2. Enter 2 for Entertainment\n\
                                3. Enter 3 for Travel\n\
                                4. Enter 4 for Personal\n\
                                5. Enter 5 for Miscellaneuos"
                    )
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
            amount = float(input("Enter the amount of transaction: "))
            expense_description = input("Enter the description for your transaction: ")
            entry = [
                date,
                transaction_type,
                amount,
                category,
                expense_description,
            ]
            for date as key in budget dictionary:
                if dictionary[date][month] == entry[0][month]:
                    sum = 0
                    for all_transactions_list:
                        sum += all_transactions_list[date][category][amount]
            if sum > budget_dictioinary[category][amount]:
                print(f"You have gone over budget for category {entry[3]} for month {entry[0][month]}")
                print("Do you want to still continue with adding this and editing monthly budget OR cancel this entry")
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
            category = "others"
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
    n = 0
    for i in all_transactions_list:
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
    global budgets
    budget_month = get_budget_month()
    Food_budget = float(input("Enter the budget for food: "))
    Entertainment_budget = float(input("Enter the budget for Entertainment: "))
    Travel_budget = float(input("Enter the budget for Travel: "))
    Personal_budget = float(input("Enter the budget for Personal: "))
    Miscellaneous_budget = float(input("Enter the budget for Miscellaneous: "))
    budget_targets = {"Food":Food_budget,"Entertainment":Entertainment_budget,"Travel":Travel_budget,"Personal":Personal_budget,"Miscellaneuos":Miscellaneous_budget}
    budgets[budget_month] = budget_targets



def budget_status():
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
