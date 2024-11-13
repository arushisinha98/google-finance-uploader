from datetime import datetime
import pandas as pd


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
