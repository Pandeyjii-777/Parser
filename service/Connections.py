from models import Database, Kafka
import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.environ.get("HOST_NAME")
database = os.environ.get("DATABASE")
username = os.environ.get("USERNAME")
pwd = os.environ.get("PASSWORD")
port_id = os.environ.get("PORT_ID")
conn = os.environ.get("CONN")

# print(os.environ.get("RANDOM"))

database = Database.Database(hostname, database, username, pwd, port_id)
cur = database.get_cursor()
conn = database.get_connection()

servers = os.environ.get("BOOTSTRAP_SERVERS")
api = os.environ.get("API_VERSION")

# kafka = Kafka.Kafka(servers, api)
# producer = kafka.get_producer()