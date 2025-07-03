Usage
Installation
To install on local machine or PC:

pip install nse[local]
This will additionally install the requests library.

# server parameter set to False
nse = NSE(download_folder='', server=False)
To install on server like AWS or other cloud services.

pip install nse[server]
This will additionally install httpx library with http2 support.

# Make sure to set server parameter to True.
nse = NSE(download_folder='', server=True)
Example
from nse import NSE
from pathlib import Path

# Working directory
DIR = Path(__file__).parent

nse = NSE(download_folder=DIR)

status = nse.status()

nse.exit() # close requests session
Using ‘with’ statement
with NSE(download_folder=DIR) as nse:
    status = nse.status()
API
class nse.NSE(download_folder: str | Path, server: bool = False, timeout: int = 15)
An Unofficial Python API for the NSE India stock exchange.

Methods will raise
TimeoutError if request takes too long.

ConnectionError if request failed for any reason.

Parameters:
download_folder (pathlib.Path or str) – A folder/dir to save downloaded files and cookie files

server (bool) – A parameter to specify whether the script is being run on a server (like AWS, Azure, Google Cloud etc). True if running on a server, False if run locally.

timeout (int) – Default 15. Network timeout in seconds

Raises:
ValueError – if download_folder is not a folder/dir

ImportError – If server set to True and httpx[http2] is not installed or ``server set to False and requests is not installed.

General Methods
NSE.exit()
Close the requests session.

Use at the end of script or when class is no longer required.

Not required when using the ``with`` statement.

NSE.status() → List[Dict]
Returns market status

Sample response

Returns:
Market status of all NSE market segments

Return type:
list[dict]

NSE.holidays(type: Literal['trading', 'clearing'] = 'trading') → Dict[str, List[Dict]]
NSE holiday list

CM key in dictionary stands for Capital markets (Equity Market).

Sample response

Parameters:
type (str) – Default trading. One of trading or clearing

Returns:
Market holidays for all market segments.

Return type:
dict[str, list[dict]]

NSE.blockDeals() → Dict
Block deals

Sample response

Returns:
Block deals. data key is a list of all block deal (Empty list if no block deals).

Return type:
dict

NSE.bulkdeals(fromdate: datetime, todate: datetime) → List[Dict]
Download the bulk deals report for the specified date range and return the data.

Sample response

Parameters:
fromdate (datetime.datetime) – Start date of the bulk deals report to download

todate (datetime.datetime) – End date of the bulk deals report to download

Raises:
ValueError – if the date range exceeds one year.

RuntimeError – if no bulk deals data is available for the specified date range.

Returns:
Bulk deals data

Return type:
dict

Stocks Quotes and Market info
NSE.equityMetaInfo(symbol) → Dict
Meta info for equity symbols.

Provides useful info like stock name, code, industry, ISIN code, current status like suspended, delisted etc.

Also has info if stock is an FnO, ETF or Debt security

Sample response

Parameters:
symbol (str) – Equity symbol code

Returns:
Stock meta info

Return type:
dict

NSE.quote(symbol, type: Literal['equity', 'fno'] = 'equity', section: Literal['trade_info'] | None = None) → Dict
Price quotes and other data for equity or derivative symbols

Sample response

For Market cap, delivery data and order book, use pass section=’trade_info’ as keyword argument. See sample response below:

Sample response

Parameters:
symbol (str) – Equity symbol code

type (str) – One of equity or fno. Default equity

section – Optional. If specified must be trade_info

Raises:
ValueError – if section does not equal trade_info

Returns:
Price quote and other stock meta info

Return type:
dict

NSE.equityQuote(symbol) → Dict[str, str | float]
A convenience method that extracts date and OCHLV data from NSE.quote for given stock symbol

Sample response

Parameters:
symbol (str) – Equity symbol code

Returns:
Date and OCHLV data

Return type:
dict[str, str or float]

NSE.gainers(data: Dict, count: int | None = None) → List[Dict]
Top gainers by percent change above zero.

Sample response

Parameters:
data (dict) –

Output of one of NSE.listSME, NSE.listEquityStocksByIndex

