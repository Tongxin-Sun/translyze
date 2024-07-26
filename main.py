import sys
import os
import time
import shutil
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style, init


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
    upload_prompt = """
===================================================================
  Let's start by uploading all your bank statements.             

  ⚠️ Bank statements should be .csv files.
  
  Please upload one file at a time. When finish, enter 'done'.

"""
    dynamic_print(upload_prompt, 0.02)
    
    combined_data = []
    file_paths = []
    
    while True:
        dynamic_print("===================================================================")
        file_path = input("Enter the path of the CSV file (or 'done' to finish): _")
        file_paths.append(file_path)
        print()

        if file_path.lower() == 'done':
            dynamic_print(Fore.GREEN + "Do you want to finish uploading and "
                            "start analysis?\nYou won't be able to upload "
                            "additional bank statements later: (y/n)" + Style.RESET_ALL)
            is_done = input().strip().upper()
            if is_done == 'Y':
                break
            else:
                continue
        
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
       
    print("Great! Your file is being prepared...")
    for _ in tqdm(range(100), desc="Preparing file", ncols=75, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        time.sleep(0.03)  # Simulate work being done
      
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        combined_df.index.name = 'ID'
        #combined_df.to_csv('combined_bank_statements.csv', index=False)
        print("Successful!")
        
    display_menu(combined_df)


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
            df['Amount'] = pd['Amount'] * -1
        
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
  3. Generate Analysis Report (PDF)                   
                                                      
                                                      
  [Press Ctrl + C to Exit the Program at Any Time]           
========================================================
    """
    dynamic_print(menu)
    
    handle_menu_choice(df)
    
    
def handle_menu_choice(df):
    choice = input("Enter your choice: ")
    
    if choice == '1':
        display_transactions(df)
    elif choice == '2':
        display_expense(df)
    elif choice == '3':
        generate_report(df)
        
        
def display_transactions(df):
    print("=========================================================================")
    print(df)
    print("""
          
          
  [Press D to Delete a Transaction]                                    
  [Press B to Go Back to Main Menu]                                    
  [Press Ctrl + C to Exit the Program at any time]                            
                                                                       
=========================================================================    
          """)
    while True:
        choice = input().upper()
        if choice == 'D':
            delete_a_transaction(df)
            break
        elif choice == 'B':
            display_menu(df)
            break
        else:
            print("Invalid input. Please enter 'D' to Delete a Transaction or 'B' to Go Back to Main Menu.")


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


def display_expense(df):
    total_expense = df[df['Amount'] < 0]['Amount'].sum()
    total_expense_str = f"${abs(total_expense):.2f}"
    
    def display_expense_summary():
        summary = f"""
=========================================================================
  View Overall Expense                                                 
                                                                       
  Here is the summary of your overall expenses:                        
                                                                       
  -------------------------------------------------                    
  | Total Expense                                  |                   
  |------------------------------------------------|                   
  | {total_expense_str}                            |                   
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
