from connection.connect_db import open_connection
from query_execution.batting import batting_data

source_connection = open_connection("source")
destination_connection = open_connection("destination")

batting_data(source_connection, destination_connection)