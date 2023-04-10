# %% Import Python packages
import requests
import psycopg
from getpass import getpass


# %% OData API URLs
base_url = "https://ghoapi.azureedge.net/api"
indicator_url = "https://ghoapi.azureedge.net/api/Indicator"

indicator_response = requests.get(indicator_url)

indicator_json = indicator_response.json()
print("The dimensions of the raw data list is:",len(indicator_json))
print("The raw data's type is:",type(indicator_json))

print('\nThe raw data elements are identified by:')
count = 1
for value in indicator_json:
    print(count,")", value)
    count += 1

print("\nThe number of available indicators is:",len(indicator_json['value']))

print("\nA single indicators raw data is shown below")
# print(indicator_json['@odata.context'])
# print(type(indicator_json['value']))
print(indicator_json['value'][0])
print(indicator_json['value'][1]['IndicatorCode'])
print("The data type here is:",type(indicator_json['value'][0]))

print('\nThis raw data can be pulled out into key and value elements as:')
for keys in indicator_json['value'][0]:
    print(keys,": ", indicator_json['value'][0][keys])
print('\n')



# %% Set up and interface with my local PostgreSQL server

# Setting the database and user for faster iteration
dbuser = "postgres" # default user in my local PostgreSQL server
dbname = "worlddata" # database created to house WHO data

# Create new database session an existing database
with psycopg.connect(dbname=dbname, user=dbuser, password=getpass(prompt="Enter your password for {}:".format(dbuser))) as conn:
    print("Successfully connected to the database, '{}', as user, '{}'".format(dbname, dbuser))
    
    # Create a cursor to perform database operations
    with conn.cursor() as cur:

        # Show all existing tables in the database
        cur.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            """    
        )
        # Copy the list of existing tables from SQL into a Python object
        existingTables = []
        print("The existing tables in the {} database are:".format(dbname))
        for table in cur.fetchall():
            existingTables.append(table[0])
        print(existingTables)


        # Show contents of each existing table
        for i in range(len(existingTables)):
            cur.execute("SELECT * FROM {}".format(existingTables[i]))
            print("For the table: {}, some example data is shown as:".format(existingTables[i]))
            print(cur.fetchmany(3))



        # Copy all data from indicator_json object to the SQL database
        # with cur.copy("COPY indicators (IndicatorCode, IndicatorName) FROM STDIN") as copy:
        #     for i in indicator_json['value']:
        #         copy.write_row(indicator_json['value'][i])

        # exceptCount = 0
        # for i in range(len(indicator_json['value'])):
        # # for i in range(5):
        #     try:
        #         cur.execute(
        #         "INSERT INTO indicators (IndicatorCode, IndicatorName) VALUES (%s , %s)",
        #         (indicator_json['value'][i]['IndicatorCode'],indicator_json['value'][i]['IndicatorName'])
        #         )   
        #     except:
        #         exceptCount += 1
        #         i += 1
        # print("The number of exceptions is:", exceptCount)

        
        # Create new table. If it already exists, the script fails.
        # cur.execute(
        #     """
        #     CREATE TABLE test (
        #         id serial PRIMARY KEY,
        #         num integer,
        #         data text
        #     )
        #     """
        # )

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion
        # cur.execute(
        #     "INSERT INTO test (num, data) VALUES (%s, %s)",
        #     (100,"abc'def")
        # )

        # Show contents of each existing table
        print('\n')
        for i in range(len(existingTables)):
            cur.execute("SELECT * FROM {}".format(existingTables[i]))
            print("For the table: {}, some example data is shown as:".format(existingTables[i]))
            print(cur.fetchmany(3))


        # Pull data from psql table into Python variables
        print('\n')
        cur.execute("SELECT indicatorcode FROM {}".format(existingTables[1]))
        print(cur.fetchall())

        
        # @@ Terminate transactions in 1 of 2 ways:
        # (1) Commit any pending transaction to the database, OR
        conn.commit()
        # (2) Roll back to the start of any pending transaction
        # conn.rollback()

# Close the database connection
conn.close()
print("Successfully disconnected from the database, '{}'".format(dbname))

# %%
