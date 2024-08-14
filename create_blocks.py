from prefect.blocks.system import Secret
from prefect import get_client
import asyncio

async def create_blocks():
    async with get_client() as client:
        # MSSQL connection string
        mssql_secret = Secret(
            value="mssql+pyodbc://sa:YourStrong@Passw0rd@mssql:1433/LabEquipment?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        )
        await mssql_secret.save("mssql-connection-string")

        # PostgreSQL connection string
        postgres_secret = Secret(
            value="postgresql://prefect:password@postgres:5432/prefect"
        )
        await postgres_secret.save("postgres-connection-string")

if __name__ == "__main__":
    asyncio.run(create_blocks())