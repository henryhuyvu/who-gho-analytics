# %% Import Python packages
import requests
import psycopg

# %% Set up and interface with my local PostgreSQL server

# Connect to an existing database
with psycopg.connect(dbname="worlddata", user="postgres", password=input("Enter your password:")) as conn:
    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute(
            """
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text
            )
            """
        )

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100,"abc'def")
        )

        # Query the database and obtain data as Python objects.
        cur.execute(
            "SELECT * FROM test"
        )
        cur.fetchone() # will return (1, 100, "abc'def")
        # cur.fetchmany()
        # cur.fetchall() # These two other commands will return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        conn.commit()


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
    print(count, value)
    count += 1

print("\nThe number of available indicators is:",len(indicator_json['value']))

print("\nA single indicators raw data is shown below")
# print(indicator_json['@odata.context'])
# print(type(indicator_json['value']))
print(indicator_json['value'][0])
print("The data type here is:",type(indicator_json['value'][0]))

print('\nThis raw data can be pulled out into key and value elements as:')
for keys in indicator_json['value'][0]:
    print(keys,": ", indicator_json['value'][0][keys])

# %%
