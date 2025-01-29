import requests
from dotenv import load_dotenv
import os

load_dotenv()


def create_admin_users(base_url, db, admin_username, admin_password, num_users):
    """Create multiple admin users."""
    session = requests.Session()
    login_url = f"{base_url}/web/session/authenticate"
    create_user_url = f"{base_url}/web/dataset/call_kw/res.users/create"

    # Log in as the main admin user
    login_response = session.post(login_url, json={
        "params": {
            "db": db,
            "login": admin_username,
            "password": admin_password,
        }
    })

    if login_response.status_code != 200:
        raise Exception("Admin login failed")

    # Create multiple admin users
    for i in range(1, num_users + 1):
        new_username = f"admin{i}"
        new_password = "adminLoadTest123"  # You can change this if needed

        create_user_response = session.post(create_user_url, json={
            "params": {
                "model": "res.users",
                "method": "create",
                "args": [{
                    "name": new_username,
                    "login": new_username,
                    "password": new_password,
                    "groups_id": [(4, 1)]  # Add to the admin group
                }],
                "kwargs": {}
            }
        })

        if create_user_response.status_code != 200:
            print(f"Failed to create user {new_username}")
        else:
            print(f"Created user {new_username}")


# Example usage
create_admin_users(
    base_url=os.getenv("ODOO_HOST"),
    db=os.getenv("ODOO_DB_NAME"),
    admin_username=os.getenv("ODOO_ADMIN_USERNAME"),
    admin_password=os.getenv("ODOO_ADMIN_PASSWORD"),
    num_users=int(os.getenv("NUM_ADMIN_USERS"))
)
