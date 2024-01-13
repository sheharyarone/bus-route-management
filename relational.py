import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, Label, Entry, Button, messagebox
import mysql.connector
from db_credentials import db_config

def handleRelationalModel(root):

    new_window = tk.Toplevel(root)
    new_window.title("Relational Model")

    window_width = 200
    window_height = 300
    new_window.geometry(f"{window_width}x{window_height}")
    label = tk.Label(new_window, text="Relational Data",
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
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute a SELECT query to fetch all route data
        cursor.execute("SELECT * FROM Route")
        route_data = cursor.fetchall()

        # Close the database connection
        connection.close()

        return route_data

    def addRoute():
        # Create a new top-level window for adding a route
        add_window = tk.Toplevel(root)
        add_window.title("Add New Route")

        # Labels and Entry widgets for capturing route details
        labels = ["Route Name:", "Start Location:", "End Location:"]
        entries = [tk.Entry(add_window) for _ in range(len(labels))]

        # Function to handle the submission of the form
        def submitForm():
            values = [entry.get() for entry in entries]

            # Validate input
            if not all(values):
                messagebox.showerror("Error", "All fields must be filled")
                return

            try:
                # Establish a database connection
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',
                    database='db_proj'
                )

                # Create a cursor to execute SQL queries
                cursor = connection.cursor()

                # Execute the INSERT query to add a new route
                cursor.execute("INSERT INTO Route (RouteName, StartLocation, EndLocation) VALUES (%s, %s, %s)",
                               tuple(values))

                # Commit the changes to the database
                connection.commit()

                # Display a success message
                messagebox.showinfo("Success", "Route added successfully")

                # Close the cursor and the database connection
                cursor.close()
                connection.close()

                # Close the add window
                add_window.destroy()

            except Exception as e:
                # Display an error message if the insertion fails
                messagebox.showerror(
                    "Error", f"Failed to add route: {str(e)}")

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

        # Establish a database connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        try:
            # Execute the DELETE query to delete the selected route
            cursor.execute(
                "DELETE FROM Route WHERE RouteID = %s", (route_id,))

            # Commit the changes to the database
            connection.commit()

            # Display a success message
            messagebox.showinfo("Success", "Route deleted successfully")
        except Exception as e:
            # Display an error message if the deletion fails
            messagebox.showerror("Error", f"Failed to delete route: {str(e)}")
        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

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

        # Fetch buses data from the database based on the selected route
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            # Execute the SQL query to fetch buses data on the route
            query = "SELECT Bus.BusID, Bus.BusNumber, Bus.Capacity, Bus.LastMaintenanceDate, Bus.NextMaintenanceDueDate, Bus.DriverID " \
                    "FROM BusRoute " \
                    "JOIN Bus ON BusRoute.BusID = Bus.BusID " \
                    "WHERE BusRoute.RouteID = %s"
            cursor.execute(query, (route_id,))
            buses_data = cursor.fetchall()

            # Insert the fetched data into the treeview
            for row in buses_data:
                buses_tree.insert("", "end", values=row)

        except Exception as e:
            # Display an error message if the query fails
            messagebox.showerror(
                "Error", f"Failed to fetch buses on route: {str(e)}")

        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

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
        assign_window.title("Assign Buses to Route")

        # Labels and Entry widgets for capturing bus details
        labels = ["Bus ID:"]
        entries = [tk.Entry(assign_window) for _ in range(len(labels))]

        def bus_assign():
            bus_id = entries[0].get()

            if not bus_id:
                messagebox.showerror("Error", "Bus ID must be filled")
                return

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345',
                database='db_proj'
            )
            cursor = connection.cursor()

            try:
                # Execute the INSERT query to assign a bus to the route
                cursor.execute("""
                    INSERT INTO BusRoute(BusID, RouteID) VALUES (%s, %s)
                """, (bus_id, route_id))

                # Commit the changes to the database
                connection.commit()

                # Display a success message
                messagebox.showinfo(
                    "Success", "Bus assigned to route successfully")

            except Exception as e:
                # Display an error message if the assignment fails
                messagebox.showerror(
                    "Error", f"Failed to assign bus to route: {str(e)}")

            finally:
                # Close the cursor and the database connection
                cursor.close()
                connection.close()

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

    # Fetch route data from the database
    route_data = fetch_route_data()
    root = tk.Tk()
    # Create the main window
    root.title("Route Data")

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
        root.destroy(), handle_routes(root)))
    button5.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop
    root.mainloop()


