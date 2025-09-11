import psycopg2
from urllib.parse import urlparse

# Neon serverless connection string
DATABASE_URL = "postgresql://neondb_owner:npg_0dqKAi5MFHjY@ep-odd-cake-a1dyyak1-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Parse the URL
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]  # remove leading /
hostname = result.hostname
port = result.port or 5432
sslmode = 'require'  # Neon serverless always needs SSL

try:
    connection = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
        sslmode=sslmode
    )
    cursor = connection.cursor()
    print("Connected to Neon serverless successfully!")

    # Example query
    cursor.execute("SELECT NOW()")
    print("Server time:", cursor.fetchone())

except Exception as e:
    print("Error:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
