#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def main():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    query = gql("""
    query {
        orders(orderDate_Gte: "%s") {
            id
            customer {
                email
            }
        }
    }
    """ % seven_days_ago)

    result = client.execute(query)

    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in result.get("orders", []):
            log.write(f"{timestamp} - Order {order['id']} | {order['customer']['email']}\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()

