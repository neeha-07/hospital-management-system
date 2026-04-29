-- Hospital Management System Database Schema
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Users table (admin, doctor, patient)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'doctor', 'patient') NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remember_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expiry DATETIME
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    specialization ENUM('Cardiology','Neurology','Gynecology','Pediatrics','Dermatology') NOT NULL,
    qualification VARCHAR(100),
    experience INT,
    consultation_fee DECIMAL(10,2),
    available_days VARCHAR(100),
    available_timing VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    age INT,
    gender ENUM('Male','Female','Other'),
    blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-'),
    date_of_birth DATE,
    address TEXT,
    emergency_contact VARCHAR(20),
    medical_history TEXT,
    document_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    time_slot VARCHAR(50),
    status ENUM('Scheduled','Completed','Cancelled','Rescheduled') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    medicine_details TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Pharmacy / Billing table
CREATE TABLE IF NOT EXISTS billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    medicine_name VARCHAR(255),
    quantity INT,
    total_medicine_charges DECIMAL(10,2),
    consultation_charges DECIMAL(10,2),
    discount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2),
    payment_mode ENUM('Cash','Card','UPI','Insurance') DEFAULT 'Cash',
    payment_status ENUM('Pending','Paid','Partial') DEFAULT 'Pending',
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Insert default admin user (password: admin123)
INSERT INTO users (full_name, email, password_hash, role) VALUES
('Admin User', 'admin@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewDQZ0FbvhC0xK6m', 'admin')
ON DUPLICATE KEY UPDATE id=id;

select * from users;
select * from doctors;
select * from patients;
select * from appointments;
select * from prescriptions;
select * from billing;