count (int) – Optional. Limit number of result returned

Returns:
List of top gainers

Return type:
list[dict]

NSE.losers(data: Dict, count: int | None = None) → List[Dict]
Top losers by percent change below zero.

Sample response

Parameters:
data (dict) –

Output of one of NSE.listSME, NSE.listEquityStocksByIndex

count (int) – Optional. Limit number of result returned

Returns:
List of top losers

Return type:
list[dict]

NSE.advanceDecline() → List[Dict[str, str]]
Deprecated since version 1.0.9: Removed in v1.0.9 as url no longer active.

Use nse.listEquityStocksByIndex

NSE.fetch_index_names() → Dict[str, List[Tuple[str, str]]]
Returns a dict with a list of tuples. Each tuple contains the short index name and full name of the index.

The full name can be passed as index parameter to fetch_historical_index_data()

NSE.fetch_equity_historical_data(symbol: str, from_date: date | None = None, to_date: date | None = None, series: List[str] = ['EQ']) → List[Dict]
Downloads the historical daily price and volume data for a specified symbol within a given date range, from from_date to to_date.

The data is returned as a JSON object, where the primary data is stored as a list of rows (indexed starting at 0).

Each row is represented as a dict, with column names as keys and their corresponding values.

The date is stored under the key mTIMESTAMP.

If the provided symbol is incorrect or invalid, an empty JSON will be returned.

Sample response

Parameters:
symbol (str) – The exchange-traded symbol for which the data needs to be downloaded e.g. HDFCBANK, SGBAPR28I or GOLDBEES

from_date (datetime.date) – The starting date from which we fetch the data. If None, the default date is 30 days from to_date.

to_date (datetime.date) – The ending date upto which we fetch the data. If None, today’s date is taken by default.

series – The series for which we need to fetch the data. A list of the series containing elements from the below list

Raises:
ValueError – if from_date is greater than to_date

TypeError – if from_date or to_date is not of type datetime.date

Returns:
Data as a list of rows, each row as dictionary with key as column name mapped to the value

Return type:
List[Dict]

The list of valid series
AE

AF

BE

BL

EQ

IL

RL

W3

GB

GS

NSE.fetch_historical_vix_data(from_date: date | None = None, to_date: date | None = None) → List[Dict]
Downloads the historical India VIX within a given date range from from_date to to_date.

The data is returned as a JSON object, where the primary data is stored as a list of rows (indexed starting at 0).

Each row is represented as a dict, with column names as keys and their corresponding values.

The date is stored under the key EOD_TIMESTAMP.

Sample response

Parameters:
from_date (datetime.date) – The starting date from which we fetch the data. If None, the default date is 30 days from to_date.

to_date (datetime.date) – The ending date upto which we fetch the data. If None, today’s date is taken by default.

Raises:
ValueError – if from_date is greater than to_date

TypeError – if from_date or to_date is not of type datetime.date

Returns:
Data as a list of rows, each row as dictionary with key as column name mapped to the value

Return type:
List[Dict]

NSE.fetch_historical_fno_data(symbol: str, instrument: Literal['FUTIDX', 'FUTSTK', 'OPTIDX', 'OPTSTK', 'FUTIVX'] = 'FUTIDX', from_date: date | None = None, to_date: date | None = None, expiry: date | None = None, option_type: Literal['CE', 'PE'] | None = None, strike_price: float | None = None) → List[dict]
Downloads the historical futures and options data within a given date range from from_date to to_date.

Reference url: https://www.nseindia.com/report-detail/fo_eq_security

The data is returned as a list of rows (indexed starting at 0).

Each row is represented as a dict, with column names as keys and their corresponding values.

Sample response

Parameters:
symbol (str) – Symbol name.

instrument – Default FUTIDX. Instrument name can be one of FUTIDX, FUTSTK, OPTIDX, OPTSTK, FUTIVX.

from_date (datetime.date) – Optional. The starting date from which we fetch the data. If None, the default date is 30 days from to_date.

to_date (datetime.date) – Optional. The ending date upto which we fetch the data. If None, today’s date is taken by default.

expiry (datetime.date) – Optional. Expiry date of the instrument to filter results.

