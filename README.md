# College Finance Bot

A comprehensive personal finance management system designed for college students to track expenses, plan budgets, and make informed financial decisions.

## Overview

College Finance Bot is a Python-based command-line application that provides students with essential financial management tools. The system utilizes MySQL for persistent data storage and includes visualization capabilities for financial projections.

## Features

### Core Functionality

**Monthly Budget Planner**
Set budget allocations across three priority categories with percentage-based planning and automatic miscellaneous budget calculation.

**Income and Expense Tracker**
Record and categorize all financial transactions with predefined income tags and custom expense categories.

**Bill Splitter**
Calculate individual shares when splitting bills among multiple people.

**Tax Calculator**
Compute income tax based on Indian tax slabs with effective tax rate calculation.

**Compound Interest Calculator**
Project investment growth with customizable parameters including variance scenarios and multiple compounding frequencies (annual, quarterly, monthly).

**Savings Calculator**
Calculate long-term savings growth with expected annual returns and visual projections.

**Currency Converter**
Convert between ten major world currencies using either live exchange rates or fixed offline rates.

### User Management

- Secure user registration and authentication system
- Individual user accounts with isolated financial data
- Complete transaction history maintenance
- Session-based user access control

### Data Visualization

- Interactive matplotlib charts for investment and savings projections
- Multiple interest rate scenario comparisons
- Time-series visualization of financial growth

## Technical Stack

- **Programming Language:** Python 3.x
- **Database:** MySQL Server
- **Visualization Library:** matplotlib
- **Currency API:** forex-python
- **Database Connector:** mysql-connector-python

## System Requirements

### Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- Internet connection (for live currency conversion rates)

### Required Python Packages

- mysql-connector-python
- matplotlib
- forex-python

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/college-finance-bot.git
cd college-finance-bot
```

### Step 2: Install Dependencies

```bash
pip install mysql-connector-python
pip install matplotlib
pip install forex-python
```

### Step 3: Configure Database Connection

Modify the database configuration in the script:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "college_finance_db"
}
```

### Step 4: Initialize and Run

```bash
python Finance_Bot_FMM.py
```

The application will automatically create the necessary database and table structures upon first execution.

## Usage Guide

### Initial Setup

1. Launch the application
2. Select "new" for first-time registration
3. Create credentials (username: minimum 3 characters, password: minimum 6 characters)
4. Login with your newly created credentials

### Main Menu Functions

**Option 1: Monthly Budget Planner**
Configure your monthly budget by specifying total amount and allocating percentages across three priority expense categories. The system automatically calculates remaining miscellaneous budget.

**Option 2: Bill Splitter**
Input total bill amount and number of participants to calculate per-person share.

**Option 3: Tax Calculator**
Enter annual income to compute tax liability based on Indian tax slabs and view effective tax rate.

**Option 4: Compound Interest Calculator**
Input principal amount, monthly contributions, investment duration, annual interest rate, variance percentage, and compounding frequency to visualize investment growth scenarios.

**Option 5: Currency Converter**
Convert amounts between supported currencies using live or fixed exchange rates.

**Option 6: Savings Calculator**
Calculate projected savings balance based on monthly savings amount, duration, and expected annual return.

**Option 7: Record Income/Expense**
Add financial transactions with appropriate categorization and automatic balance tracking.

**Option 8: Logout**
Terminate current session and exit application.

### Income Entry Categories

The system supports the following predefined income tags:

- salary: Regular employment income
- bonus: Performance-based bonuses
- interest: Interest earnings from deposits
- investment: Returns from investments
- gift: Monetary gifts received
- other: Miscellaneous income sources

Expense entries allow custom tags for flexible categorization.

## Supported Currencies

The currency converter module supports the following currencies:

| Code | Currency Name |
|------|---------------|
| INR | Indian Rupee |
| USD | US Dollar |
| EUR | Euro |
| GBP | British Pound |
| JPY | Japanese Yen |
| AUD | Australian Dollar |
| CAD | Canadian Dollar |
| CHF | Swiss Franc |
| CNY | Chinese Yuan |
| NZD | New Zealand Dollar |

## Database Architecture

The application implements a relational database structure with eight tables:

**users**
Stores user authentication credentials and unique identifiers.

**entries**
Records all income and expense transactions with timestamps and categorization.

**monthly_budget**
Maintains monthly budget plans with priority allocations.

**bill_splits**
Logs bill splitting calculations and per-person shares.

**tax_calculations**
Archives tax computation history with effective rates.

**compound_interest_records**
Stores investment projection parameters and results.

**currency_conversions**
Maintains currency conversion transaction history.

**savings_records**
Records savings calculation parameters and projected balances.

## Security Considerations

This application is designed as an educational project. For production deployment, implement the following security enhancements:

- Replace plain-text password storage with secure hashing algorithms (bcrypt, argon2, or PBKDF2)
- Store database credentials in environment variables rather than hardcoded values
- Implement prepared statements consistently to prevent SQL injection vulnerabilities
- Add comprehensive input validation and sanitization
- Implement secure session management with timeout mechanisms
- Add encryption for sensitive financial data at rest and in transit
- Implement proper access control and authorization mechanisms
- Add audit logging for sensitive operations
- Implement rate limiting to prevent abuse

## Contributing

Contributions to this project are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch from main
3. Implement your changes with appropriate documentation
4. Write or update tests as necessary
5. Submit a pull request with a clear description of changes

Please ensure your code follows PEP 8 style guidelines and includes appropriate comments.

## Future Development Roadmap

The following enhancements are planned for future releases:

- Web-based user interface for improved accessibility
- Mobile application for iOS and Android platforms
- Data export functionality (Excel, PDF, CSV formats)
- Recurring expense and income tracking
- Budget vs. actual spending analysis with variance reporting
- Financial goal setting and progress tracking
- Investment portfolio management and performance analysis
- Receipt scanning with OCR integration
- Multi-currency account support
- Automated expense categorization using machine learning
- Financial insights and recommendations engine
- Integration with banking APIs for automatic transaction import

## License

This project is licensed under the MIT License. See the LICENSE file for complete terms and conditions.

## Author

[Your Name]
GitHub: [@Java-Mx](https://github.com/java-mx)

## Acknowledgments

This project utilizes:
- Indian Income Tax slabs as per current government taxation policy
- Exchange rates provided by forex-python API
- MySQL database management system
- Python matplotlib library for data visualization

Developed as an academic project for practical application of database management and financial calculation concepts.

## Contact and Support

For questions, bug reports, or feature requests:
- Open an issue in the GitHub repository
- Email: ashwinchhawaniya2@gmail.com

## Documentation

For detailed API documentation and advanced usage examples, please refer to the project wiki.