def handle_bus(root):
    def fetch_bus_data():
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute a SELECT query to fetch all bus data
        cursor.execute("SELECT * FROM Bus")
        bus_data = cursor.fetchall()

        # Close the database connection
        connection.close()

        return bus_data

    def addBus():
        # Create a new top-level window for adding a bus
        add_window = tk.Toplevel(root)
        add_window.title("Add New Bus")

        # Labels and Entry widgets for capturing bus details
        labels = ["Bus Number:", "Capacity:", "Last Maintenance Date:",
                  "Next Maintenance Due Date:", "Driver ID:"]
        entries = [tk.Entry(add_window) for _ in range(len(labels))]

        # Function to handle the submission of the form
        def submitForm():
            values = [entry.get() for entry in entries]

            # Validate input
            if not all(values):
                messagebox.showerror("Error", "All fields must be filled")
                return

            try:
                # Establish a database connection
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',
                    database='db_proj'
                )

                # Create a cursor to execute SQL queries
                cursor = connection.cursor()

                # Execute the INSERT query to add a new bus
                cursor.execute("INSERT INTO Bus (BusNumber, Capacity, LastMaintenanceDate, NextMaintenanceDueDate, DriverID) VALUES (%s, %s, %s, %s, %s)",
                               tuple(values))

                # Commit the changes to the database
                connection.commit()

                # Display a success message
                messagebox.showinfo("Success", "Bus added successfully")

                # Close the cursor and the database connection
                cursor.close()
                connection.close()

                # Close the add window
                add_window.destroy()

            except Exception as e:
                # Display an error message if the insertion fails
                messagebox.showerror(
                    "Error", f"Failed to add bus: {str(e)}")

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

        # Establish a database connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        try:
            # Execute the DELETE query to delete the selected bus
            cursor.execute(
                "DELETE FROM Bus WHERE BusID = %s", (bus_id,))

            # Commit the changes to the database
            connection.commit()

            # Display a success message
            messagebox.showinfo("Success", "Bus deleted successfully")
        except Exception as e:
            # Display an error message if the deletion fails
            messagebox.showerror("Error", f"Failed to delete bus: {str(e)}")
        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

    def assignRoute():

        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Bus is selected")
            return

        bus_id = tree.item(selected_item)['values'][0]

        assign_window = tk.Toplevel(root)
        assign_window.title("Assign Route")

        labels = ["Route Number:"]
        entries = [tk.Entry(assign_window) for _ in range(len(labels))]

        def bus_route_add():
            route_num = entries[0].get()

            if not route_num:
                messagebox.showerror("Error", "Route Number must be filled")
                return

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345',
                database='db_proj'
            )
            cursor = connection.cursor()

            try:
                # Execute the INSERT query to assign a route to the bus
                cursor.execute("""
                    INSERT INTO BusRoute(BusID, RouteID) VALUES (%s, %s)
                """, (bus_id, route_num))

                # Commit the changes to the database
                connection.commit()

                # Display a success message
                messagebox.showinfo("Success", "Route assigned successfully")

            except Exception as e:
                # Display an error message if the assignment fails
                messagebox.showerror(
                    "Error", f"Failed to assign route: {str(e)}")

            finally:
                # Close the cursor and the database connection
                cursor.close()
                connection.close()

        submit_button = tk.Button(assign_window, text="OK", command=lambda: (
            bus_route_add(), assign_window.destroy()))
        submit_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(assign_window, text="Cancel",
                                  command=lambda: assign_window.destroy())
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

        # Fetch bus routes data from the database based on the selected bus
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            # Execute the SQL query to fetch bus routes data
            query = "SELECT Route.RouteID, Route.RouteName, Route.StartLocation, Route.EndLocation " \
                    "FROM BusRoute " \
                    "JOIN Route ON BusRoute.RouteID = Route.RouteID " \
                    "WHERE BusRoute.BusID = %s"
            cursor.execute(query, (bus_id,))
            bus_routes_data = cursor.fetchall()

            # Insert the fetched data into the treeview
            for row in bus_routes_data:
                routes_tree.insert("", "end", values=row)

        except Exception as e:
            # Display an error message if the query fails
            messagebox.showerror(
                "Error", f"Failed to fetch bus routes: {str(e)}")

        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

        # Pack the treeview
        routes_tree.pack(pady=10)

        # Close the window button
        close_button = tk.Button(
            routes_window, text="Close", command=lambda: routes_window.destroy())
        close_button.pack(pady=10)

    # Fetch bus data from the database
    bus_data = fetch_bus_data()
    root = tk.Tk()
    # Create the main window
    root.title("Bus Data")

    # Set the width and height of the window
    window_width = 1300
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Create a treeview widget to display the data
    tree = ttk.Treeview(root, columns=(
        "BusID", "BusNumber", "Capacity", "LastMaintenanceDate", 'NextMaintenanceDueDate', 'DriverID'), show="headings")
    tree.heading("BusID", text="BusID")
    tree.heading("BusNumber", text="BusNumber")
    tree.heading("Capacity", text="Capacity")
    tree.heading("LastMaintenanceDate", text="LastMaintenanceDate")
    tree.heading("NextMaintenanceDueDate", text="NextMaintenanceDueDate")
    tree.heading("DriverID", text="DriverID")

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

    button3 = tk.Button(root, text="Show Route", command=getBusRoutes)
    button3.pack(side=tk.LEFT, padx=10)

    button4 = tk.Button(root, text="Assign Route", command=assignRoute)
    button4.pack(side=tk.LEFT, padx=10)

    button5 = tk.Button(root, text="Refresh",
                        command=lambda: (root.destroy(), handle_bus(root)))
    button5.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter event loop
    root.mainloop()


