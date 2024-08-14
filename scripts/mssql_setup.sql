USE master;
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'LabEquipment')
BEGIN
    CREATE DATABASE LabEquipment;
END;
GO

USE LabEquipment;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Equipment')
BEGIN
    CREATE TABLE Equipment (
        ID INT PRIMARY KEY IDENTITY(1,1),
        EquipmentName NVARCHAR(100),
        SerialNumber NVARCHAR(50),
        PurchaseDate DATE,
        LastCalibrationDate DATE,
        NextCalibrationDate DATE,
        Status NVARCHAR(20)
    );
END;
GO

-- Populate with synthetic data
INSERT INTO Equipment (EquipmentName, SerialNumber, PurchaseDate, LastCalibrationDate, NextCalibrationDate, Status)
VALUES 
    ('Microscope', 'MSC-001', '2020-01-15', '2023-01-15', '2024-01-15', 'Active'),
    ('Centrifuge', 'CTF-002', '2019-05-20', '2023-05-20', '2024-05-20', 'Active'),
    ('Spectrometer', 'SPC-003', '2021-03-10', '2023-03-10', '2024-03-10', 'Maintenance'),
    ('PCR Machine', 'PCR-004', '2018-11-30', '2023-11-30', '2024-11-30', 'Active'),
    ('pH Meter', 'PHM-005', '2022-07-05', '2023-07-05', '2024-07-05', 'Inactive');
GO