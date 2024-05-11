# Vendor Management System

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/staufique/Vendor_Management_System.git

2. Install all requirement package
   ```bash
   pip install -r requirements.txt

3. Setup smtp for sending mails to vendors in settings.py file
  go to settings and change these variables

  - `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`
  - `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
  - `EMAIL_HOST = 'smtp.gmail.com'`
  - `EMAIL_PORT = 587`
  - `EMAIL_USE_TLS = True`
  - `EMAIL_HOST_USER = 'your_email'`  # Your Gmail email address
  - `EMAIL_HOST_PASSWORD = 'your_password'`  # Your Gmail password or app-specific password

4. In models file add your email in `notify_vendor()` and `notify_to_vendor_for_status_updating()` functions.

### Note:
  If you dosn't require to send email to vendors please comment these following lines in settings.py
  - `# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`
  - `# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
  - `# EMAIL_HOST = 'smtp.gmail.com'`
  - `# EMAIL_PORT = 587`
  - `# EMAIL_USE_TLS = True`
  - `# EMAIL_HOST_USER = 'your_email'`  # Your Gmail email address
  - `# EMAIL_HOST_PASSWORD = 'your_password'`  # Your Gmail password or app-specific password

    and comment these two functions in models.py file
     `# notify_vendor()` and `# notify_to_vendor_for_status_updating()`

This document outlines the API endpoints available in the system along with their functionalities and usage instructions.

## Table of Contents

