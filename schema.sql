-- Sample schema for GenAI SQL demo: a simple company database
-- with departments and employees.

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INTEGER REFERENCES departments(department_id),
    salary NUMERIC(10, 2),
    hire_date DATE
);

INSERT INTO departments (department_name, location) VALUES
('Engineering', 'Bengaluru'),
('Sales', 'Mumbai'),
('Human Resources', 'Delhi'),
('Marketing', 'Hyderabad');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date) VALUES
('Ananya', 'Sharma', 'ananya.sharma@example.com', 1, 85000, '2022-03-15'),
('Rohit', 'Verma', 'rohit.verma@example.com', 1, 92000, '2021-07-01'),
('Priya', 'Nair', 'priya.nair@example.com', 2, 65000, '2023-01-10'),
('Karthik', 'Reddy', 'karthik.reddy@example.com', 2, 60000, '2023-05-22'),
('Sneha', 'Iyer', 'sneha.iyer@example.com', 3, 55000, '2020-11-30'),
('Arjun', 'Mehta', 'arjun.mehta@example.com', 4, 70000, '2022-09-18');