# Function to display driver data in the Tkinter window
def handle_driver(root):

    def fetch_driver_data():
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute a SELECT query to fetch all driver data
        cursor.execute("SELECT * FROM Driver")
        driver_data = cursor.fetchall()

        # Close the database connection
        connection.close()

        return driver_data

    def deleteDriver(tree):
        selected_item = tree.focus()

        if not selected_item:
            messagebox.showerror("Error", "No Driver is selected")
            return

        # Extract the driver ID or unique identifier from the selected item
        driver_id = tree.item(selected_item)['values'][0]

        # Establish a database connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        try:
            # Execute the DELETE query to delete the selected driver
            cursor.execute(
                "DELETE FROM Driver WHERE DriverID = %s", (driver_id,))

            # Commit the changes to the database
            connection.commit()

            # Display a success message
            messagebox.showinfo("Success", "Driver deleted successfully")
        except Exception as e:
            # Display an error message if the deletion fails
            messagebox.showerror("Error", f"Failed to delete driver: {str(e)}")
        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

    def addDriver(root):
        # Create a new top-level window for adding a driver
        add_window = tk.Toplevel(root)
        add_window.title("Add New Driver")

        # Labels and Entry widgets for capturing driver details
        label_fname = Label(add_window, text="First Name:")
        entry_fname = Entry(add_window)

        label_lname = Label(add_window, text="Last Name:")
        entry_lname = Entry(add_window)

        label_license = Label(add_window, text="License Number:")
        entry_license = Entry(add_window)

        # Function to handle the submission of the form

        def submitForm():
            fname = entry_fname.get()
            lname = entry_lname.get()
            license_number = entry_license.get()

            # Validate input
            if not fname or not lname or not license_number:
                messagebox.showerror("Error", "All fields must be filled")
                return

            try:
                # Establish a database connection
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',
                    database='db_proj'
                )

                # Create a cursor to execute SQL queries
                cursor = connection.cursor()

                # Execute the INSERT query to add a new driver
                cursor.execute("INSERT INTO Driver (FirstName,LastName, LicenseNumber) VALUES (%s, %s, %s)",
                               (fname, lname, license_number))

                # Commit the changes to the database
                connection.commit()

                # Display a success message
                messagebox.showinfo("Success", "Driver added successfully")

                # Close the cursor and the database connection
                cursor.close()
                connection.close()

                # Close the add window
                add_window.destroy()

            except Exception as e:
                # Display an error message if the insertion fails
                messagebox.showerror(
                    "Error", f"Failed to add driver: {str(e)}")

        # Button to submit the form
        submit_button = Button(add_window, text="Submit", command=submitForm)

        # Layout the widgets
        label_fname.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_fname.grid(row=0, column=1, padx=10, pady=5)

        label_lname.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_lname.grid(row=1, column=1, padx=10, pady=5)

        label_license.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_license.grid(row=2, column=1, padx=10, pady=5)

        submit_button.grid(row=3, column=1, pady=10)
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Driver Data")

    # Set the width and height of the window
    window_width = 900
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Fetch driver data from the database
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
