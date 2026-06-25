import time, datetime
import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient
import psycopg2

#----------Global Variables----------#
load_dotenv() #looks for and finds '.env' file 
API_KEY = os.getenv("COINBASE_API_KEY") #extracts and saves API KEY from env file
SECRET_KEY = os.getenv("COINBASE_SECRET_KEY")
has_bought = False
coinbase_client = RESTClient(api_key=API_KEY, api_secret=SECRET_KEY #variable as your exclusive secure walkie-talkie to Coinbase-
                    ) #It has your credentials built right into it.
DB_USER = os.getenv("DB_USER") #Database variables to initialize db container connection
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = 'crypto-db'
COMMODITIES = ['XRP','BTC','ETH','SOL','ADA','LINK','AVAX','DOT','HBAR','LTC','DOGE','SHIB','XTZ','BCH','APT','XLM']

#----------Database----------#
#-Connection-#
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()
#-Tables-#
cursor.execute("""
    CREATE TABLE IF NOT EXISTS commodity_history (
               id SERIAL PRIMARY KEY,
               symbol VARCHAR(10) NOT NULL,
               price NUMERIC NOT NULL,
               timestamp TIMESTAMP NOT NULL
    );
""")
conn.commit() #Commits data to the database permananently
print("Commodity database table confirmed/created succesfully!", flush = True)

#--------------------^ INFRASTRUCTURE ^/v ALGORITHMS v--------------------#

#----------LOOP----------#
print("Deploying commodity asset injector engine...")
while True:
    for symbol in COMMODITIES:
        try:
            product_id = f"{symbol}-USD"

            #-Data Retreival-#
            product = coinbase_client.get_product(product_id)
            price_string = product.price or product.price
            current_price = float(price_string)

            cursor.execute( #Inserting metrics into Postgre database
                "INSERT INTO commodity_history (symbol, price, timestamp) VALUES (%s,%s,%s);",
                (symbol, current_price, datetime.datetime.now())
            )
            conn.commit()

            print(f"[{symbol}] has been logged at {current_price}", flush=True)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}", flush=True)
        time.sleep(1)
    print("---Completed retreival cycle for all 16, starting next batch...", flush=True)
    time.sleep(30)

#----------NOTES----------#
    # print(f"Status Code: {response.status_code} Response Text: {response.text}")
    # response = requests.get(BASE_URL)
    # data_dict = response.json()