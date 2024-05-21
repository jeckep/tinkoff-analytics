import os
from datetime import datetime

from dotenv import load_dotenv
from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationType

load_dotenv()

token = os.environ["TINKOFF_TOKEN"]


def print_deposites():
    with Client(token) as client:
        accounts = client.users.get_accounts()
        account_id = accounts.accounts[0].id

        def get_request(cursor=""):
            return GetOperationsByCursorRequest(
                # from_=datetime(2022, 1, 1),
                account_id=account_id,
                operation_types=[OperationType(1)],  # only PayIn operations
                cursor=cursor
            )

        deposites = []
        operations = client.operations.get_operations_by_cursor(get_request())
        for op in operations.items:
            deposites.append({'currency': op.payment.currency,
                              'amount': op.payment.units, 'date': op.date.strftime('%Y-%m-%d')})

        while operations.has_next:
            request = get_request(cursor=operations.next_cursor)
            operations = client.operations.get_operations_by_cursor(request)
            for op in operations.items:
                deposites.append({'currency': op.payment.currency, 'amount': op.payment.units,
                                  'date': op.date.strftime('%Y-%m-%d')})

        for dep in deposites:
            print(dep['currency'], dep['amount'], dep['date'])


def get_portfolio_sum():
    with Client(token) as client:
        accounts = client.users.get_accounts()
        account_id = accounts.accounts[0].id

        portfolio = client.operations.get_portfolio(account_id=account_id)
        return portfolio.total_amount_portfolio.units


if __name__ == "__main__":
    portfolio_sum = get_portfolio_sum()
    print(f"Текущая  рублёвая стоимость портфеля: {portfolio_sum:n} руб\n")

    print_deposites()