option_type (str) – Optional. Filter results by option type. Must be one of CE or PE

strike_price (Optional[float]) – Optional. Filter results by option type. Must be one of CE or PE

Raises:
ValueError – if from_date is greater than to_date or if instrument is an Option and option_type is not specified.

TypeError – if from_date or to_date or expiry is not of type datetime.date.

Returns:
Data as a list of rows, each row as dictionary with key as column name mapped to the value

Return type:
List[Dict]

NSE.fetch_historical_index_data(index: str, from_date: date | None = None, to_date: date | None = None) → Dict[str, List[dict]]
Downloads the historical index data within a given date range from from_date to to_date.

Reference url: https://www.nseindia.com/reports-indices-historical-index-data

The data is returned as a dict object with price and turnover as keys. The values are stored as a list of rows (indexed starting at 0).

Each row is represented as a dict, with column names as keys and their corresponding values.

See list of acceptable values for index parameter.

Warning

While the NSE API returns the entire date range, date values in price and turnover may not be in sync due to turnover containing additional dates.

Sample response

Parameters:
index (str) – The name of the Index.

from_date (datetime.date) – The starting date from which we fetch the data. If None, the default date is 30 days from to_date.

to_date (datetime.date) – The ending date upto which we fetch the data. If None, today’s date is taken by default.

Raises:
ValueError – if from_date is greater than to_date

TypeError – if from_date or to_date is not of type datetime.date

Returns:
A dictionary with price and turnover as keys and the data as a list of rows, each row is dictionary.

Return type:
Dict[str, List]

NSE.fetch_fno_underlying() → Dict[str, List[Dict[str, str]]]
Fetches the indices and stocks for which FnO contracts are available to trade

Reference URL: https://www.nseindia.com/market-data/securities-available-for-trading

Returns:
A dictionary with keys ‘IndexList’ and ‘UnderlyingList’. The values are the list of indices and stocks along with their names and tickers respectively in alphabetical order for stocks.

Return type:
Dict[str, List[Dict[str, str]]]

List Stocks
NSE.listFnoStocks()
Deprecated since version 1.0.9: Removed in version 1.0.9,

Use nse.listEquityStocksByIndex(index=’SECURITIES IN F&O’)

NSE.listEquityStocksByIndex(index='NIFTY 50') → dict
List Equity stocks by their Index name. Defaults to NIFTY 50

See list of acceptable values for index argument.

Sample response

Returns:
A dictionary. The data key is a list of all stocks represented by a dictionary with the symbol name and other metadata.

NSE.listIndices() → dict
List all indices

Sample response

Returns:
A dictionary. The data key is a list of all Indices represented by a dictionary with the symbol code and other metadata.

NSE.listIndexStocks(index)
Deprecated since version 1.0.9: Removed in version 1.0.9.

Use nse.listEquityStocksByIndex

NSE.listEtf() → dict
List all etf stocks

Sample response

Returns:
A dictionary. The data key is a list of all ETF’s represented by a dictionary with the symbol code and other metadata.

NSE.listSme() → dict
List all sme stocks

Sample response

Returns:
A dictionary. The data key is a list of all SME’s represented by a dictionary with the symbol code and other metadata.

NSE.listSgb() → dict
List all sovereign gold bonds

Sample response

Returns:
A dictionary. The data key is a list of all SGB’s represented by a dictionary with the symbol code and other metadata.

List IPOs
NSE.listCurrentIPO() → List[Dict]
List current IPOs

Sample response

Returns:
List of Dict containing current IPOs

Return type:
List[Dict]

NSE.listUpcomingIPO() → List[Dict]
List upcoming IPOs

Sample response

Returns:
List of Dict containing upcoming IPOs

Return type:
List[Dict]

NSE.listPastIPO(from_date: datetime | None = None, to_date: datetime | None = None) → List[Dict]
List past IPOs

Sample response

Parameters:
from_date (datetime.datetime) – Optional defaults to 90 days from to_date

to_date (datetime.datetime) – Optional defaults to current date

Raises:
ValueError – if to_date is less than from_date

