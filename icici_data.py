import yfinance as yf
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Initialize MongoDB connection
client = MongoClient('mongodb+srv://kusuma:kusuma123@cluster0.vbc433c.mongodb.net/?retryWrites=true&w=majority')  # Change this connection URL to match your MongoDB setup
db = client['icici_bank_data']

# Define the ticker symbol and the date range for the week
ticker = 'ICICIBANK.NS'
start_date = datetime(2023, 10, 23)  # Change the start date to the desired week's start date
end_date = start_date + timedelta(days=2)

# Function to fetch and store stock data
def fetch_and_store_data():
    # Calculate the current time and round it to the nearest 15-minute interval
    current_time = datetime.now()
    rounded_time = current_time.replace(second=0, microsecond=0)
    rounded_time = rounded_time - timedelta(minutes=rounded_time.minute % 15)

    # Fetch ICICI Bank data for the given time
    icici_data = yf.download(ticker, start=rounded_time, end=rounded_time + timedelta(minutes=15), progress=False)

    # Convert the data to a list of dictionaries
    icici_data_dict = icici_data.reset_index().to_dict(orient='records')

    # Store the data in the MongoDB database
    collection = db[rounded_time.strftime('%Y-%m-%d')]
    collection.insert_one({"data": icici_data_dict})

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_data, 'interval', minutes=15, start_date=start_date.replace(hour=11, minute=15),
                  end_date=end_date.replace(hour=14, minute=15))
scheduler.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