1. [User Authentication](#1-user-authentication)
   - [1.1. User Signup](#11-user-signup)
   - [1.2. User Login](#12-user-login)
   - [1.3. User Logout](#13-user-logout)
2. [Vendor Management](#2-vendor-management)
   - [2.1. Retrieve All Vendors](#21-retrieve-all-vendors)
   - [2.2. Retrieve a Specific Vendor](#22-retrieve-a-specific-vendor)
   - [2.3. Create a New Vendor](#23-create-a-new-vendor)
   - [2.4. Update a Vendor](#24-update-a-vendor)
   - [2.5. Delete a Vendor](#25-delete-a-vendor)
3. [Purchase Order Management](#3-purchase-order-management)
   - [3.1. Retrieve All Purchase Orders](#31-retrieve-all-purchase-orders)
   - [3.2. Retrieve a Specific Purchase Order](#32-retrieve-a-specific-purchase-order)
   - [3.3. Create a New Purchase Order](#33-create-a-new-purchase-order)
   - [3.4. Update a Purchase Order](#34-update-a-purchase-order)
   - [3.5. Delete a Purchase Order](#35-delete-a-purchase-order)
   - [3.6. Acknowledge a Purchase Order](#36-acknowledge-a-purchase-order)
   - [3.7. Update Delivery Status](#37-update-delivery-status)
4. [Vendor Performance](#4-vendor-performance)
   - [4.1. Retrieve Vendor Performance](#41-retrieve-vendor-performance)
   - [4.2. Retrieve Vendor Performance for a Specific Date](#42-retrieve-vendor-performance-for-a-specific-date)


## Introduction
Brief Introduction of project





## 1. User Authentication

### 1.1. User Signup

- **Endpoint:** `/api/signup/`
- **Method:** `POST`
- **Description:** Allows users to register by providing necessary information.
- **Parameters:**
  - `username` (string, required): Username of the user.
  - `email` (string, required): Email address of the user.
  - `password` (string, required): Password for the user account.
- **Response:**
  - 201 Created: User registration successful.
  - 400 Bad Request: If input data is invalid.

### 1.2. User Login

- **Endpoint:** `/api/login/`
- **Method:** `POST`
- **Description:** Allows users to log in and obtain authentication tokens.
- **Parameters:**
  - `email` (string, required): Email address of the user.
  - `password` (string, required): Password for the user account.
- **Response:**
  - 200 OK: Login successful. Returns access and refresh tokens.
  - 404 Not Found: If login credentials are invalid.

### 1.3. User Logout

- **Endpoint:** `/api/logout/`
- **Method:** `GET`
- **Description:** Logs out the currently authenticated user and invalidates tokens.
- **Response:**
  - 200 OK: Logout successful.

## 2. Vendor Management

### 2.1. Retrieve All Vendors

- **Endpoint:** `/api/vendors/`
- **Method:** `GET`
- **Description:** Retrieves a list of all vendors.
- **Response:** Returns JSON data containing information about all vendors.

### 2.2. Retrieve a Specific Vendor

- **Endpoint:** `/api/vendors/<int:id>/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific vendor identified by ID.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the vendor.
- **Response:** Returns JSON data containing information about the vendor.

### 2.3. Create a New Vendor

- **Endpoint:** `/api/vendors/`
- **Method:** `POST`
- **Description:** Allows authorized users to create a new vendor.
- **Parameters:** Provide vendor details in the request body.
- **Response:** Returns JSON data containing details of the newly created vendor.
- **Note:** Only Superuser can Create a New Vendor

### 2.4. Update a Vendor

- **Endpoint:** `/api/vendors/<int:id>/`
- **Method:** `PUT`
- **Description:** Allows authorized users to update details of an existing vendor.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the vendor to be updated.
- **Response:** Returns JSON data containing updated details of the vendor.
- **Note:** Only Superuser can Update a Vendor

### 2.5. Delete a Vendor

- **Endpoint:** `/api/vendors/<int:id>/`
- **Method:** `DELETE`
- **Description:** Allows authorized users to delete a vendor.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the vendor to be deleted.
- **Response:** Returns confirmation message upon successful deletion.
- **Note:** Only Superuser can Delete a Vendor

## 3. Purchase Order Management

### 3.1. Retrieve All Purchase Orders

- **Endpoint:** `/api/purchase_orders/`
- **Method:** `GET`
- **Description:** Retrieves a list of all purchase orders.
- **Response:** Returns JSON data containing information about all purchase orders.

### 3.2. Retrieve a Specific Purchase Order

- **Endpoint:** `/api/purchase_orders/<int:id>/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific purchase order identified by ID.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the purchase order.
- **Response:** Returns JSON data containing information about the purchase order.

### 3.3. Create a New Purchase Order

- **Endpoint:** `/api/purchase_orders/`
- **Method:** `POST`
- **Description:** Allows authorized users to create a new purchase order.
- **Parameters:** Provide purchase order details in the request body.
- **Response:** Returns JSON data containing details of the newly created purchase order.
- **Note:** If Purchase Order Created Vendor Will Get an mail for acknowledge the order.

### 3.4. Update a Purchase Order

- **Endpoint:** `/api/purchase_orders/<int:id>/`
- **Method:** `PUT`
- **Description:** Allows authorized users to update details of an existing purchase order.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the purchase order to be updated.
- **Response:** Returns JSON data containing updated details of the purchase order.

### 3.5. Delete a Purchase Order

- **Endpoint:** `/api/purchase_orders/<int:id>/`
- **Method:** `DELETE`
- **Description:** Allows authorized users to delete a purchase order.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the purchase order to be deleted.
- **Response:** Returns confirmation message upon successful deletion.

### 3.6. Acknowledge a Purchase Order

- **Endpoint:** `/api/purchase_orders/<int:id>/acknowledge/`
- **Method:** `GET`
- **Description:** Allows vendors to acknowledge receipt of a purchase order.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the purchase order to be acknowledged.
- **Response:** Returns JSON data confirming the acknowledgment.
- **Note:** After Acknowledgement vendor will get an another mail to update the status of an order.

### 3.7. Update Delivery Status

- **Endpoint:** `/api/status/<int:id>/<str:status>/`
- **Method:** `GET`
- **Description:** Allows updating the delivery status of a purchase order.
- **Parameters:**
  - `id` (integer, required): Unique identifier of the purchase order.
  - `status` (string, required): New status of the purchase order (delivered or cancelled).
- **Response:** Returns JSON data containing updated details of the purchase order.

## 4. Vendor Performance

### 4.1. Retrieve Vendor Performance

- **Endpoint:** `/api/vendors/<int:vendor_id>/performance/`
- **Method:** `GET`
- **Description:** Retrieves performance metrics for a specific vendor.
- **Parameters:**
  - `vendor_id` (integer, required): Unique identifier of the vendor.
- **Response:** Returns JSON data containing performance metrics.

### 4.2. Retrieve Vendor Performance for a Specific Date

- **Endpoint:** `/api/vendors/<int:vendor_id>/performance/<str:date>/`
- **Method:** `GET`
- **Description:** Retrieves performance metrics for a specific vendor on a given date.
- **Parameters:**
  - `vendor_id` (integer, required): Unique identifier of the vendor.
  - `date` (string, required): Date for which performance metrics are requested (format: YYYY-MM-DD).
- **Response:** Returns JSON data containing performance metrics for the specified date.
