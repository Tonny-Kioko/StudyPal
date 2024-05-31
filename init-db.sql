-- Create the user
CREATE USER postgres WITH PASSWORD 'c3po';

-- Create the database
CREATE DATABASE studypaldb;

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE studypaldb TO postgres;
