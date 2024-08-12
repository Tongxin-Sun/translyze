import sys
import json
import os
import time
import shutil
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style, init
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def dynamic_print(text, delay=0.02):
    """
    Print text dynamically to simulate typing effect.

    Args:
        text (string): The text to be printed.
        delay (float, optional): The delay between each character in seconds. 
            Defaults to 0.1.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def welcome():
    """
    Display the welcome page.
    Ask if the user wants to view the user guide, or want to proceed.
    """
    welcome_message = """
===================================================================
  Welcome to Translyzer! 👋👋👋

  Translyzer is a bank statement analysis application.

  Upload all your bank statements. Translyzer helps to combine
  and present them in one place, calculating your overall
  expenses, and producing an analysis report in seconds!

  🆕 New to Translyzer? Press 'U' to view user guide.

  OR

  Press 'N' to proceed.


  [Press Ctrl + C to exit the program at any time.]
===================================================================
"""
    dynamic_print(welcome_message, 0.02)


def display_user_guide():
    user_guide = """
===================================================================
                        USER GUIDE

  Translyzer helps you to streamline the following tasks:

  📤 Upload your bank statements (CSV files)
     - Upload all the bank statements that you want to analyze.
       Translyzer will help combine them.

  🧾 View Transactions
     - View and edit transactions to correct any details.

  📊 Generate an Expense Summary
     - View all your expenses. You can also optionally view       
       expenses by category.

  📈 Generate a Detailed Analysis Report (PDF)
     - Generate a detailed analysis report at any time.
       Want to save more time? Choose this option after uploading
       your bank statements, and get a report in seconds!

  If you're ready, press 'N' to proceed to upload bank statements.

  [Press Ctrl + C to Exit the Program at Any Time]
  ===================================================================
    """
    dynamic_print(user_guide, 0.02)
    handle_user_choice()
        


def handle_user_choice():
    choice = input("Please enter your choice: _").strip().upper()
    if choice == 'U':
        display_user_guide()
    elif choice == 'N':
        upload_files()
    else:
        print("Your input is invalid. Please try again.")


def create_folder(folder_name):
    """_
    Create a folder if it does not exist.
    If the folder exists, delete all files in the folder to make it empty.
    """
    if os.path.exists(folder_name):
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(folder_name)


def copy_files_to_folder(files):
    """_
    Move the list of files to the specified folder.
    """
    create_folder('bank-statements')
    moved_files = []
    for file in files:
        try:
            file_name = os.path.basename(file)
            destination = os.path.join('bank-statements', file_name)
            shutil.copy2(file, destination)
            moved_files.append(destination)
        except Exception as e:
            print(f"Error copying file {file}: {e}")
    return moved_files


def upload_files():
    """
    Upload files based on user input.
    """
    combined_data = []
    upload_prompt(combined_data)
       
    print("Great! Your file is being prepared...")
    for _ in tqdm(range(100), desc="Preparing file", ncols=75, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        time.sleep(0.03)  # Simulate work being done
      
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_df.index.name = 'ID'
        #combined_df.to_csv('combined_bank_statements.csv', index=False)
        print("Successful!")
        
    display_menu(combined_df)


def upload_prompt(combined_data):
    upload_prompt = """
===================================================================
  Let's start by uploading all your bank statements.             

  ⚠️ Bank statements should be .csv files.
  
  Please upload one file at a time. When finish, enter 'done'.
  
  For each file, you will be asked several questions to ensure accurate preprocessing of the data.
  On average, it will take approximately 50 seconds per file to complete this process.

