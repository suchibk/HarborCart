-- Optional SQL Server schema for a future persistence adapter.
-- The running sample stores email/ID pairs in memory; it does not execute this file.
CREATE TABLE dbo.Customers
(
    CustomerId UNIQUEIDENTIFIER NOT NULL CONSTRAINT PK_Customers PRIMARY KEY,
    FirstName NVARCHAR(80) NOT NULL,
    LastName NVARCHAR(80) NOT NULL,
    Age INT NOT NULL,
    Email NVARCHAR(254) COLLATE Latin1_General_100_CI_AS NOT NULL,
    CONSTRAINT CK_Customers_Age CHECK (Age >= 21 AND Age <= 120),
    CONSTRAINT UQ_Customers_Email UNIQUE (Email)
);
