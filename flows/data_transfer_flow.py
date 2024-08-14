import pandas as pd
from prefect import flow, task
from sqlalchemy import create_engine, text
from prefect.blocks.system import Secret
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

@task(name="Extract data from MSSQL")
def extract_from_mssql():
    mssql_connection_string = Secret.load("mssql-connection-string").get()
    engine = create_engine(mssql_connection_string)
    
    with engine.connect() as connection:
        query = text("SELECT * FROM Equipment")
        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

@task(name="Load data to PostgreSQL")
def load_to_postgres(df: pd.DataFrame):
    postgres_connection_string = Secret.load("postgres-connection-string").get()
    engine = create_engine(postgres_connection_string)
    
    with engine.connect() as connection:
        # Create the wrk_Equipment table if it doesn't exist
        create_table_query = text("""
        CREATE TABLE IF NOT EXISTS wrk_Equipment (
            id SERIAL PRIMARY KEY,
            EquipmentName VARCHAR(100),
            SerialNumber VARCHAR(50),
            PurchaseDate DATE,
            LastCalibrationDate DATE,
            NextCalibrationDate DATE,
            Status VARCHAR(20)
        )
        """)
        connection.execute(create_table_query)
        connection.commit()
        
        # Insert the data
        df.to_sql('wrk_Equipment', engine, if_exists='replace', index=False)

@flow(name="MSSQL to PostgreSQL Data Transfer")
def transfer_data():
    data = extract_from_mssql()
    load_to_postgres(data)
    print(f"Transferred {len(data)} rows from MSSQL to PostgreSQL")

if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow=transfer_data,
        name="data-transfer-deployment",
        work_queue_name="default",
        schedule=(CronSchedule(cron="0 0 * * *", timezone="UTC")),  # Run daily at midnight UTC
    )
    deployment.apply()