Returns:
List of Dict containing past IPOs

Return type:
List[Dict]

NSE Circulars
NSE.circulars(subject: str | None = None, dept_code: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None) → dict
Return exchange circulars and communications by Department

Sample response

Parameters:
subject – Optional keyword string used to filter circulars based on their subject.

dept_code (str) – Optional Department code. See table below for options

from_date (datetime.datetime) – Optional defaults to 7 days from to_date

to_date (datetime.datetime) – Optional defaults to current date

Raises:
ValueError – if to_date is less than from_date

Below is the list of dept_code values and their description

CMTR - Capital Market (Equities) Trade

COM - Commodity Derivatives

CC - Corporate Communications

CRM - CRM & Marketing

CD - Currency Derivatives

DS - Debt Segment

SME - Emerge

SMEITP - Emerge-ITP

FAAC - Finance & Accounts

FAO - Futures & Options

INSP - Inspection & Compliance

LEGL - Legal, ISC & Arbitration

CMLS - Listing

MA - Market Access

MSD - Member Service Department

MEMB - Membership

MF - Mutual Fund

NWPR - New Products

NCFM - NSE Academy Limited

CMPT - NSE Clearing - Capital Market

IPO - Primary Market Segment

RDM - Retail Debt Market

SLBS - Securities Lending & Borrowing Scheme

SURV - Surveillance & Investigation

TEL - Systems & Telecom

UCIBD - UCI Business Development

WDTR - Wholesale Debt Market

Download NSE reports
Reports are saved to filesystem and a pathlib.Path object is returned.

By default, all methods save the file to the download_folder specified during initialization. Optionally all methods accept a folder argument if wish to save to another folder.

Zip files are automatically extracted and saved to file.

NSE.fetch_daily_reports_file_metadata(segment: Literal['CM', 'INDEX', 'SLBS', 'SME', 'FO', 'COM', 'CD', 'NBF', 'WDM', 'CBM', 'TRI-PARTY'] = 'CM') → Dict
Returns file metadata for daily reports.

The returned dictionary contains info about current day and previous day reports.

Useful for checking if a report is ready and updated.

Parameters:
segment (Literal["CM", "INDEX", "SLBS", "SME", "FO", "COM", "CD", "NBF", "WDM", "CBM", "TRI-PARTY"]) – The market segment to retrieve metadata. Defaults to CM.

Returns:
A dictionary containing metadata about the daily report files for the specified segment.

Return type:
Dict

NSE.equityBhavcopy(date: datetime, folder: str | Path | None = None) → Path
Download the daily Equity bhavcopy report for specified date and return the saved filepath.

Parameters:
date (datetime.datetime) – Date of bhavcopy to download

folder (pathlib.Path or str) – Optional folder/dir path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a folder/dir.

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved file

Return type:
pathlib.Path

NSE.deliveryBhavcopy(date: datetime, folder: str | Path | None = None) → Path
Download the daily Equity delivery report for specified date and return saved file path.

Parameters:
date (datetime.datetime) – Date of delivery bhavcopy to download

folder (pathlib.Path or str) – Optional folder/dir path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a folder/dir

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved file

Return type:
pathlib.Path

NSE.indicesBhavcopy(date: datetime, folder: str | Path | None = None) → Path
Download the daily Equity Indices report for specified date and return the saved file path.

Parameters:
date (datetime.datetime) – Date of Indices bhavcopy to download

folder (pathlib.Path or str) – Optional folder/dir path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a folder/dir

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved file

Return type:
pathlib.Path

NSE.pr_bhavcopy(date: datetime, folder: str | Path | None = None) → Path
Download the daily PR Bhavcopy zip report for specified date and return the saved zipfile path.

The file returned is a zip file containing a collection of various reports.

It includes a Readme.txt, explaining the contents of each file and the file naming format.

Parameters:
date (datetime.datetime) – Report date to download

folder (pathlib.Path or str) – Optional folder path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a dir/folder

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved zip file

Return type:
pathlib.Path

from datetime import datetime
from zipfile import ZipFile

import pandas as pd
from nse import NSE

dt = datetime(2024, 9, 15)

