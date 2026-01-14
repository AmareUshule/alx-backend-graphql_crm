import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{now} CRM is alive\n"
    log_file_path = "/tmp/crm_heartbeat_log.txt"

    # Append to log file
    with open(log_file_path, "a") as f:
        f.write(log_message)

    # Optional: query GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL endpoint responsive: {result}\n")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL endpoint error: {e}\n")

