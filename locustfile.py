from locust import HttpUser, task, between, events
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class OdooUser(HttpUser):
    host = os.getenv("ODOO_HOST")
    db_name = os.getenv("ODOO_DB_NAME")
    wait_time = between(1, 2)
    admin_users = [f"admin{i}" for i in range(1, int(os.getenv("NUM_ADMIN_USERS")) + 1)]
    current_user_index = 0

    def on_start(self):
        """Log in as an admin user when the user starts."""
        self.login()

    def login_old(self):
        """Log in to Odoo."""
        response = self.client.post("/web/session/authenticate", json={
            "params": {
                "db": self.db_name,  # Replace with your Odoo database name
                "login": "admin",  # Replace with your admin user email
                "password": "admin",  # Replace with your admin user password
            }
        }, name='login1')
        if response.status_code != 200:
            raise Exception("Login failed")
        self.session_id = response.cookies.get("session_id")
        print("Logged in successfully")

    def login(self):
        """Log in to Odoo using round-robin for admin users."""
        username = OdooUser.admin_users[OdooUser.current_user_index]
        OdooUser.current_user_index = (OdooUser.current_user_index + 1) % len(OdooUser.admin_users)

        response = self.client.post("/web/session/authenticate", json={
            "params": {
                "db": self.db_name,  # Replace with your Odoo database name
                "login": "admin2",  # Replace with your admin user email
                "password": "admin123456",  # Replace with your admin user password
            }
        }, name=f'login')
        # print(response.json())

        if response.status_code != 200:
            raise Exception("Login failed")
        self.session_id = response.cookies.get("session_id")
        if not self.session_id:
            raise Exception(f"Failed to log in for user {username}")
        print(f"Logged in successfully as {username}")

    @task
    def create_sales_order(self):
        """Create a sales order."""
        product_id = self.get_random_product()
        print(f'Found product: {product_id}')
        if not product_id:
            return

        response = self.client.post("/web/dataset/call_kw/sale.order/create", json={
            "params": {
                "model": "sale.order",
                "method": "create",
                "args": [{
                    "partner_id": 1,  # Replace with a valid partner ID
                    "order_line": [(0, 0, {
                        "product_id": product_id,
                        "product_uom_qty": 1,
                    })]
                }],
                "kwargs": {},
            },
            "session_id": self.session_id,
        }, name='create_sales_order')
        if response.status_code != 200:
            print("Failed to create sales order")
        print("Created sales order", response.json().get("result"))

    @task
    def validate_sales_order(self):
        """Search for and validate a sales order that is not in 'Done' status."""
        response = self.client.post("/web/dataset/call_kw/sale.order/search_read", json={
            "params": {
                "model": "sale.order",
                "method": "search_read",
                "args": [[("state", "!=", "done")]],  # Search for orders not in 'Done' status
                "kwargs": {"limit": 1},
            },
            "session_id": self.session_id,
        }, name='search_unvalidated_sales_order')
        if response.status_code != 200:
            print("Failed to search for sales orders")
            return

        orders = response.json().get("result", [])
        if not orders:
            print("No sales orders found to validate")
            return

        order_id = orders[0]["id"]
        self.client.post("/web/dataset/call_kw/sale.order/action_confirm", json={
            "params": {
                "model": "sale.order",
                "method": "action_confirm",
                "args": [[order_id]],
                "kwargs": {},
            },
            "session_id": self.session_id,
        }, name='validate_sales_order')

    @task
    def get_random_product(self):
        """Get a random product ID."""
        response = self.client.post(
            "/web/dataset/call_kw/product.product/search_read",
            json={
                "params": {
                    "model": "product.product",
                    "method": "search_read",
                    "args": [[]],
                    "kwargs": {"limit": 10},
                },
                "session_id": self.session_id,
            },
            headers={"Content-Type": "application/json"},
            name='get_random_product'
        )
        if response.status_code != 200:
            print("Failed to fetch products")
            return None

        products = response.json().get("result", [])
        if not products:
            print("No products found")
            return None

        product_id = random.choice(products)["id"]
        print(f"Random product ID: {product_id}")  # Debugging output
        return product_id

# @task
# def download_sales_order_report(self):
#     """Simulate downloading a sales order report without saving the PDF."""
#     # Step 1: Search for a random sales order
#     response = self.client.post("/web/dataset/call_kw/sale.order/search_read", json={
#         "params": {
#             "model": "sale.order",
#             "method": "search_read",
#             "args": [[]],  # Search for orders not in 'Done' status
#             "kwargs": {"limit": 1},
#         },
#         "session_id": self.session_id,
#     }, name='search_sales_order')
#     if response.status_code != 200:
#         print("Failed to search for sales orders")
#         return
#
#     orders = response.json().get("result", [])
#     if not orders:
#         print("No sales orders found to generate a report")
#         return
#
#     # Step 2: Randomly select a sales order
#     order = random.choice(orders)
#     order_id = order["id"]
#     print(f"Selected sales order for report: {order_id}")
#
#     # Step 3: Simulate downloading the report
#     report_url = f"/report/pdf/sale.report_saleorder/{order_id}"
#     response = self.client.get(
#         report_url,
#         headers={"Cookie": f"session_id={self.session_id}"},
#         name="download_sales_order_report",
#     )
#     if response.status_code == 200:
#         print(f"Successfully simulated download of report for sales order {order_id}")
#     else:
#         print(f"Failed to download report for sales order {order_id}")
