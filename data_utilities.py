import os

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