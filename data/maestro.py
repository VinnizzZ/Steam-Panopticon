from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Infos do BD
load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")
banco = os.getenv("banco")

# Conectando no BD
DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{banco}'
engine = create_engine(DATABASE_URL)

# Function para executar procedures
def execute_stored_procedure(procedure_name, params=None):
    """
    Executes a stored procedure using raw connection to handle parameters.
    """
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        if params:
            cursor.callproc(procedure_name, params)
        else:
            cursor.callproc(procedure_name)
            
        # Fetch results if the procedure returns data (optional)
        results = []
        for result in cursor.fetchall():
            results.append(result)
            
        cursor.close()
        connection.commit() # Commit changes if the procedure modifies data
        print(f"Procedure '{procedure_name}' executed successfully.")
        return results
    except Exception as e:
        connection.rollback() # Rollback on error
        print(f"Error executing procedure '{procedure_name}': {e}")
        raise
    finally:
        connection.close()

# 3. Create your orchestrator function to define the workflow
def orchestrator():
    print("Starting the workflow orchestration...")
    try:
        # Step 1: Run the first stored procedure (e.g., data_cleanup)
        print("Running data_cleanup...")
        execute_stored_procedure('data_cleanup_procedure')

        # Step 2: Run the second procedure, potentially with parameters and fetching results
        print("Running data_processing...")
        # Example: procedure_process_data might take an input parameter '2024'
        processing_results = execute_stored_procedure('procedure_process_data', ['2024'])
        print(f"Processing results: {processing_results}")

        # Step 3: Run a final reporting procedure
        print("Running generate_report...")
        execute_stored_procedure('generate_report_procedure')

        print("Workflow completed successfully.")

    except Exception as e:
        print(f"Workflow failed: {e}")

if __name__ == "__main__":
    orchestrator()