"""
    dynamic_print(upload_prompt, 0.02)
    
    file_paths = []
    
    while True:
        dynamic_print("===================================================================")
        file_path = input("Enter the path of the CSV file (or 'done' to finish): _")
        file_paths.append(file_path)
        print()

        if file_path.lower() == 'done':
            print(df)
            break
        
        account_name = input("Enter a nickname for this account (optional): _").strip().capitalize()
        print()
        account_type = input("Is this a Debit or Credit card account (Debit/Credit)? _").strip().capitalize()
        print()
        date_col = input("What is the column header for the date column? _").strip().capitalize()
        print()
        desc_col = input("What is the column header for the description column? _").strip().capitalize()
        print()
        amount_col = input("What is the column header for the amount column? _ ").strip().capitalize()
        print()
        category_col =input("What is the column header for the category column? _").strip().capitalize()
        print()
        is_negative_spending = input("Is spending represented by negative numbers and income by positive numbers? (y/n) _").strip().lower()
        print()
        
        df = preprocess_bank_statement(file_path, account_name, account_type, date_col, desc_col, amount_col, category_col, is_negative_spending)
        
        if not df.empty:
            combined_data.append(df)
         
        print()   
        dynamic_print("Uploaded bank statements: ")
        for i, path in enumerate(file_paths):
            file_name = os.path.basename(path)
            dynamic_print(f"{i + 1}. {file_name}")
        print()
        undo_redo(file_paths, combined_data)
        
    
def undo_redo(file_paths, combined_data):
    while True:
        choice = input("Press 'R' to redo this file, 'U' to undo the last file, or 'N' to continue: ").strip().upper()
        if choice == 'R':
            print("Redoing file upload...")
                    # The user will re-enter the information for this file
            file_paths.pop()  # Remove the last file path
            combined_data.pop()  # Remove the last DataFrame
            break  # Break out to start again with the redo
        elif choice == 'U':
            print("Undoing the last file upload...")
                    # Remove the last file and DataFrame
            file_paths.pop()
            combined_data.pop()
            break  # Break out to start again with the undo
        elif choice == 'N':
            break  # Continue to next file
        else:
            print("Invalid input. Please enter 'R' to redo, 'U' to undo, or 'N' to continue.")

def preprocess_bank_statement(file_path, account_name, account_type, date_col, desc_col, amount_col, category_col, is_negative_spending):
    try:
        df = pd.read_csv(file_path, index_col=False)
        
        df.columns = [col.capitalize() for col in df.columns]
        
        df = df.rename(columns={
            date_col: 'Date',
            desc_col: 'Description',
            amount_col: 'Amount',
            category_col: 'Category'
        })
        
        if is_negative_spending == 'n':
            df['Amount'] = df['Amount'] * -1
        
        df['Account Name'] = account_name
        df['Account Type'] = account_type
        
        df = df[['Account Name', 'Account Type', 'Date', 'Description', 'Amount', 'Category']]
        return df

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return pd.DataFrame()
    

def display_menu(df):
    menu = """
========================================================
  Your bank statements are now ready for analysis!    
                                                      
                    MAIN MENU           
                                                      
  1. View Transactions                                
  2. View Expense Summary
  3. View Income Summary                             
  4. Generate Analysis Report (PDF)                   
                                                      
                                                      
  [Press Ctrl + C to Exit the Program at Any Time]           
========================================================
    """
    print(menu)
    
    handle_menu_choice(df)
    
    
def handle_menu_choice(df):
    choice = input("Enter your choice: ")
    
    if choice == '1':
        display_transactions(df)
    elif choice == '2':
        display_expense(df)
    elif choice == '3':
        display_income(df)
    elif choice == '4':
        generate_report(df)
        
        
def display_transactions(df):
    print("=========================================================================")
    print(df)
    print("""

   1. Edit Transaction
   2. Delete Transaction
   3. Consolidate Category

  [Press B to Go Back to Main Menu]              
  [Press Ctrl + C to Exit the Program at any time]
                                    
