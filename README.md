
# User Manual

## Software Required:

- MySQL workbench
- MySQL server
- MongoDB Community Edition (Mongo DB)


## Packages Required:

- Python
- Tkinter - `pip install tk`
- mysql-connector - `pip install mysql-connector-python`
- pymongo - `pip install pymongo`

## Steps:

1. Run the Schema Code and Data.sql file first inside the workbench to create the required tables and populate data in them.
2. Then configure username and password corresponding to your database in the `db_credentials.py` file.
3. Open the MongoDB Compass and start the server. Now you must create a database with the name 'db_Proj' and create the following collections:
   - Bus
   - Driver
   - Route
   - BusRoute
4. Run the file `mongoDB_dataLoad.py` file included in the code part to populate the data inside the collections and define some constraints.
5. Run the `main.py` and the GUI will open and corresponding changes will be made in the database as you progress.
