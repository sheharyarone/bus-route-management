CREATE SCHEMA db_proj;
USE db_proj;

CREATE TABLE Driver (
    DriverID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    LicenseNumber VARCHAR(20) NOT NULL
);

CREATE TABLE Bus (
    BusID INT PRIMARY KEY AUTO_INCREMENT,
    BusNumber VARCHAR(10) NOT NULL,
    Capacity INT,
    LastMaintenanceDate DATE,
    NextMaintenanceDueDate DATE,
    DriverID INT,
    CONSTRAINT FK_Bus_Driver FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE
);

CREATE TABLE Route (
    RouteID INT PRIMARY KEY AUTO_INCREMENT,
    RouteName VARCHAR(100) NOT NULL,
    StartLocation VARCHAR(100) NOT NULL,
    EndLocation VARCHAR(100) NOT NULL
);

CREATE TABLE BusRoute (
    BusID INT,
    RouteID INT,
    PRIMARY KEY (BusID, RouteID),
    CONSTRAINT FK_BusRoute_Bus FOREIGN KEY (BusID) REFERENCES Bus(BusID) ON DELETE CASCADE,
    CONSTRAINT FK_BusRoute_Route FOREIGN KEY (RouteID) REFERENCES Route(RouteID) ON DELETE CASCADE
);

-- Insert data into the Driver table
INSERT INTO Driver (FirstName, LastName, LicenseNumber) VALUES
    ('John', 'Doe', 'ABC123'),
    ('Jane', 'Smith', 'XYZ456'),
    ('Mike', 'Johnson', 'DEF789'),
    ('Sara', 'Brown', 'GHI012'),
    ('Chris', 'Williams', 'JKL345');

-- Insert data into the Bus table
INSERT INTO Bus (BusNumber, Capacity, LastMaintenanceDate, NextMaintenanceDueDate, DriverID) VALUES
    ('Bus001', 30, '2023-01-15', '2023-02-15', 1),
    ('Bus002', 40, '2023-02-10', '2023-03-10', 2),
    ('Bus003', 35, '2023-03-05', '2023-04-05', 3),
    ('Bus004', 25, '2023-04-20', '2023-05-20', 4),
    ('Bus005', 50, '2023-05-12', '2023-06-12', 5);

-- Insert data into the Route table
INSERT INTO Route (RouteName, StartLocation, EndLocation) VALUES
    ('Route1', 'City A', 'City B'),
    ('Route2', 'City C', 'City D'),
    ('Route3', 'City E', 'City F'),
    ('Route4', 'City G', 'City H'),
    ('Route5', 'City I', 'City J');

-- Insert data into the BusRoute table
INSERT INTO BusRoute (BusID, RouteID) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);