import csv
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from cassandra import ConsistencyLevel

sqlCreateEntryTable = """
                CREATE TABLE municipalityDB.sensors_entries( 
                sensor_entry_id int PRIMARY KEY, 
                created_at timestamp,
                entry_id int,
                temperature decimal,
                humidity decimal, 
                Enviroment text 
                )
            """

print("Mbateyoooogha : %2d, Portal : %5.2f" % (1, 05.333)) 

# Connect to Cassandra cluster
cluster = Cluster(['cassandra'], port=9042)

session = cluster.connect()

session.execute("CREATE KEYSPACE IF NOT EXISTS municipalityDB WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }") 
session.execute('DROP TABLE IF EXISTS municipalitydb.sensors_entries')
session.execute(sqlCreateEntryTable)

# Prepare batch statement
batch = BatchStatement()

with open("Data/SensorsData.csv", "r") as file:
    csvReader = csv.DictReader(file)

    number = 0
    for row in csvReader:      
        number = number + 1
       
        batch.add(SimpleStatement("INSERT INTO municipalitydb.sensors_entries (sensor_entry_id, created_at, entry_id, Temperature, Humidity, Enviroment) VALUES (%s, %s, %s, %s, %s, %s)"), 
                                                                                                                                (number, 
                                                                                                                                row['created_at'],
                                                                                                                                int(row['entry_id']),
                                                                                                                                float(row['Temperature']),
                                                                                                                                float(row['Humidity']),
                                                                                                                                row['Enviroment']
                                                                                                                                ))
# Execute batch insert
session.execute(batch)

# Close connection
cluster.shutdown()
