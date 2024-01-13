import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, Label, Entry, Button, messagebox
from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["db_Proj"]  # Use your MongoDB database name


def handleNonRelationalModel(root):

    new_window = tk.Toplevel(root)
    new_window.title("Non Relational Model")

    window_width = 200
    window_height = 300
    new_window.geometry(f"{window_width}x{window_height}")

    # Create a Label at the top of the window
    label = tk.Label(new_window, text="Non-Relational Data",
                     font=("Helvetica", 16))
    label.pack(pady=10)

    # Create Button 1 with lambda function and place it at (50, 50)
    button1 = tk.Button(new_window, text="Drivers",
                        command=lambda: handle_driver(root))
    button1.place(x=50, y=50)

    # Create Button 2 with lambda function and place it at (50, 120)
    button2 = tk.Button(new_window, text="Bus",
                        command=lambda: handle_bus(root))
    button2.place(x=50, y=120)

    # Create Button 3 with lambda function and place it at (50, 190)
    button3 = tk.Button(new_window, text="Routes",
                        command=lambda: handle_routes(root))
    button3.place(x=50, y=190)


def handle_routes(root):
    def fetch_route_data():
        # Fetch all route data from MongoDB
        routes = db.Route.find()
        route_data = [(route['RouteID'], route['RouteName'],
                       route['StartLocation'], route['EndLocation']) for route in routes]
        return route_data

    def addRoute():
        # Create a new top-level window for adding a route
        add_window = tk.Toplevel(root)
        add_window.title("Add New Route")

        # Labels and Entry widgets for capturing route details
        labels = ["RouteID", "Route Name:", "Start Location:", "End Location:"]
        entries = [tk.Entry(add_window) for _ in range(len(labels))]

        # Function to handle the submission of the form
        def submitForm():
            values = [entry.get() for entry in entries]

            # Validate input
            if not all(values):
                messagebox.showerror("Error", "All fields must be filled")
                return

            route_id_exists = db.Route.find_one({"RouteID": int(values[0])})

            if route_id_exists:
                messagebox.showerror("Error", "RouteID already exists")
                return
            # Insert a new route into MongoDB
            db.Route.insert_one({
                "RouteID": int(values[0]),
                "RouteName": values[1],
                "StartLocation": values[2],
                "EndLocation": values[3]
            })

            # Display a success message
            messagebox.showinfo("Success", "Route added successfully")

            # Close the add window
            add_window.destroy()

        # Button to submit the form
        submit_button = tk.Button(
            add_window, text="Submit", command=submitForm)

        # Layout the widgets
        for i, label_text in enumerate(labels):
            label = tk.Label(add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entries[i].grid(row=i, column=1, padx=10, pady=5)

        submit_button.grid(row=len(labels), column=1, pady=10)

    def deleteRoute():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Route is selected")
            return

        # Extract the route ID or unique identifier from the selected item
        route_id = tree.item(selected_item)['values'][0]

        # Delete the selected route from MongoDB
        db.Route.delete_one({"RouteID": int(route_id)})
        db.BusRoute.delete_many({"RouteID": int(route_id)})

        # Display a success message
        messagebox.showinfo("Success", "Route deleted successfully")

    def showBuses():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Route is selected")
            return

        route_id = tree.item(selected_item)['values'][0]

        buses_window = tk.Toplevel(root)
        buses_window.title("Buses on Route")

        # Create a treeview widget to display the buses on the route
        buses_tree = ttk.Treeview(buses_window, columns=(
            "BusID", "BusNumber", "Capacity", "LastMaintenanceDate", "NextMaintenanceDueDate", "DriverID"), show="headings")
        buses_tree.heading("BusID", text="BusID")
        buses_tree.heading("BusNumber", text="BusNumber")
        buses_tree.heading("Capacity", text="Capacity")
        buses_tree.heading("LastMaintenanceDate", text="LastMaintenanceDate")
        buses_tree.heading(
            "NextMaintenanceDueDate", text="NextMaintenanceDueDate")
        buses_tree.heading("DriverID", text="DriverID")

        # Fetch buses data from MongoDB based on the selected route
        bus_routes = db.BusRoute.find({"RouteID": int(route_id)})
        bus_ids = [bus_route['BusID'] for bus_route in bus_routes]

        # Fetch bus details from MongoDB based on bus IDs
        buses = db.Bus.find({"BusID": {"$in": bus_ids}})
        buses_data = [(bus['BusID'], bus['BusNumber'], bus['Capacity'], bus['LastMaintenanceDate'],
                       bus['NextMaintenanceDueDate'], bus['DriverID']) for bus in buses]

        # Insert the fetched data into the treeview
        for row in buses_data:
            buses_tree.insert("", "end", values=row)

        # Pack the treeview
        buses_tree.pack(pady=10)

        # Close the window button
        close_button = tk.Button(
            buses_window, text="Close", command=lambda: buses_window.destroy())
        close_button.pack(pady=10)

    def assignBuses():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Route is selected")
            return

        route_id = tree.item(selected_item)['values'][0]

        assign_window = tk.Toplevel(root)
        assign_window.title("Assign Bus to Route")

        # Labels and Entry widgets for capturing bus details
        labels = ["Bus ID:"]
        entries = [tk.Entry(assign_window) for _ in range(len(labels))]

        def bus_assign():
            bus_id = int(entries[0].get())

            if not bus_id:
                messagebox.showerror("Error", "Bus ID must be filled")
                return

            bus_id_exists = db.Bus.find_one({"BusID": int(bus_id)})

            if not bus_id_exists:
                messagebox.showerror("Error", "BusID does not exist")
                return

            bus_route_exists = db.BusRoute.find_one(
                {"BusID": int(bus_id), "RouteID": int(route_id)})
            if bus_route_exists:
                messagebox.showerror(
                    "Error", "This bus is already assigned on this route!")
                return

            # Insert a new BusRoute into MongoDB
            db.BusRoute.insert_one({
                "BusID": int(bus_id),
                "RouteID": int(route_id)
            })

            # Display a success message
            messagebox.showinfo(
                "Success", "Bus assigned to route successfully")

            # Close the assign window
            assign_window.destroy()

        submit_button = tk.Button(assign_window, text="OK", command=lambda: (
            bus_assign(), assign_window.destroy()))
        submit_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(assign_window, text="Cancel",
                                  command=lambda: assign_window.destroy())
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Layout the widgets
        for i, label_text in enumerate(labels):
            label = tk.Label(assign_window, text=label_text)
            label.pack(padx=10, pady=5, anchor="e")
            entries[i].pack(padx=10, pady=5)

    # Fetch route data from MongoDB
    route_data = fetch_route_data()

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Routes Data")

    # Set the width and height of the window
    window_width = 900
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Create a treeview widget to display the data
    tree = ttk.Treeview(root, columns=(
        "RouteID", "RouteName", "StartLocation", "EndLocation"), show="headings")
    tree.heading("RouteID", text="RouteID")
    tree.heading("RouteName", text="RouteName")
    tree.heading("StartLocation", text="StartLocation")
    tree.heading("EndLocation", text="EndLocation")

    # Insert the fetched data into the treeview
    for row in route_data:
        tree.insert("", "end", values=row)

    # Pack the treeview
    tree.pack(pady=10)

    # Create buttons in horizontal order
    button1 = tk.Button(root, text="Add Route", command=addRoute)
    button1.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(root, text="Delete Route", command=deleteRoute)
    button2.pack(side=tk.LEFT, padx=10)

    button3 = tk.Button(root, text="Show Buses", command=showBuses)
    button3.pack(side=tk.LEFT, padx=10)

    button4 = tk.Button(root, text="Assign Buses", command=assignBuses)
    button4.pack(side=tk.LEFT, padx=10)

    button5 = tk.Button(root, text="Refresh", command=lambda: (
        root.destroy(), handle_routes(None)))
    button5.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop
    root.mainloop()


# Function to display bus data in the Tkinter window
def handle_bus(root):

    def fetch_bus_data():
        # Fetch all bus data from MongoDB
        buses = db.Bus.find()
        bus_data = [(bus['BusID'], bus['BusNumber'], bus['Capacity'], bus['LastMaintenanceDate'],
                     bus['NextMaintenanceDueDate'], bus['DriverID']) for bus in buses]
        return bus_data

    def addBus():
        # Create a new top-level window for adding a bus
        add_window = tk.Toplevel(root)
        add_window.title("Add New Bus")

        # Labels and Entry widgets for capturing bus details
        labels = ["Bus ID:", "Bus Number:", "Capacity:",
                  "Last Maintenance Date:", "Next Maintenance Due Date:", "Driver ID:"]
        entries = [tk.Entry(add_window) for _ in range(len(labels))]

        # Function to handle the submission of the form
        def submitForm():
            values = [entry.get() for entry in entries]

            # Validate input
            if not all(values):
                messagebox.showerror("Error", "All fields must be filled")
                return

            # Check if the specified DriverID exists in the Driver collection
            driver_id_exists = db.Driver.find_one({"DriverID": int(values[5])})

            if not driver_id_exists:
                messagebox.showerror("Error", "DriverID does not exist")
                return

            bus_id_exists = db.Bus.find_one({"BusID": int(values[0])})

            if bus_id_exists:
                messagebox.showerror("Error", "BusID already exists")
                return
            # Insert a new bus into MongoDB
            db.Bus.insert_one({
                "BusID": int(values[0]),  # Assuming BusID is the first field
                "BusNumber": values[1],
                "Capacity": values[2],
                "LastMaintenanceDate": values[3],
                "NextMaintenanceDueDate": values[4],
                "DriverID": int(values[5])
            })

            # Display a success message
            messagebox.showinfo("Success", "Bus added successfully")

            # Close the add window
            add_window.destroy()

        # Button to submit the form
        submit_button = tk.Button(
            add_window, text="Submit", command=submitForm)

        # Layout the widgets
        for i, label_text in enumerate(labels):
            label = tk.Label(add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entries[i].grid(row=i, column=1, padx=10, pady=5)

        submit_button.grid(row=len(labels), column=1, pady=10)

    def deleteBus():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Bus is selected")
            return

        # Extract the bus ID or unique identifier from the selected item
        bus_id = tree.item(selected_item)['values'][0]

        # Delete the selected bus from MongoDB
        db.Bus.delete_one({"BusID": int(bus_id)})
        db.BusRoute.delete_many({"BusID": int(bus_id)})

        # Display a success message
        messagebox.showinfo("Success", "Bus deleted successfully")

    def assignRoute():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Bus is selected")
            return

        bus_id = tree.item(selected_item)['values'][0]

        assign_window = tk.Toplevel(root)
        assign_window.title("Assign Route to Bus")

        labels = ["Route Number:"]
        entries = [tk.Entry(assign_window) for _ in range(len(labels))]

        def bus_route_add():
            route_num = entries[0].get()

            if not route_num:
                messagebox.showerror("Error", "Route Number must be filled")
                return

            route_id_exists = db.Route.find_one({"DriverID": int(route_num)})

            if not route_id_exists:
                messagebox.showerror("Error", "RouteID does not exists!")
                return

            bus_route_exists = db.BusRoute.find_one(
                {"BusID": int(bus_id), "RouteID": int(route_num)})
            if bus_route_exists:
                messagebox.showerror(
                    "Error", "This bus is already assigned on this route!")
                return
            # Insert a new BusRoute into MongoDB
            db.BusRoute.insert_one({
                "BusID": int(bus_id),
                "RouteID": int(route_num)
            })

            # Display a success message
            messagebox.showinfo("Success", "Route assigned successfully")

            # Close the assign window
            assign_window.destroy()

        submit_button = tk.Button(assign_window, text="OK", command=lambda: (
            bus_route_add(), assign_window.destroy()))
        submit_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(
            assign_window, text="Cancel", command=lambda: assign_window.destroy())
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Layout the widgets
        for i, label_text in enumerate(labels):
            label = tk.Label(assign_window, text=label_text)
            label.pack(padx=10, pady=5, anchor="e")
            entries[i].pack(padx=10, pady=5)

    def getBusRoutes():
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Bus is selected")
            return

        bus_id = tree.item(selected_item)['values'][0]

        routes_window = tk.Toplevel(root)
        routes_window.title("Bus Routes")

        # Create a treeview widget to display the routes
        routes_tree = ttk.Treeview(routes_window, columns=(
            "RouteID", "RouteName", "StartLocation", "EndLocation"), show="headings")
        routes_tree.heading("RouteID", text="RouteID")
        routes_tree.heading("RouteName", text="RouteName")
        routes_tree.heading("StartLocation", text="StartLocation")
        routes_tree.heading("EndLocation", text="EndLocation")

        # Fetch BusRoute data from MongoDB based on the selected bus
        bus_routes = db.BusRoute.find({"BusID": bus_id})

        # Fetch detailed route information based on RouteID
        for bus_route in bus_routes:
            route_id = bus_route["RouteID"]
            route = db.Route.find_one({"RouteID": route_id})

            # If the route is found, insert it into the treeview
            if route:
                route_data = (route['RouteID'], route['RouteName'],
                              route['StartLocation'], route['EndLocation'])
                routes_tree.insert("", "end", values=route_data)

        # Pack the treeview
        routes_tree.pack(pady=10)

        close_button = tk.Button(
            routes_window, text="Close", command=lambda: routes_window.destroy())
        close_button.pack(pady=10)

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Bus Data")

    # Set the width and height of the window
    window_width = 1300
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Fetch bus data from MongoDB
    bus_data = fetch_bus_data()

    # Create a treeview widget to display the data
    tree = ttk.Treeview(root, columns=(
        "BusID", "BusNumber", "Capacity", "LastMaintenanceDate", "NextMaintenanceDueDate", "DriverID"), show="headings")
    tree.heading("BusID", text="BusID")
    tree.heading("BusNumber", text="Bus Number")
    tree.heading("Capacity", text="Capacity")
    tree.heading("LastMaintenanceDate", text="Last Maintenance Date")
    tree.heading("NextMaintenanceDueDate", text="Next Maintenance Due Date")
    tree.heading("DriverID", text="Driver ID")

    # Insert the fetched data into the treeview
    for row in bus_data:
        tree.insert("", "end", values=row)

    # Pack the treeview
    tree.pack(pady=10)

    # Create buttons in horizontal order
    button1 = tk.Button(root, text="Add Bus", command=addBus)
    button1.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(root, text="Delete Bus", command=deleteBus)
    button2.pack(side=tk.LEFT, padx=10)

    button3 = tk.Button(root, text="Assign Route", command=assignRoute)
    button3.pack(side=tk.LEFT, padx=10)

    button4 = tk.Button(root, text="Get Bus Routes", command=getBusRoutes)
    button4.pack(side=tk.LEFT, padx=10)

    button5 = tk.Button(root, text="Refresh", command=lambda: (
        root.destroy(), handle_bus(None)))
    button5.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop
    root.mainloop()


# Function to display driver data in the Tkinter window
def handle_driver(root):

    def fetch_driver_data():
        # Fetch all driver data from MongoDB
        drivers = db.Driver.find()
        driver_data = [(driver['DriverID'], driver['FirstName'],
                        driver['LastName'], driver['LicenseNumber']) for driver in drivers]
        return driver_data

    def deleteDriver(tree):
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Driver is selected")
            return

        # Extract the driver ID or unique identifier from the selected item
        driver_id = tree.item(selected_item)['values'][0]

        # Delete the selected driver from MongoDB
        db.Driver.delete_one({"DriverID": int(driver_id)})

        buses = db.Bus.find({"DriverID": driver_id})
        bus_ids = [bus['BusID'] for bus in buses]

        # Delete all associated BusRoute objects
        db.BusRoute.delete_many({"BusID": {"$in": bus_ids}})

        # Delete all buses associated with the driver
        db.Bus.delete_many({"DriverID": driver_id})
        # Display a success message
        messagebox.showinfo("Success", "Driver deleted successfully")

    def addDriver(root):
        # Create a new top-level window for adding a driver
        add_window = tk.Toplevel(root)
        add_window.title("Add New Driver")

        # Labels and Entry widgets for capturing driver details
        label_driverid = Label(add_window, text='Driver ID :')
        entry_driverid = Entry(add_window)

        label_fname = Label(add_window, text="First Name:")
        entry_fname = Entry(add_window)

        label_lname = Label(add_window, text="Last Name:")
        entry_lname = Entry(add_window)

        label_license = Label(add_window, text="License Number:")
        entry_license = Entry(add_window)

        # Function to handle the submission of the form
        def submitForm():
            driver_id = entry_driverid.get()
            fname = entry_fname.get()
            lname = entry_lname.get()
            license_number = entry_license.get()

            # Validate input
            if not driver_id or not fname or not lname or not license_number:
                messagebox.showerror("Error", "All fields must be filled")
                return
            driver_id_exists = db.Driver.find_one({"DriverID": int(driver_id)})

            if driver_id_exists:
                messagebox.showerror("Error", "DriverID already exists")
                return

            # Insert a new driver into MongoDB
            db.Driver.insert_one({
                "DriverID": int(driver_id),
                "FirstName": fname,
                "LastName": lname,
                "LicenseNumber": license_number
            })

            # Display a success message
            messagebox.showinfo("Success", "Driver added successfully")

            # Close the add window
            add_window.destroy()

        # Button to submit the form
        submit_button = Button(add_window, text="Submit", command=submitForm)

        label_driverid.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_driverid.grid(row=0, column=1, padx=10, pady=5)

        # Layout the widgets
        label_fname.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_fname.grid(row=1, column=1, padx=10, pady=5)

        label_lname.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_lname.grid(row=2, column=1, padx=10, pady=5)

        label_license.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_license.grid(row=3, column=1, padx=10, pady=5)

        submit_button.grid(row=4, column=1, pady=10)

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Driver Data")

    # Set the width and height of the window
    window_width = 900
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Fetch driver data from MongoDB
    driver_data = fetch_driver_data()

    # Create a treeview widget to display the data
    tree = ttk.Treeview(root, columns=(
        "DriverID", "FirstName", "LastName", "LicenseNumber"), show="headings")
    tree.heading("DriverID", text="DriverID")
    tree.heading("FirstName", text="First Name")
    tree.heading("LastName", text="Last Name")
    tree.heading("LicenseNumber", text="License Number")

    # Insert the fetched data into the treeview
    for row in driver_data:
        tree.insert("", "end", values=row)

    # Pack the treeview
    tree.pack(pady=10)

    # Create buttons in horizontal order
    button1 = tk.Button(root, text="Add Driver",
                        command=lambda: addDriver(root))
    button1.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(root, text="Delete Driver",
                        command=lambda: deleteDriver(tree))
    button2.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(root, text="Refresh",
                        command=lambda: (root.destroy(), handle_driver(root)))
    button2.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop
    root.mainloop()
