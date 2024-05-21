import os
from datetime import datetime

from dotenv import load_dotenv
from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationType

load_dotenv()

token = os.environ["TINKOFF_TOKEN"]

OPERATION_TYPE_INPUT = OperationType(1)
OPERATION_TYPE_OUTPUT = OperationType(9)


def get_acc_ids():
    with Client(token) as client:
        accounts = client.users.get_accounts().accounts
        return [acc.id for acc in accounts]

def print_deposites():
    with Client(token) as client:
        op_dtos = []
        accounts = get_acc_ids()
        for account_id in accounts:
            def get_request(cursor=""):
                return GetOperationsByCursorRequest(
                    account_id=account_id,
                    operation_types=[OPERATION_TYPE_INPUT, OPERATION_TYPE_OUTPUT],
                    cursor=cursor
                )
            operations = client.operations.get_operations_by_cursor(get_request())
            for op in operations.items:
                op_dtos.append({'currency': op.payment.currency,
                                  'amount': op.payment.units, 'date': op.date.strftime('%Y-%m-%d')})

            while operations.has_next:
                request = get_request(cursor=operations.next_cursor)
                operations = client.operations.get_operations_by_cursor(request)
                for op in operations.items:
                    op_dtos.append({'currency': op.payment.currency, 'amount': op.payment.units,
                                      'date': op.date.strftime('%Y-%m-%d')})

        for op in op_dtos:
            print(op['currency'], op['amount'], op['date'], sep='\t')


def get_portfolios_sum():
    with Client(token) as client:
        accounts = get_acc_ids()
        total = 0
        for account_id in accounts:
            portfolio = client.operations.get_portfolio(account_id=account_id)
            total += portfolio.total_amount_portfolio.units
        return total


if __name__ == "__main__":
    print(get_acc_ids())
    portfolio_sum = get_portfolios_sum()
    print(f"Текущая  рублёвая стоимость портфеля: {portfolio_sum:n} руб\n")

    print_deposites()
