# Load Testing Odoo with Locust

This project is designed to perform load testing on an Odoo instance using Locust. It includes scripts to create admin
users and simulate user behavior.

## Project Structure

- `requirements.txt`: Contains the Python dependencies for the project.
- `user_creator.py`: Script to create admin users in the Odoo instance.
- `locustfile.py`: Locust script to simulate user load and behavior.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.7+**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies.

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

---

#### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

- **Windows**:
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
    python -m venv venv
    source venv/bin/activate
    ```
  

---

#### 3. Install Dependencies

```markdown
### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```


---

#### 4. Configure Environment Variables

```markdown
### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

# .env
ODOO_HOST=<ODOO_HOST>
ODOO_DB_NAME=<ODOO_DB_NAME>
ODOO_ADMIN_USERNAME=<ODOO_ADMIN_USERNAME>
ODOO_ADMIN_PASSWORD=<ODOO_ADMIN_PASSWORD>
NUM_ADMIN_USERS=<NUM_ADMIN_USERS>
```


---

#### 5. Create Admin Users to be used in the Load Test

```markdown
### 5. Create Admin Users

Run the `user_creator.py` script to create admin users in the Odoo instance:

```bash
python user_creator.py
```


---

#### 6. Run Locust Load Test

```markdown
### 6. Run Locust Load Test

Start the Locust load test using the `locustfile.py` script:

```bash
locust -f locustfile.py
```


---

## Running the First Test
1. Open your browser and navigate to the Locust web interface:
http://localhost:8089
2. Set the number of users and spawn rate:
- **Number of users**: Total number of simulated users.
- **Spawn rate**: Number of users to start per second.
- **Host**: Enter the Odoo instance URL (e.g., `your-db-name.odoo.com`).

3. Click **Start** to begin the load test.

4. Monitor the test results in real-time on the Locust dashboard.

## Troubleshooting

- **Login Failures**: Ensure the `.env` file contains the correct Odoo credentials and database name.
- **Low QPS**: Check the server resources (CPU, memory, etc.) and database performance during the test.
- **Locust Errors**: Verify that the Locust script is correctly configured and the Odoo instance is accessible.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## Contact
For questions or support, please contact [Adnan Sabbir](https://www.linkedin.com/in/adnansabbir/).