# 🏥 Clinic Management System (Odoo 17)

A custom-built Clinic Management System developed using **Odoo 17**, designed to manage core healthcare workflows including patients, doctors, appointments, visits, prescriptions, billing, reporting, and integrations with Accounting and Inventory modules.

---

## 📌 Project Overview

This project simulates a real-world clinic workflow inside Odoo ERP. It handles the full patient journey starting from appointment booking to medical visit, prescription, and invoice generation.

The system also includes reporting features and integration with Odoo Accounting and Inventory modules to ensure a complete ERP-based healthcare solution.

---

## ⚙️ Key Features

### 👤 Patient Management

* Create and manage patient records
* Link patients to Odoo contacts (`res.partner`)
* Store medical history and visit records

### 👨‍⚕️ Doctor Management

* Manage doctor profiles and schedules
* Assign doctors to appointments and visits

### 📅 Appointment System

* Book, confirm, and manage appointments
* Support follow-up appointments linked to original visits

### 🏥 Medical Visits

* Record consultation details
* Track diagnosis and treatment
* Handle visit workflow states

### 💊 Prescription Management

* Add multiple prescription lines per visit
* Link prescriptions to products (medicine catalog)

### 💰 Billing & Accounting Integration

* Auto-generate invoices from visits
* Support service-based and prescription-based billing
* Integration with Odoo Accounting (`account.move`)

### 📦 Inventory Integration

* Use `product.product` for medical services and medicines
* Track services and consumables via Inventory module

### 📊 Reporting

PDF reports generated for all core modules including patients, doctors, appointments, visits, and prescriptions. The system provides printable summaries for medical records, appointments history, clinical visits, and billing-related data to support operational and administrative workflows.

---

## 🔄 Workflow Diagram

Patient → Appointment → Visit → Prescription → Invoice → Payment

---

## 🧱 Technical Architecture

* **Framework:** Odoo 17
* **Language:** Python
* **Database:** PostgreSQL
* **UI:** XML Views (Form, Tree, Kanban)
* **Architecture Style:** MVC (Model - View - Controller)

---

## 🧠 Core Concepts Used

* Odoo ORM (create, write, update, unlink)
* Model relationships:

  * One2many / Many2one / Many2many
* Model inheritance (`_inherit`)
* Security groups and access rights
* Automated actions and business logic
* Report engine (QWeb PDF reports)

---

## 🔗 Integrations

* Odoo Accounting (`account.move`) for invoice generation
* Odoo Inventory (`product.product`) for services and medicines

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/your-username/clinic_management.git

# Move to Odoo addons path
cp -r clinic_management /odoo/custom_addons/

# Restart Odoo server
./odoo-bin -c odoo.conf

# Activate developer mode and install module
```

---

## 📁 Module Structure

```
clinic_management/
├── models/
├── views/
├── reports/
├── security/
├── data/
├── controllers/
├── static/
└── __manifest__.py
```

---

---

## 👨‍💻 Author

**Waleed**
Odoo Developer | Python | ERP Systems

---

## 📌 Note

This project is built for educational and portfolio purposes to demonstrate Odoo development skills and ERP system design capabilities.