=========================================================================    
          """)
    while True:
        choice = input().upper()
        if choice == '1':
            edit_a_transaction(df)
            break
        elif choice == '2':
            delete_a_transaction(df)
            break
        elif choice == '3':
            consolidate_category(df)
            break
        elif choice == 'B':
            display_menu(df)
            break
        else:
            print("Invalid input. Please enter 'D' to Delete a Transaction or 'B' to Go Back to Main Menu.")


def get_user_input():
    """Prompts the user for input and returns it."""
    ID = input('Enter the transaction ID: ')
    col = input('Which field would you like to edit? (Account Name, Account Type, Date, Description, Amount, Category): ').strip().capitalize()
    new_value = input(f'Enter the new value for {col}: ')
    return ID, col, new_value


def create_request(ID, col, new_value, df):
    """Creates a request dictionary."""
    return {
        'Type': 'Request',
        'ID': ID,
        'Col': col,
        'New Value': new_value,
        'Data': df.to_dict()
    }


def write_request_to_file(request, file_path):
    """Writes the request dictionary to a file."""
    with open(file_path, 'w') as file:
        json.dump(request, file)


def read_response_from_file(file_path):
    """Reads the response dictionary from a file."""
    time.sleep(2)
    with open(file_path, 'r') as file:
        return json.load(file)


def process_response(df, file_path):
    """Processes the response and updates the DataFrame."""
    while True:
        try:
            response = read_response_from_file(file_path)
            if response['Type'] == 'Response':
                df = pd.DataFrame(response['Data'])
                print('Data has been successfully edited!\n')
                return df
        except json.decoder.JSONDecodeError:
            continue


def convert_value(col, value):
    """Converts the value to the appropriate type based on the column."""
    if col in ['Amount']:
        try:
            return float(value)
        except ValueError:
            print(f"Warning: Unable to convert '{value}' to float. Using original value.")
            return value
    return value


def edit_a_transaction(df):
    ID, col, new_value = get_user_input()
    new_value = convert_value(col, new_value)
    request = create_request(ID, col, new_value, df)
    write_request_to_file(request, '../transaction-editor/communication.txt')
    df = process_response(df, '../transaction-editor/communication.txt')
    display_transactions(df)


def delete_a_transaction(df):
    try:
        transaction_id = int(input("Enter the ID of the transaction you want to delete: "))
        
        # Check if the transaction ID exists in the DataFrame
        if transaction_id not in df.index:
            print(f"Transaction ID {transaction_id} does not exist.")
            return

        # Extract the transaction details
        transaction = df.loc[transaction_id]
        
        # Display transaction details and confirm deletion
        print(f"\n⚠️ Are you sure you want to delete the following transaction?\n"
              f"   ID: {transaction_id}\n"
              f"   Date: {transaction['Date']}\n"
              f"   Description: {transaction['Description']}\n"
              f"   Amount: ${transaction['Amount']}\n"
              f"   Category: {transaction['Category']}\n")
        
        confirm = input("[Press Y to Confirm Deletion] [Press N to Cancel]: ").upper()
        
        if confirm == 'Y':
            # Drop the transaction from the DataFrame
            df = df.drop(transaction_id)
            dynamic_print(f"\nTransaction ID {transaction_id} deleted successfully!!\n")
        else:
            dynamic_print("\nDeletion cancelled.\n")
            
        display_transactions(df)
    
    except ValueError:
        print("Invalid input. Please enter a valid transaction ID.")


def consolidate_category(df):
    category_list = input(
        "Please enter the categories you want to merge, separated by commas"
        " (e.g., 'Shopping, Entertainment'): "
        )
    new_category = input("Enter the name for the new combined category: "
                         ).strip()
    request = {
        'Type': 'Request',
        'Category List': category_list,
        'New Category': new_category,
        'Data': df.to_dict()
        }
    write_request_to_file(request, '../category-consolidator/communication.txt')
    df = process_response(df, "../category-consolidator/communication.txt")
    display_transactions(df)


def request_to_microserviceA(m):
    
    with open('./transaction-calculator/commpipe.txt', 'w') as request_file:
        request_file.write(str(m))
    time.sleep(2)
    with open('./transaction-calculator/commpipe.txt', 'r') as response_file:
        amount = response_file.readline()
    return amount
            

def display_expense(df):
    total_expense = df[df['Amount'] < 0]['Amount'].sum()
    total_expense_str = f"${abs(total_expense):.2f}"
    df.to_csv('./transaction-calculator/dataframe.txt', index=False)
    highest_expense = request_to_microserviceA(1)
    time.sleep(10)
    lowest_expense = request_to_microserviceA(2)
    time.sleep(2)
    average_expense = request_to_microserviceA(3)
    
    def display_expense_summary():
        summary = f"""