with NSE("") as nse:
  # Download the PR bhavcopy zip file
  zipped_file = nse.pr_bhavcopy(dt)

# Extract all files into current folder
with ZipFile(zipped_file) as zip:
  zip.namelist() # get the list of files
  zip.extractall()

# OR Load a file named HL150924.csv from the zipfile into a Pandas DataFrame
with ZipFile(zipped_file) as file:
  with zip.open(f"HL{dt:%d%m%Y}.csv") as f:
      df = pd.read_csv(f, index_col="Symbol")
NSE.fnoBhavcopy(date: datetime, folder: str | Path | None = None) → Path
Download the daily Udiff format FnO bhavcopy report for specified date and return the saved file path.

Parameters:
date (datetime.datetime) – Date of FnO bhavcopy to download

folder (pathlib.Path or str) – Optional folder path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a dir/folder

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved file

Return type:
pathlib.Path

NSE.priceband_report(date: datetime, folder: str | Path | None = None) → Path
Download the daily priceband report for specified date and return the saved file path.

Parameters:
date (datetime.datetime) – Report date to download

folder (pathlib.Path or str) – Optional folder path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a dir/folder

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved file

Return type:
pathlib.Path

NSE.cm_mii_security_report(date: datetime, folder: str | Path | None = None) → Path
Download the daily CM MII security file report for specified date and return the saved and extracted file path.

The file returned is a csv file.

Parameters:
date (datetime.datetime) – Report date to download

folder (pathlib.Path or str) – Optional folder path to save file. If not specified, use download_folder specified during class initializataion.

Raises:
ValueError – if folder is not a dir/folder

FileNotFoundError – if download failed or file corrupted

RuntimeError – if report unavailable or not yet updated.

Returns:
Path to saved zip file

Return type:
pathlib.Path

NSE.download_document(url: str, folder: str | Path | None = None) → Path
Download the document from the specified URL and return the saved file path. If the downloaded file is a zip file, extracts its contents to the specified folder.

Parameters:
url (str) – URL of the document to download e.g. https://archives.nseindia.com/annual_reports/AR_ULTRACEMCO_2010_2011_08082011052526.zip

folder (pathlib.Path or str or None) – Folder path to save file. If not specified, uses download_folder from class initialization.

Raises:
ValueError – If folder is not a directory

FileNotFoundError – If download failed or file corrupted

RuntimeError – If file extraction fails

Returns:
Path to saved file (or extracted file if zip)

Return type:
pathlib.Path

This method is useful for downloading attachments from announcements, actions etc. See code example below

from nse import NSE

with NSE(download_folder="") as nse:
    announcements = nse.announcements()

    for dct in announcements:
        # Only download the first pdf attachment
        if "attchmntFile" in dct and ".pdf" in dct["attchmntFile"]:
            filepath = nse.download_document(dct["attchmntFile"])
            print(filepath)  # saved file path
            break
Corporate Announcements and Actions
NSE.actions(segment: Literal['equities', 'sme', 'debt', 'mf'] = 'equities', symbol: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None) → List[Dict]
Get all forthcoming corporate actions.

Sample response

If symbol is specified, only actions for the symbol is returned.

If from_data and to_date are specified, actions within the date range are returned

Parameters:
segment (str) – One of equities, sme, debt or mf. Default equities

symbol (str or None) – Optional Stock symbol

from_date (datetime.datetime) – Optional from date

to_date (datetime.datetime) – Optional to date

Raises:
ValueError – if from_date is greater than to_date

Returns:
A list of corporate actions

Return type:
list[dict]

NSE.announcements(index: Literal['equities', 'sme', 'debt', 'mf', 'invitsreits'] = 'equities', symbol: str | None = None, fno=False, from_date: datetime | None = None, to_date: datetime | None = None) → List[Dict]
Get all corporate announcements for current date.

If symbol is specified, only announcements for the symbol is returned.

If from_date and to_date are specified, announcements within the date range are returned

Sample response

Parameters:
index (str) – One of equities, sme, debt or mf. Default equities

symbol (str or None) – Optional Stock symbol

fno (bool) – Only FnO stocks

