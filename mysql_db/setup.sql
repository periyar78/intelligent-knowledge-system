-- ============================================
-- University Knowledge System - MySQL Setup
-- ============================================

CREATE DATABASE IF NOT EXISTS university;
USE university;

DROP TABLE IF EXISTS Enrollment;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Faculty;
DROP TABLE IF EXISTS Department;

-- ---------- Department ----------
CREATE TABLE Department (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL
);

INSERT INTO Department (dept_name) VALUES
('CSE'), ('IT'), ('ECE'), ('MECH');

-- ---------- Faculty ----------
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    specialization VARCHAR(100)
);

INSERT INTO Faculty (name, specialization) VALUES
('Dr. Kumar', 'Artificial Intelligence'),
('Dr. Ravi', 'Artificial Intelligence'),
('Dr. Meena', 'Databases'),
('Dr. Suresh', 'Networks'),
('Dr. Lakshmi', 'Machine Learning');

-- ---------- Course ----------
CREATE TABLE Course (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100),
    faculty_id INT,
    dept_id INT,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

INSERT INTO Course (course_name, faculty_id, dept_id) VALUES
('Machine Learning', 1, 1),
('Artificial Intelligence', 2, 1),
('DBMS', 3, 1),
('Computer Networks', 4, 2),
('Deep Learning', 5, 1),
('Data Structures', 3, 1),
('Operating Systems', 4, 2);

-- ---------- Student (15 students) ----------
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    gpa DECIMAL(3,2),
    year_joined INT
);

INSERT INTO Student (student_id, name, department, gpa, year_joined) VALUES
(101, 'Arun',    'CSE',   8.5, 2023),
(102, 'Priya',   'IT',    9.1, 2023),
(103, 'Rahul',   'CSE',   7.8, 2022),
(104, 'Sneha',   'CSE',   8.9, 2023),
(105, 'Vikram',  'ECE',   6.9, 2022),
(106, 'Divya',   'IT',    8.2, 2024),
(107, 'Karthik', 'CSE',   9.3, 2023),
(108, 'Anjali',  'MECH',  7.4, 2022),
(109, 'Manoj',   'CSE',   8.7, 2024),
(110, 'Deepa',   'ECE',   7.9, 2023),
(111, 'Suresh',  'IT',    8.0, 2022),
(112, 'Kavya',   'CSE',   9.5, 2024),
(113, 'Ramesh',  'MECH',  6.5, 2023),
(114, 'Nithya',  'CSE',   8.1, 2022),
(115, 'Ganesh',  'ECE',   7.2, 2024);

-- ---------- Enrollment (many-to-many Student <-> Course) ----------
CREATE TABLE Enrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

INSERT INTO Enrollment (student_id, course_id) VALUES
(101, 1), (101, 3),
(102, 2), (102, 5),
(103, 3), (103, 6),
(104, 1), (104, 2),
(105, 4), (105, 7),
(106, 2), (106, 5),
(107, 1), (107, 2), (107, 5),
(108, 7),
(109, 3), (109, 6),
(110, 4),
(111, 6), (111, 7),
(112, 1), (112, 5),
(113, 7),
(114, 3),
(115, 4);
