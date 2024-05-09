API Endpoints README
This document outlines the API endpoints available in the system along with their functionalities and usage instructions.

Table of Contents
1. User Authentication
1.1. User Signup
1.2. User Login
1.3. User Logout
2. Vendor Management
2.1. Retrieve All Vendors
2.2. Retrieve a Specific Vendor
2.3. Create a New Vendor
2.4. Update a Vendor
2.5. Delete a Vendor
3. Purchase Order Management
3.1. Retrieve All Purchase Orders
3.2. Retrieve a Specific Purchase Order
3.3. Create a New Purchase Order
3.4. Update a Purchase Order
3.5. Delete a Purchase Order
3.6. Acknowledge a Purchase Order
3.7. Update Delivery Status
4. Vendor Performance
4.1. Retrieve Vendor Performance
4.2. Retrieve Vendor Performance for a Specific Date
1. User Authentication
1.1. User Signup
Endpoint: /api/signup/
Method: POST
Description: Allows users to register by providing necessary information.
Parameters:
email (string, required): Email address of the user.
password (string, required): Password for the user account.
Response:
201 Created: User registration successful.
400 Bad Request: If input data is invalid.
1.2. User Login
Endpoint: /api/login/
Method: POST
Description: Allows users to log in and obtain authentication tokens.
Parameters:
email (string, required): Email address of the user.
password (string, required): Password for the user account.
Response:
200 OK: Login successful. Returns access and refresh tokens.
404 Not Found: If login credentials are invalid.
1.3. User Logout
Endpoint: /api/logout/
Method: GET
Description: Logs out the currently authenticated user and invalidates tokens.
Response:
200 OK: Logout successful.
2. Vendor Management
2.1. Retrieve All Vendors
Endpoint: /api/vendors/
Method: GET
Description: Retrieves a list of all vendors.
Response: Returns JSON data containing information about all vendors.
2.2. Retrieve a Specific Vendor
Endpoint: /api/vendors/<int:id>/
Method: GET
Description: Retrieves details of a specific vendor identified by ID.
Parameters:
id (integer, required): Unique identifier of the vendor.
Response: Returns JSON data containing information about the vendor.
2.3. Create a New Vendor
Endpoint: /api/vendors/
Method: POST
Description: Allows authorized users to create a new vendor.
Parameters: Provide vendor details in the request body.
Response: Returns JSON data containing details of the newly created vendor.
2.4. Update a Vendor
Endpoint: /api/vendors/<int:id>/
Method: PUT
Description: Allows authorized users to update details of an existing vendor.
Parameters:
id (integer, required): Unique identifier of the vendor to be updated.
Response: Returns JSON data containing updated details of the vendor.
2.5. Delete a Vendor
Endpoint: /api/vendors/<int:id>/
Method: DELETE
Description: Allows authorized users to delete a vendor.
Parameters:
id (integer, required): Unique identifier of the vendor to be deleted.
Response: Returns confirmation message upon successful deletion.
3. Purchase Order Management
3.1. Retrieve All Purchase Orders
Endpoint: /api/purchase_orders/
Method: GET
Description: Retrieves a list of all purchase orders.
Response: Returns JSON data containing information about all purchase orders.
3.2. Retrieve a Specific Purchase Order
Endpoint: /api/purchase_orders/<int:id>/
Method: GET
Description: Retrieves details of a specific purchase order identified by ID.
Parameters:
id (integer, required): Unique identifier of the purchase order.
Response: Returns JSON data containing information about the purchase order.
3.3. Create a New Purchase Order
Endpoint: /api/purchase_orders/
Method: POST
Description: Allows authorized users to create a new purchase order.
Parameters: Provide purchase order details in the request body.
Response: Returns JSON data containing details of the newly created purchase order.
3.4. Update a Purchase Order
Endpoint: /api/purchase_orders/<int:id>/
Method: PUT
Description: Allows authorized users to update details of an existing purchase order.
Parameters:
id (integer, required): Unique identifier of the purchase order to be updated.
Response: Returns JSON data containing updated details of the purchase order.
3.5. Delete a Purchase Order
Endpoint: /api/purchase_orders/<int:id>/
Method: DELETE
Description: Allows authorized users to delete a purchase order.
Parameters:
id (integer, required): Unique identifier of the purchase order to be deleted.
Response: Returns confirmation message upon successful deletion.
3.6. Acknowledge a Purchase Order
Endpoint: /api/purchase_orders/<int:id>/acknowledge/
Method: GET
Description: Allows vendors to acknowledge receipt of a purchase order.
Parameters:
id (integer, required): Unique identifier of the purchase order to be acknowledged.
Response: Returns JSON data confirming the acknowledgment.
3.7. Update Delivery Status
Endpoint: /api/status/<int:id>/<str:status>/
Method: GET
Description: Allows updating the delivery status of a purchase order.
Parameters:
id (integer, required): Unique identifier of the purchase order.
status (string, required): New status of the purchase order (delivered or cancelled).
Response: Returns JSON data containing updated details of the purchase order.
4. Vendor Performance
4.1. Retrieve Vendor Performance
Endpoint: /api/vendors/<int:vendor_id>/performance/
Method: GET
Description: Retrieves performance metrics for a specific vendor.
Parameters:
vendor_id (integer, required): Unique identifier of the vendor.
Response: Returns JSON data containing performance metrics.
4.2. Retrieve Vendor Performance for a Specific Date
Endpoint: /api/vendors/<int:vendor_id>/performance/<str:date>/
Method: GET
Description: Retrieves performance metrics for a specific vendor on a given date.
Parameters:
vendor_id (integer, required): Unique identifier of the vendor.
date (string, required): Date for which performance metrics are requested (format: YYYY-MM-DD).
Response: Returns JSON data containing performance metrics for the specified date.