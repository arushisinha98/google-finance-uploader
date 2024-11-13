# google-finance-uploader

Migrate your trades to Google Finance to track your portfolios in one place!

1. Create a virtual environment
`$ python -m venv env`
2. Install all dependencies
`$ python -m pip install -r requirements.txt`
3. Run the script
`$ python main.py`


How it works:

- The script will first read all the excel or csv files in `data/` and ask you to pick one to upload.
- The script will ask you which columns contain the transaction date, instrument, quantity, and (optionally) transaction price information. Note that transaction price is not necessary as this field can be auto-populated by Google Finance.
- The script will ask you to log into Google Finance and choose a portfolio to add the transactions into.
- Once confirmed, the script will iteratively add all the transactions in the file to your Google Finance Portfolio. Any skips or failures are logged and output as separate csv files along with the reason. Note that Google Finance does not currently support fractional sells so these will be skipped by the script.


Tips:
- Ensure that buys are denoted by +ve quantities and sells are denoted by -ve quantities.
- Check that all the instruments you wish to add are available on Google Finance.
- For international stock exchanges, include the currency code in the instrument (e.g. instead of `D05`, try `D05 SG` or instead of `2801` try `2801 HK`) to ensure that the Google Finance dropdown is more likely to pick the stock you intended.