from_date (datetime.datetime) – Optional from date

to_date (datetime.datetime) – Optional to date

Raises:
ValueError – if from_date is greater than to_date

Returns:
A list of corporate actions

Return type:
list[dict]

NSE.boardMeetings(index: Literal['equities', 'sme'] = 'equities', symbol: str | None = None, fno: bool = False, from_date: datetime | None = None, to_date: datetime | None = None) → List[Dict]
Get all forthcoming board meetings.

If symbol is specified, only board meetings for the symbol is returned.

If from_date and to_date are specified, board meetings within the date range are returned

Sample response

Parameters:
index (str) – One of equities or sme. Default equities

symbol (str or None) – Optional Stock symbol

fno (bool) – Only FnO stocks

from_date (datetime.datetime) – Optional from date

to_date (datetime.datetime) – Optional to date

Raises:
ValueError – if from_date is greater than to_date

Returns:
A list of corporate board meetings

Return type:
list[dict]

NSE.annual_reports(symbol: str, segment: Literal['equities', 'sme'] = 'equities') → Dict[str, List[Dict[str, str]]]
Returns the dictionary containing the list of annual reports of the symbol for every year.

Each dictionary within the list contains the link to the annual report in PDF format.

with NSE("") as nse:
    annual_reports = nse.annual_reports(symbol="HDFCBANK")

    file = nse.download_document(annual_reports["data"][0]["fileName"])

    print(file) # filepath of downloaded annual report
Sample response

Parameters:
symbol (str) – Stock symbol for which annual reports are to be fetched.

segment (Literal["equities", "sme"]) – One of equities or sme. Default is equities.

Returns:
A dictionary where keys are years and values are lists of dictionaries with PDF links to annual reports.

Return type:
dict[str, list[dict[str, str]]]

Futures and Options (FnO)
NSE.getFuturesExpiry(index: Literal['nifty', 'banknifty', 'finnifty'] = 'nifty') → List[str]
Get current, next and far month expiry as a sorted list with order guaranteed.

Its easy to calculate the last thursday of the month. But you need to consider holidays.

This serves as a lightweight lookup option.

Parameters:
index (str) – One of nifty, banknifty, finnifty. Default nifty.

Returns:
Sorted list of current, next and far month expiry

Return type:
list[str]

NSE.fnoLots() → Dict[str, int]
Get the lot size of FnO stocks.

Sample response

Returns:
A dictionary with symbol code as keys and lot sizes for values

Return type:
dict[str, int]

NSE.optionChain(symbol: Literal['banknifty', 'nifty', 'finnifty', 'niftyit'] | str) → Dict
Unprocessed option chain from NSE for Index futures or FNO stocks

Sample response

Parameters:
symbol (str) – FnO stock or index futures code. For Index futures, must be one of banknifty, nifty, finnifty, niftyit

Returns:
Option chain for all expiries

Return type:
dict

NSE.compileOptionChain(symbol: str | Literal['banknifty', 'nifty', 'finnifty', 'niftyit'], expiryDate: datetime) → Dict[str, str | float | int]
Filter raw option chain by expiryDate and calculate various statistics required for analysis. This makes it easy to build an option chain for analysis using a simple loop.

Statistics include:
Max Pain,

Strike price with max Call and Put Open Interest,

Total Call and Put Open Interest

Total PCR ratio

PCR for every strike price

Every strike price has Last price, Open Interest, Change, Implied Volatility for both Call and Put

Other included values: At the Money (ATM) strike price, Underlying strike price, Expiry date.

Sample response

Parameters:
symbol (str) – FnO stock or Index futures symbol code. If Index futures must be one of banknifty, nifty, finnifty, niftyit.

expiryDate (datetime.datetime) – Option chain Expiry date

Returns:
Option chain filtered by expiryDate

Return type:
dict[str, str | float | int]

static NSE.maxpain(optionChain: Dict, expiryDate: datetime) → float
Get the max pain strike price

Parameters:
optionChain (dict) – Output of NSE.optionChain

expiryDate (datetime.datetime) – Options expiry date

Returns:
max pain strike price

Return type:
float