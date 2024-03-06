import misc
import os
import json
import sqlite3


def json2Database(jsonFileName, tableName, primaryKey, isDropTable):
    # Fix File Name Path First
    jsonFileName = os.path.join(os.getcwd(),jsonFileName)
    DB_FILENAME = os.path.join(os.getcwd(),misc.DB_FILENAME)

    # Open the JSON file
    with open(jsonFileName, 'r') as file:
        data = json.load(file)

    # Connect to the SQLite database (create a new one if it doesn't exist)
    conn = sqlite3.connect(DB_FILENAME)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Drop the table if it already exists
    if bool(isDropTable):
        cursor.execute(f"DROP TABLE IF EXISTS {tableName}")

    # Extract the keys from the first JSON object to determine the column names
    keys = list(data[0].keys())

    # Generate the CREATE TABLE statement dynamically
    create_table_keys = [s for s in keys if s != primaryKey]
    create_table_query = f'CREATE TABLE IF NOT EXISTS {tableName} ({primaryKey} INTEGER PRIMARY KEY UNIQUE, {", ".join(create_table_keys)})'
    
    # Create the table
    cursor.execute(create_table_query)
    
    # Insert the data into the table
    for item in data:
        # Generate the INSERT statement dynamically
        insert_query = f"INSERT INTO {tableName} ({', '.join(keys)}) VALUES ({', '.join(['?'] * len(keys))})"
        
        # Convert any lists to a string representation
        values = [str(item[key]) if isinstance(item[key], list) else item[key] for key in keys]
        
        # Execute the INSERT statement and handle the IntegrityError
        try:
            cursor.execute(insert_query, tuple(values))
        except sqlite3.IntegrityError:
            pass  # Ignore the error and continue to the next row
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return True

def database2JSON(tableName, jsonFileName):
    # Fix File Name Path First
    jsonFileName = os.path.join(os.getcwd(), jsonFileName)
    DB_FILENAME = os.path.join(os.getcwd(), misc.DB_FILENAME)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_FILENAME)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Fetch all rows from the table
    cursor.execute(f"SELECT * FROM {tableName}")
    rows = cursor.fetchall()
    
    # Get column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    
    # Prepare a list to hold the converted data
    data = []
    
    # Convert each row into a dictionary
    for row in rows:
        row_data = dict(zip(column_names, row))
        data.append(row_data)
    
    # Save the data as JSON to the specified file
    with open(jsonFileName, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    # Close the connection
    conn.close()

    return True

def getValues(tableName, columns, condition=None, groupBy=None):
    try:
        # Fix File Name Path First
        DB_FILENAME = os.path.join(os.getcwd(), misc.DB_FILENAME)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_FILENAME)
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
        
        # Create a comma-separated string of column names
        columns_str = ', '.join(columns)
        
        # Build the SELECT query with the column names and condition
        select_query = f"SELECT {columns_str} FROM {tableName}"
        if condition:
            select_query += f" WHERE {condition}"
        if groupBy:
            select_query += f" GROUP BY {groupBy}"
        
        # Execute the SELECT query
        cursor.execute(select_query)
        
        # Fetch all the rows returned by the SELECT query
        rows = cursor.fetchall()
        
        # Process the retrieved values
        result = []
        for row in rows:
            # Access the values using index or column names
            values = list(row)  # Convert the row to a list
            
            # Create a dictionary of column names and values
            row_dict = {col: val for col, val in zip(columns, values)}
            
            # Append the dictionary to the result list
            result.append(row_dict)
        
        # Close the connection
        conn.close()
        
        # Return the result list
        return result
    except sqlite3.Error as e:
        return None
    
    return True

def updateValue(tableName, column, newValue, condition=None):
    try:
        # Fix File Name Path First
        DB_FILENAME = os.path.join(os.getcwd(), misc.DB_FILENAME)
        
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_FILENAME)
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
        
        # Build the UPDATE query with the column, new value, and condition
        update_query = f"UPDATE {tableName} SET {column} = ?"
        update_params = (newValue,)
        if condition:
            update_query += f" WHERE {condition}"
        
        # Execute the UPDATE query
        cursor.execute(update_query, update_params)
        
        # Commit the changes to the database
        conn.commit()
        
        # Close the connection
        conn.close()
    except sqlite3.Error as e:
        return False
    
    return True

def isTableExists(tableName):
    conn = sqlite3.connect(misc.DB_FILENAME)
    cursor = conn.cursor()

    # Query to retrieve table names from the database schema
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    cursor.execute(query, (tableName,))
    
    result = cursor.fetchone()
    tableExists = result is not None

    cursor.close()
    conn.close()

    return tableExists