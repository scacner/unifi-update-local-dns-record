from getpass import getpass
from sshtunnel import SSHTunnelForwarder
import pymongo

MONGO_HOST = input('UniFi Gateway IP Address: ')
MONGO_DB = 'ace'
MONGO_USER = 'root'
MONGO_PASS = getpass('UniFi Gateway SSH Password: ')
SSH_PORT = 27117
DEVICE_KEY = input('Column name containing the unique client device value from user collection (e.g. "last_ip"): ')
DEVICE_VALUE = input('Value of client device for the above key (e.g. "192.168.1.42"): ')
MONGO_COLLECTION = 'user'
SET_KEY = 'local_dns_record'

server = SSHTunnelForwarder(
	MONGO_HOST,
	ssh_username=MONGO_USER,
	ssh_password=MONGO_PASS,
	remote_bind_address=('127.0.0.1', SSH_PORT)
)
server.start()
client = pymongo.MongoClient(
	'127.0.0.1', server.local_bind_port
) # server.local_bind_port is assigned local port

db = client[MONGO_DB]

# Access the 'user' collection
collection = db[MONGO_COLLECTION]

# Find the document with the right key/value pair
document = collection.find_one({DEVICE_KEY: DEVICE_VALUE})

current_value = document[SET_KEY]
full_key_string = f'{MONGO_HOST}:{MONGO_DB}:{MONGO_COLLECTION}:{DEVICE_VALUE}:{SET_KEY}'
print(f'Current value of {full_key_string} = "{current_value}"')

new_value = input('New value for Local DNS Record (e.g. "*.local.mydomain.com" ) ["q" or empty input to quit]: ')

if new_value.strip().lower() not in ('q', ''):
	print(f'Updating {full_key_string} to "{new_value}"')
	collection.update_one({DEVICE_KEY: DEVICE_VALUE}, {'$set': {SET_KEY: new_value}})
	document = collection.find_one({DEVICE_KEY: DEVICE_VALUE})
	current_value = document[SET_KEY]
	print(f'{full_key_string} updated; current value = {current_value}')
	print('If the UniFi Network app does not show the updated Local DNS Record, the Gateway may need to be restarted.')

else:
	print(f'No update performed. Closing connection to {MONGO_HOST}')

client.close()
server.stop()
