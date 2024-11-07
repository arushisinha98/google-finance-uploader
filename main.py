import os
import pandas as pd
from assistant import GoogleFinanceAutomator
from datetime import datetime


import os
import pandas as pd
from assistant import GoogleFinanceAutomator
from datetime import datetime

class UploadTracker:
    def __init__(self, filename):
        self.skipped_rows = []
        self.failed_rows = []
        self.filename = filename
        
    def add_skipped(self, row, reason):
        """Track skipped transaction"""
        self.skipped_rows.append({**row, 'reason': reason})
        
    def add_failed(self, row, error):
        """Track failed transaction"""
        self.failed_rows.append({**row, 'error': str(error)})
        
    def save_report(self):
        """Save skipped and failed transactions to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d')
        
        if self.skipped_rows:
            skipped_df = pd.DataFrame(self.skipped_rows)
            skipped_df.to_csv(f'{self.filename}-SKIPPED-{timestamp}Upload.csv', index=False)
            print(f"\nSkipped transactions saved to: {self.filename}-SKIPPED_{timestamp}Upload.csv")
            
        if self.failed_rows:
            failed_df = pd.DataFrame(self.failed_rows)
            failed_df.to_csv(f'{self.filename}-FAILED-{timestamp}Upload.csv', index=False)
            print(f"Failed transactions saved to: {self.filename}-FAILED-{timestamp}Upload.csv")


def get_excel_files(directory='data'):
    """Recursively find all Excel files in directory and subdirectories"""
    excel_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.xlsx', '.csv')):
                excel_files.append(os.path.join(root, file))
    return excel_files

def display_files(files):
    """Display files with numbering"""
    print("\nAvailable files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

def verify_column(df, column_name):
    """Verify if column exists in dataframe"""
    if not column_name:
        return True  # Empty column name is valid for optional fields
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in file")
        return False
    return True

def get_column_input(df, column_type, optional=False):
    """Get and verify column input from user"""
    while True:
        prompt = f"Select the {column_type} column"
        if optional:
            prompt += " (leave empty if not in data)"
        prompt += ": "
        
        column = input(prompt).strip()
        
        if optional and not column:
            return None
            
        if verify_column(df, column):
            return column

        print("Please try again.")


def main():

    # Step 1: Read all Excel files
    excel_files = get_excel_files()
    if not excel_files:
        print("No Excel or CSV files found in data/ directory")
        return

    # Step 2: Display files
    display_files(excel_files)

    # Step 3: Get user choice
    while True:
        try:
            choice = int(input("\nChoose a file number: "))
            if 1 <= choice <= len(excel_files):
                selected_file = excel_files[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(excel_files)}")
        except ValueError:
            print("Please enter a valid number")

    # Step 4: Read and display selected file
    print(f"\nReading {selected_file}")
    try:
        df = pd.read_excel(selected_file) if selected_file.endswith('.xlsx') else pd.read_csv(selected_file)
        print("\nFile headers:")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return

    # Step 5: Get column mappings
    ticker_col = get_column_input(df, "TICKER")
    quantity_col = get_column_input(df, "QUANTITY")
    date_col = get_column_input(df, "PURCHASE DATE")
    price_col = get_column_input(df, "PURCHASE PRICE", optional=True)

    if not all([ticker_col, quantity_col, date_col]):  # price_col is optional
        print("Required columns not found. Exiting.")
        return
    
    # Step 6: Initialize Google Finance Automator
    print("\nInitializing Google Finance Automator...")
    automator = GoogleFinanceAutomator()
    tracker = UploadTracker(selected_file[:selected_file.rfind('.')])

    # Start manual process
    if not automator.start_manual_process():
        print("Failed to initialize Google Finance. Exiting.")
        return

    # Modified investment processing loop
    successful_additions = 0
    
    for index, row in df.iterrows():
        try:
            quantity = float(row[quantity_col])
            
            # Skip negative quantities
            if quantity <= 0:
                print(f"Skipping row {index + 1}: Negative or zero quantity")
                tracker.add_skipped(
                    row.to_dict(),
                    "Negative or zero quantity"
                )
                continue
            
            # Prepare investment data
            symbol = str(row[ticker_col])
            purchase_date = pd.to_datetime(row[date_col], dayfirst=True).strftime('%m/%d/%Y')
            purchase_price = float(str(row[price_col]).replace('$','').replace(',','')) if price_col else None
            
            # Add investment
            success = automator.add_investment(
                symbol=symbol,
                quantity=quantity,
                purchase_date=purchase_date,
                purchase_price=purchase_price
            )
            
            if success:
                successful_additions += 1
                print(f"Added investment {successful_additions}: {symbol}")
            else:
                tracker.add_failed(
                    row.to_dict(),
                    "Failed to add investment"
                )
                
        except Exception as e:
            print(f"Error processing row {index + 1}: {str(e)}")
            tracker.add_failed(
                row.to_dict(),
                str(e)
            )
            continue
    
    # Print summary
    print(f"\n{successful_additions} investments successfully added to portfolio.")
    print(f"{len(tracker.skipped_rows)} transactions skipped")
    print(f"{len(tracker.failed_rows)} transactions failed")
    
    # Save report of skipped and failed transactions
    tracker.save_report()
    
    # Clean up
    try:
        automator.close()
    except:
        pass

if __name__ == "__main__":
    main()