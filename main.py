import sys


def display_welcome_page():
    welcome_message = """
===================================================================
|  Welcome to Translyzer! 👋👋👋                                 |
|                                                                 |
|  Translyzer is a bank statement analysis application.           |
|                                                                 |
|  Upload all your bank statements. Translyzer helps to combine   |
|  and present them in one place, calculating your overall        |
|  expenses, and producing an analysis report in seconds!         |
|                                                                 |
|  New to Translyzer? Here’s how to get started:                  |
|                                                                 |
|  📤 Upload your bank statements (CSV files)                     |
|    - Upload all the bank statements that you want to analyze.   |
|      Translyzer will help combine them.                         |
|                                                                 |
|  🧾 View Transactions                                           |
|    - View and edit transactions to correct any details.         |
|                                                                 |
|  📊 Generate an Expense Summary                                 |
|    - View all your expenses. You can also optionally view       |
|      expenses by category.                                      |
|                                                                 |
|  📈 Generate a Detailed Analysis Report (PDF)                   |
|    - Generate a detailed analysis report at any time.           |
|      Want to save more time? Choose this option after uploading |
|      your bank statements, and get a report in seconds!         |
|                                                                 |
|  [Press X to Exit the Program at Any Time]                      |
|                                                                 |
===================================================================
"""
    print(welcome_message)


def main():
    display_welcome_page()

    # Press X will exit the program
    while True:
        user_input = input().strip().upper()

        if user_input == 'X':
            print("Exiting the program...")
            sys.exit()


if __name__ == "__main__":
    main()
