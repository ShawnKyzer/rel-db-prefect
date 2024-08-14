FROM python:3.12

# Install ODBC driver for SQL Server
RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Python dependencies
RUN pip install pyodbc psycopg2-binary

WORKDIR /app
#COPY data_transfer.py .

#CMD ["python", "data_transfer.py"]