=========================================================================
  View Overall Expense                                                 
                                                                       
  Here is the summary of your overall expenses:                        
                                                                       
  -------------------------------------------------                    
  | Total Expense                                  |                   
  |------------------------------------------------|                   
  | {total_expense_str}                            |
  |------------------------------------------------|
  | Highest Expense                                |
  |------------------------------------------------|
  | {highest_expense}                              |
  |------------------------------------------------|
  | Lowest Expense                                 |
  |------------------------------------------------|
  | {lowest_expense}                               |
  |------------------------------------------------|
  | Average Expense                                |
  |------------------------------------------------|
  | {average_expense}                              |                   
  --------------------------------------------------                   
                                                                       
  [+] Detailed Expense by Category:                                    
  (Press D to show/hide details)                                       
                                                                       
                                                                       
  [Press B to Go Back to Main Menu]                                    
  [Press Ctrl + C to Exit the Program at any time]                            
=========================================================================
        """
        print(summary)
    
    def display_detailed_expense():
        print(f"""
=========================================================================
  View Overall Expense                                                 
                                                                       
  Here is the summary of your overall expenses:                        
  [Press D to show a detailed list of expenses by category]            
                                                                       
  --------------------------------------------------                   
  | Total Expense                                  |                   
  |------------------------------------------------|                   
  | {total_expense_str}                            |                   
  --------------------------------------------------                   
                                                                       
  [-] Detailed Expense by Category:                                    
  (Press D to show/hide details)                                       
                                                                       
  ----------------------------------------------------                 
  | Category                    | Amount             |                 
  |-----------------------------|--------------------|                        
              """)
        grouped = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().abs().reset_index()
        for _, row in grouped.iterrows():
            print(f"  | {row['Category']:<30} | ${row['Amount']:<9.2f}  |")
        print("|  --------------------------------------------------------------------|")
        print("""                                                                       
  [Press B to Go Back to Main Menu]                                    
  [Press Ctrl + C to Exit the Program at any time]                            
========================================================================= """)
    
    display_expense_summary()
    detailed_view = False
    
    while True:
        choice = input().upper()
        if choice == 'D':
            detailed_view = not detailed_view
            if detailed_view:
                display_detailed_expense()
            else:
                display_expense_summary()
            
        elif choice == 'B':
            display_menu(df)
            break
        else:
            print("Invalid input. Please press D, B, or X.")


def generate_report(df):
    """
    Generates a report from the combined transactions DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the combined bank statements.

    Returns:
        None
    """
    # Ensure the Amount column is numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # Total expenses (assuming expenses are negative values)
    total_expenses = df[df['Amount'] < 0]['Amount'].sum()
    
    # Expenses by category
    expenses_by_category = df[df['Amount'] < 0].groupby('Category')['Amount'].sum()
    
    # Prepare report content
    report_content = [
        "Bank Statement Analysis Report",
        "==============================",
        f"Total Expenses: ${-total_expenses:.2f}",  # Display expenses as positive values
        "",
        "Expenses by Category:",
        "----------------------",
    ]
    
    for category, amount in expenses_by_category.items():
        report_content.append(f"{category}: ${-amount:.2f}")  # Display expenses as positive values

    # Create PDF
    c = canvas.Canvas("report.pdf", pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 50, "Bank Statement Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 70, "==============================")
    
    # Total Expenses
    c.drawString(30, height - 90, f"Total Expenses: ${-total_expenses:.2f}")  # Display expenses as positive values
    
    # Expenses by Category
    c.drawString(30, height - 130, "Expenses by Category:")
    c.drawString(30, height - 150, "----------------------")
    
    y = height - 170
    for category, amount in expenses_by_category.items():
        c.drawString(30, y, f"{category}: ${-amount:.2f}")  # Display expenses as positive values
        y -= 20
    
    # Save PDF
    c.save()
    dynamic_print("Report is saved to report.pdf")
    display_menu(df)

# Example usage:
# Assuming transactions_df is your DataFrame containing the combined bank statements
# transactions_df = pd.DataFrame(...)  # Load or create your DataFrame here
# generate_report(transactions_df, 'bank_statement_report.txt')

    pass


def main():
    init()
    try:
        # Ensure the console uses UTF-8 encoding
        sys.stdout.reconfigure(encoding='utf-8')

        welcome()

        handle_user_choice()

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit()


if __name__ == "__main__":
    main()
