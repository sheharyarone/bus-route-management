from pymongo import MongoClient


def create_database():
    # Establish a connection to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["db_Proj"]

    # Create collections
    driver_collection = db["Driver"]
    bus_collection = db["Bus"]
    route_collection = db["Route"]
    bus_route_collection = db["BusRoute"]

    # Create unique indexes
    driver_collection.create_index([("DriverID", 1)], unique=True)
    bus_collection.create_index([("BusID", 1)], unique=True)
    route_collection.create_index([("RouteID", 1)], unique=True)
    bus_route_collection.create_index(
        [("BusID", 1), ("RouteID", 1)], unique=True)

    # Insert example data into Driver collection
    driver_data = [
        {"DriverID": 1, "FirstName": "John",
            "LastName": "Doe", "LicenseNumber": "ABC123"},
        {"DriverID": 2, "FirstName": "Jane",
            "LastName": "Smith", "LicenseNumber": "XYZ456"},
        {"DriverID": 3, "FirstName": "Mike",
            "LastName": "Johnson", "LicenseNumber": "DEF789"},
        {"DriverID": 4, "FirstName": "Sara",
            "LastName": "Brown", "LicenseNumber": "GHI012"},
        {"DriverID": 5, "FirstName": "Chris",
            "LastName": "Williams", "LicenseNumber": "JKL345"}
    ]

    driver_collection.insert_many(driver_data)

    # Insert example data into Bus collection
    bus_data = [
        {"BusID": 1, "BusNumber": "Bus001", "Capacity": 30, "LastMaintenanceDate": "2023-01-15",
            "NextMaintenanceDueDate": "2023-02-15", "DriverID": 1},
        {"BusID": 2, "BusNumber": "Bus002", "Capacity": 40, "LastMaintenanceDate": "2023-02-10",
            "NextMaintenanceDueDate": "2023-03-10", "DriverID": 2},
        {"BusID": 3, "BusNumber": "Bus003", "Capacity": 35, "LastMaintenanceDate": "2023-03-05",
            "NextMaintenanceDueDate": "2023-04-05", "DriverID": 3},
        {"BusID": 4, "BusNumber": "Bus004", "Capacity": 25, "LastMaintenanceDate": "2023-04-20",
            "NextMaintenanceDueDate": "2023-05-20", "DriverID": 4},
        {"BusID": 5, "BusNumber": "Bus005", "Capacity": 50, "LastMaintenanceDate": "2023-05-12",
            "NextMaintenanceDueDate": "2023-06-12", "DriverID": 5}
    ]

    bus_collection.insert_many(bus_data)

    # Insert example data into Route collection
    route_data = [
        {"RouteID": 1, "RouteName": "Route1",
            "StartLocation": "City A", "EndLocation": "City B"},
        {"RouteID": 2, "RouteName": "Route2",
            "StartLocation": "City C", "EndLocation": "City D"},
        {"RouteID": 3, "RouteName": "Route3",
            "StartLocation": "City E", "EndLocation": "City F"},
        {"RouteID": 4, "RouteName": "Route4",
            "StartLocation": "City G", "EndLocation": "City H"},
        {"RouteID": 5, "RouteName": "Route5",
            "StartLocation": "City I", "EndLocation": "City J"}
    ]

    route_collection.insert_many(route_data)

    # Insert example data into BusRoute collection
    bus_route_data = [
        {"BusID": 1, "RouteID": 1},
        {"BusID": 2, "RouteID": 2},
        {"BusID": 3, "RouteID": 3},
        {"BusID": 4, "RouteID": 4},
        {"BusID": 5, "RouteID": 5}
    ]
    bus_route_collection.insert_many(bus_route_data)

    # Close the MongoDB connection
    client.close()


if __name__ == "__main__":
    create_database()
