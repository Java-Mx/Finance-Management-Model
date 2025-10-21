import mysql.connector
import datetime
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "javamx",
    "database": "college_finance_db"
}

CURRENCIES = {
    "INR": "Indian Rupee",
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "NZD": "New Zealand Dollar",
}

conversion_rates = {
    "USD": {"INR_to_currency": 0.01133, "currency_to_INR": 88.28},
    "EUR": {"INR_to_currency": 0.00965, "currency_to_INR": 103.60},
    "GBP": {"INR_to_currency": 0.00835, "currency_to_INR": 119.66},
    "JPY": {"INR_to_currency": 1.67, "currency_to_INR": 0.598},
    "AUD": {"INR_to_currency": 0.01722, "currency_to_INR": 58.08},
    "CAD": {"INR_to_currency": 0.0141, "currency_to_INR": 70.92},
    "CHF": {"INR_to_currency": 0.0108, "currency_to_INR": 92.60},
    "CNY": {"INR_to_currency": 0.0807, "currency_to_INR": 12.29},
    "NZD": {"INR_to_currency": 0.0190, "currency_to_INR": 52.59},
}


def convert_inr_to_currency(amount_inr, currency_code):
    """Convert INR to target currency using fixed rates."""
    if currency_code not in conversion_rates:
        raise ValueError("Unsupported currency code")
    rate = conversion_rates[currency_code]["INR_to_currency"]
    return amount_inr * rate


def convert_currency_to_inr(amount_currency, currency_code):
    if currency_code not in conversion_rates:
        raise ValueError("Unsupported currency code")
    rate = conversion_rates[currency_code]["currency_to_INR"]
    return amount_currency * rate


def print_banner(text):
    print("=" * 60)
    print(text.center(60))
    print("=" * 60)


def db_connect():
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        exit(1)


