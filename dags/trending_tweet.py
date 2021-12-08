import pandas as pd
import tweepy as tw

from sqlalchemy import create_engine
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG, Variable
from datetime import datetime

# Create Engine to Connect PostgreSQL
string_db = "postgresql+psycopg2://airflow:secure_password@localhost:5432/airflowdb"
engine = create_engine(string_db)

# Get Trending Topics in each Country (Extract)
def extract(api, trends_used):
    topic = []; country = [];  woeid = [];
    for trend in trends_used:
        print("Getting Trending Topic from {}".format(trend["name"]))
        trends_result = api.get_place_trends(trend["woeid"])

        topic.append(trends_result[0]["trends"][0]["name"])
        country.append(trend["name"])
        woeid.append(trend["woeid"])

    df_extract = pd.DataFrame({"topic": topic, "country": country, "woeid": woeid})
    print("Trending Data")
    print(df_extract, end="\n\n")

    return df_extract

# Get Existing Data from PostgreSQL
def existing_data(engine):
    with engine.connect() as conn:
        df_table = pd.read_sql("SELECT * FROM trending_topics WHERE stopped_at IS NULL", conn)
    print("Existing Data")
    print(df_table, end="\n\n")

    return df_table

# Combine Two Data from Extracted Data and Existing Data (Transform)
def transform(df_extract, df_table):
    df_transform = pd.merge(df_extract, df_table, how="outer", indicator=True).fillna({'ids':0}).astype({'ids': 'int64'})
    print("Combine Data")
    print(df_transform, end="\n\n")

    return df_transform

# Save Transform Data to PostgreSQL (Load)
def load(engine, df_transform):
    df_load = df_transform.loc[df_transform._merge != "both"].drop(["_merge","created_at","stopped_at"], axis=1)
    print(df_load, end="\n\n")

    def store_data(data):
        with engine.connect() as conn:
            if data["ids"] != 0:
                query = """
                UPDATE trending_topics
                SET stopped_at = CURRENT_TIMESTAMP
                WHERE ids = '{primary_key}'
                """.format(primary_key=data["ids"])
            else:
                query = """
                INSERT INTO trending_topics(topic, country, woeid)
                VALUES('{topic}','{country}','{woeid}')
                """.format(topic=data["topic"], country=data["country"], woeid=data["woeid"])
        
            print("{exc} Data with topic: {topic}, country: {country}".format(
                exc=query.split()[0], topic=data["topic"], country=data["country"]
            ))
            conn.execute(query)

    df_load.apply(store_data, axis=1)

# Collect & Store Data
def collect_store_data():

    # Authenticate to Twitter (Airflow Vairable)
    consumer_key = Variable.get("API_Key")
    consumer_secret = Variable.get("API_Key_Secret")
    access_token = Variable.get("Access_Token")
    access_token_secret = Variable.get("Access_Token_Secret")
    
    # Authenticate to Twitter (Localfile)
    #df_key = pd.read_csv("Twitter_API.csv")
    #consumer_key = df_key.loc[0, "API Key"]
    #consumer_secret = df_key.loc[0, "API Key Secret"]
    #access_token = df_key.loc[0, "Access Token"]
    #access_token_secret = df_key.loc[0, "Access Token Secret"]

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API Object
    api = tw.API(auth, wait_on_rate_limit=True)
    
    # Get WOEID in each Country
    trends_search = ["Indonesia", "Malaysia", "Thailand", "Singapore", "Philippines"]
    trends_availabe = api.available_trends()
    trends_used = [trend for trend in trends_availabe if trend["name"] in trends_search and trend["placeType"]["code"] == 12]

    # Create Table on PostreSQL (To Store Data)
    with engine.connect() as conn:
        result = conn.execute("""
        CREATE TABLE IF NOT EXISTS trending_topics (
            ids SERIAL PRIMARY KEY,
            topic VARCHAR(90) NOT NULL, 
            country VARCHAR(90) NOT NULL,
            woeid INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (current_timestamp),
            stopped_at TIMESTAMP
        );
        """)

    # ETL
    df_extract = extract(api, trends_used)
    df_table = existing_data(engine)
    df_transform = transform(df_extract, df_table)
    load(engine, df_transform)

# Calculate Time Differences
def cal_duration():
    with engine.connect() as conn:
        df_table = pd.read_sql("SELECT * FROM trending_topics", conn).drop(['ids'], axis=1)
    df_table["stopped_at"] = [d if not pd.isnull(d) else pd.Timestamp.now() for d in df_table['stopped_at']]
    print(df_table, end="\n\n")

    # Calculate Minutes between stopped_at & created_at
    df_table['duration'] = (df_table["stopped_at"] - df_table["created_at"]).astype('timedelta64[m]')
    df_result = df_table.groupby(['topic', 'country', 'woeid']).sum().reset_index()
    
    # Show Result to Logs
    print(df_result, end="\n\n")


default_arguments = {
    "owner": "Reza",
    "start_date": datetime(2021,12,8,12,15,0)
}

with DAG(
    "calculate_twitter_trending_topic_duration", 
    default_args=default_arguments, 
    schedule_interval="*/5 * * * *"
) as etl_dag:
    py_task1 = PythonOperator(
        task_id="get_trending_topic",
        python_callable=collect_store_data,
        dag=etl_dag
    )

    py_task2 = PythonOperator(
        task_id="calculate_time_trending",
        python_callable=cal_duration,
        dag=etl_dag
    )

    py_task1 >> py_task2

#collect_store_data()
#cal_duration()