def create_all_tables():
    cnx = mysql.connector.connect(**{k: v for k, v in DB_CONFIG.items() if k != "database"})
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} DEFAULT CHARACTER SET utf8")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    cnx.database = DB_CONFIG["database"]
    table_ddls = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB
        """,
        "monthly_budget": """
            CREATE TABLE IF NOT EXISTS monthly_budget (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                month VARCHAR(7) NOT NULL,
                budget FLOAT NOT NULL,
                priority1 VARCHAR(100),
                priority1_percent INT,
                priority2 VARCHAR(100),
                priority2_percent INT,
                priority3 VARCHAR(100),
                priority3_percent INT,
                miscellaneous_percent INT
            ) ENGINE=InnoDB
        """,
        "bill_splits": """
            CREATE TABLE IF NOT EXISTS bill_splits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                bill_amount FLOAT NOT NULL,
                num_people INT NOT NULL,
                per_person_share FLOAT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """,
        "tax_calculations": """
            CREATE TABLE IF NOT EXISTS tax_calculations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                income FLOAT NOT NULL,
                tax FLOAT NOT NULL,
                effective_rate FLOAT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """,
        "compound_interest_records": """
            CREATE TABLE IF NOT EXISTS compound_interest_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                principal FLOAT NOT NULL,
                monthly_contrib FLOAT NOT NULL,
                years FLOAT NOT NULL,
                annual_rate FLOAT NOT NULL,
                variance FLOAT NOT NULL,
                frequency ENUM('annual','quarterly','monthly'),
                final_amount FLOAT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """,
        "currency_conversions": """
            CREATE TABLE IF NOT EXISTS currency_conversions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                from_currency VARCHAR(3) NOT NULL,
                to_currency VARCHAR(3) NOT NULL,
                amount FLOAT NOT NULL,
                converted_amount FLOAT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """,
        "savings_records": """
            CREATE TABLE IF NOT EXISTS savings_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                monthly_saving FLOAT NOT NULL,
                years FLOAT NOT NULL,
                annual_return FLOAT NOT NULL,
                final_balance FLOAT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """,
        "entries": """
            CREATE TABLE IF NOT EXISTS entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                type ENUM('income','expense'),
                amount FLOAT NOT NULL,
                tag VARCHAR(100) NOT NULL,
                entry_time DATETIME NOT NULL
            ) ENGINE=InnoDB
        """,
    }
    for name, ddl in table_ddls.items():
        try:
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(f"Error creating table {name}: {err}")
            exit(1)
    cursor.close()
    cnx.close()


def register_user():
    cnx, cursor = db_connect()
    print_banner("NEW USER REGISTRATION")
    while True:
        username = input("Choose a username: ").strip()
        if len(username) < 3:
            print("Username must be at least 3 characters.")
            continue
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Username already exists. Try another.")
        else:
            break
    while True:
        password = input("Choose a password: ")
        confirm = input("Confirm password: ")
        if password != confirm:
            print("Passwords do not match. Try again.")
        elif len(password) < 6:
            print("Password must be at least 6 characters.")
        else:
            break
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password)
    )
    cnx.commit()
    print("Registration successful! Please login now.")
    cursor.close()
    cnx.close()


def login_user():
    cnx, cursor = db_connect()
    print_banner("USER LOGIN")
    username = input("Enter username: ").strip()
    password = input("Enter password: ")
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row is None:
        print("User not found.")
        cursor.close()
        cnx.close()
        return None
    user_id, stored_password = row
    if password == stored_password:
        print(f"Welcome back, {username}!")
        cursor.close()
        cnx.close()
        return user_id
    else:
        print("Incorrect password.")
        cursor.close()
        cnx.close()
        return None


def get_user_financial_summary(user_id):
    cnx, cursor = db_connect()
    cursor.execute(
        "SELECT SUM(amount) FROM entries WHERE user_id = %s AND type = 'income'", (user_id,)
    )
    total_income = cursor.fetchone()[0] or 0
    cursor.execute(
        "SELECT SUM(amount) FROM entries WHERE user_id = %s AND type = 'expense'", (user_id,)
    )
    total_expense = cursor.fetchone()[0] or 0
    cnx.close()
    return total_income, total_expense, total_income - total_expense


def record_entry(user_id):
    cnx, cursor = db_connect()
    print_banner("RECORD INCOME/EXPENSE ENTRY")
    while True:
        entry_type = input("Enter 'i' for income or 'e' for expense: ").lower()
        if entry_type == "i":
            entry_type_full = "income"
            break
        elif entry_type == "e":
            entry_type_full = "expense"
            break
        else:
            print("Please enter 'i' or 'e'.")
    while True:
        try:
            amount = float(input("Enter amount (₹): "))
            if amount <= 0:
                print("Please enter a positive number.")
                continue
            break
        except:
            print("Invalid amount. Try again.")
    if entry_type_full == "income":
        allowed_income_tags = [
            "salary",
            "bonus",
            "interest",
            "investment",
            "gift",
            "other",
        ]
        print(f"Allowed income tags: {', '.join(allowed_income_tags)}")
        while True:
            tag = input("Enter a tag for income: ").strip().lower()
            if tag in allowed_income_tags:
                break
            else:
                print("Invalid tag. Try again.")
    else:
        tag = input("Enter a tag for expense: ").strip()
    now = datetime.datetime.now()
    cursor.execute(
        "INSERT INTO entries (user_id, type, amount, tag, entry_time) VALUES (%s, %s, %s, %s, %s)",
        (user_id, entry_type_full, amount, tag, now),
    )
    cnx.commit()
    total_income, total_expense, balance = get_user_financial_summary(user_id)
    if entry_type_full == "income":
        print("\n" + "=" * 60)
        print(f"🎉 Income recorded: ₹{amount:.2f} (Cr)")
        print(f"Total Income: ₹{total_income:.2f} (Cr)")
        print("=" * 60 + "\n")
        print("Hello! Your income entry is safely logged.")
    else:
        print_banner("EXPENSE SUMMARY")
        print(f"Expense recorded: ₹{amount:.2f} (Dr), Tag: {tag}")
        print(f"Total Expense: ₹{total_expense:.2f} (Dr)")
        print(f"Current Balance: ₹{balance:.2f}")
        print("Well done staying on top of your expenses!")
    cursor.close()
    cnx.close()


def monthly_budget_planner(user_id):
    cnx, cursor = db_connect()
    print_banner("MONTHLY BUDGET PLANNER")
    try:
        budget = float(input("Enter your total monthly budget (₹): "))
        priorities = [input(f"Enter priority #{i+1} expense name: ") for i in range(3)]
        percents = []
        for p in priorities:
            while True:
                try:
                    val = int(input(f"Enter % allocation for {p}: "))
                    if 0 <= val <= 100:
                        percents.append(val)
                        break
                    else:
                        print("Must be between 0 and 100")
                except:
                    print("Enter a valid integer")
        total_pct = sum(percents)
        if total_pct > 100:
            print("Percentages exceed 100%. Cannot proceed.")
            cursor.close()
            cnx.close()
            return
        misc_pct = 100 - total_pct
        current_month = datetime.datetime.now().strftime("%Y-%m")
        cursor.execute(
            "INSERT INTO monthly_budget (user_id, month, budget, priority1, priority1_percent, priority2, priority2_percent, priority3, priority3_percent, miscellaneous_percent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                user_id,
                current_month,
                budget,
                priorities[0],
                percents[0],
                priorities[1],
                percents[1],
                priorities[2],
                percents[2],
                misc_pct,
            ),
        )
        cnx.commit()
        print("\nBudget Breakdown:")
        print(f"{'Category'.ljust(25)}{'Amount'.rjust(15)}{'Percent'.rjust(10)}")
        print("-" * 50)
        for p, t in zip(priorities, percents):
            amt = budget * t / 100
            print(f"{p.ljust(25)}{str(round(amt, 2)).rjust(15)}{str(t).rjust(10)}%")
        misc_amt = budget * misc_pct / 100
        print(
            f"{'Miscellaneous'.ljust(25)}{str(round(misc_amt, 2)).rjust(15)}{str(misc_pct).rjust(10)}%"
        )
        print("=" * 50)
        print("Great job on planning your budget for the month!")
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def bill_splitter(user_id):
    cnx, cursor = db_connect()
    print_banner("BILL SPLITTER")
    try:
        total = float(input("Enter total bill amount: "))
        while True:
            people = input("Enter number of people: ")
            if people.isdigit() and int(people) > 0:
                people = int(people)
                break
            else:
                print("Enter a valid positive integer")
        share = total / people
        cursor.execute(
            "INSERT INTO bill_splits (user_id, bill_amount, num_people, per_person_share) VALUES (%s,%s,%s,%s)",
            (user_id, total, people, share),
        )
        cnx.commit()
        print(f"Each person should pay: ₹{share:.2f}")
        print("Bill split completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def tax_calculator(user_id):
    cnx, cursor = db_connect()
    print_banner("TAX CALCULATOR")
    try:
        income = float(input("Enter annual income (₹): "))
        slabs = [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)]
        remaining = income
        tax = 0
        for slab, rate in slabs:
            taxable = min(remaining, slab)
            tax += taxable * rate
            remaining -= taxable
            if remaining <= 0:
                break
        effective_rate = (tax / income) * 100 if income > 0 else 0
        cursor.execute(
            "INSERT INTO tax_calculations (user_id, income, tax, effective_rate) VALUES (%s,%s,%s,%s)",
            (user_id, income, tax, effective_rate),
        )
        cnx.commit()
        print(f"Tax due: ₹{tax:.2f}")
        print(f"Effective tax rate: {effective_rate:.2f}%")
        print("Tax calculation done. Keep your records updated!")
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def compound_interest(user_id):
    cnx, cursor = db_connect()
    print_banner("COMPOUND INTEREST CALCULATOR")
    try:
        principal = float(input("Principal amount (₹): "))
        monthly_contrib = float(input("Monthly contribution (₹): "))
        years = float(input("Investment duration (years): "))
        rate = float(input("Annual interest rate (%): "))
        variance = float(input("Variance (%): "))
        freq_map = {"annual": 1, "quarterly": 4, "monthly": 12}
        freq = input("Compounding frequency (annual/quarterly/monthly): ").lower()
        if freq not in freq_map:
            print("Invalid frequency")
            cursor.close()
            cnx.close()
            return
        n = freq_map[freq]
        months = int(years * 12)
        rates = [rate - variance, rate, rate + variance]
        plt.figure(figsize=(10, 6))
        summaries = []
        for r in rates:
            balance = []
            amount = principal
            for month in range(months + 1):
                if n == 12:
                    monthly_rate = r / 100 / 12
                    amount = amount * (1 + monthly_rate) + monthly_contrib
                else:
                    if month % (12 // n) == 0 and month != 0:
                        monthly_rate = r / 100 / n
                        amount = amount * (1 + monthly_rate)
                    amount += monthly_contrib
                balance.append(amount)
            plt.plot(range(months + 1), balance, label=f"{r:.1f}%")
            interest_earned = balance[-1] - principal - monthly_contrib * months
            summaries.append(
                f"At {r:.1f}% total: {balance[-1]:.2f} (Interest earned: {interest_earned:.2f})"
            )
        plt.title("Compound Interest Over Time")
        plt.xlabel("Months")
        plt.ylabel("Balance (₹)")
        plt.legend()
        plt.show()
        cursor.execute(
            "INSERT INTO compound_interest_records (user_id, principal, monthly_contrib, years, annual_rate, variance, frequency, final_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (user_id, principal, monthly_contrib, years, rate, variance, freq, balance[-1]),
        )
        cnx.commit()
        print("\nSummary:")
        for s in summaries:
            print(s)
        print("Compound interest calculated! Your financial future looks bright!")
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def savings_calculator(user_id):
    cnx, cursor = db_connect()
    print_banner("SAVINGS CALCULATOR")
    try:
        saving = float(input("Monthly saving (₹): "))
        years = float(input("Duration (years): "))
        rate = float(input("Expected annual return (%): "))
        months = int(years * 12)
        r = rate / 100 / 12
        balances = [0]
        for _ in range(months):
            balances.append(balances[-1] * (1 + r) + saving)
        plt.figure(figsize=(10, 6))
        plt.plot(range(months + 1), balances, label="Savings Growth")
        plt.title("Savings Over Time")
        plt.xlabel("Months")
        plt.ylabel("Balance (₹)")
        plt.legend()
        plt.show()
        cursor.execute(
            "INSERT INTO savings_records (user_id, monthly_saving, years, annual_return, final_balance) VALUES (%s,%s,%s,%s,%s)",
            (user_id, saving, years, rate, balances[-1]),
        )
        cnx.commit()
        print(f"Total savings after {years} years: ₹{balances[-1]:.2f}")
        print("Savings goal on track! Keep it up!")
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def currency_converter(user_id):
    cnx, cursor = db_connect()
    print_banner("CURRENCY CONVERTER")
    print("Supported currencies:")
    for k, v in CURRENCIES.items():
        print(f"{k} - {v}")

    c = CurrencyRates()
    try:
        while True:
            amount = float(input("Enter amount: "))
            from_curr = input("From currency code: ").upper()
            to_curr = input("To currency code: ").upper()
            if from_curr not in CURRENCIES or to_curr not in CURRENCIES:
                print("Invalid currency code.")
                continue

            use_fixed_rates = input(
                "Use fixed offline rates instead of live rates? (yes/no): "
            ).lower()

            if use_fixed_rates == "yes":
                try:
                    # Conversion logic using fixed rates
                    if from_curr == "INR":
                        converted = convert_inr_to_currency(amount, to_curr)
                    elif to_curr == "INR":
                        converted = convert_currency_to_inr(amount, from_curr)
                    else:
                        # Convert from from_curr to INR, then INR to to_curr
                        inr_amount = convert_currency_to_inr(amount, from_curr)
                        converted = convert_inr_to_currency(inr_amount, to_curr)
                    print(f"{amount:.2f} {from_curr} = {converted:.4f} {to_curr}")
                except ValueError as ve:
                    print(ve)
                    continue
            else:
                # Live conversion using API
                converted = c.convert(from_curr, to_curr, amount)
                print(f"{amount:.2f} {from_curr} = {converted:.2f} {to_curr}")

            cursor.execute(
                "INSERT INTO currency_conversions (user_id, from_currency, to_currency, amount, converted_amount) VALUES (%s,%s,%s,%s,%s)",
                (user_id, from_curr, to_curr, amount, converted),
            )
            cnx.commit()
            print("Currency conversion successful!")
            again = input("Convert another? (yes/no): ").lower()
            if again != "yes":
                break
    except Exception as e:
        print(f"Error: {e}")
    cursor.close()
    cnx.close()


def main_menu():
    print_banner("USER MENU")
    print("1. Monthly Budget Planner")
    print("2. Bill Splitter")
    print("3. Tax Calculator")
    print("4. Compound Interest Calculator")
    print("5. Currency Converter")
    print("6. Savings Calculator")
    print("7. Record Income/Expense")
    print("8. Logout")
    return input("Select an option (1-8): ")


def main():
    create_all_tables()
    print_banner("WELCOME TO COLLEGE FINANCE BOT")
    user_id = None
    while True:
        choice = input("Are you a new user or returning? (new/login): ").lower()
        if choice == "new":
            register_user()
        elif choice == "login":
            user_id = login_user()
            if user_id:
                print("Hello! Ready to assist you with your finances.")
                break
        else:
            print("Invalid choice.")
    while True:
        choice = main_menu()
        if choice == "1":
            monthly_budget_planner(user_id)
        elif choice == "2":
            bill_splitter(user_id)
        elif choice == "3":
            tax_calculator(user_id)
        elif choice == "4":
            compound_interest(user_id)
        elif choice == "5":
            currency_converter(user_id)
        elif choice == "6":
            savings_calculator(user_id)
        elif choice == "7":
            record_entry(user_id)
        elif choice == "8":
            print("Goodbye! Have a great day!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
