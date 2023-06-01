"""
author - lihi
date   - 29 / 05 / 23
bank
"""
from CashitDB import CashitDB


def charging(username, amount, current_money):
    """
    a function that charge the account with money from the bank by credit card
    :param username:
    :param amount:
    :param current_money:
    :return:
    """
    amount = int(amount)
    updated_money = current_money + amount

    # Validate that user is existed in DB

    conn = CashitDB().create_connection()
    with conn:
        query = "UPDATE users SET sum = ? WHERE username = ?"
        result = conn.execute(query, (updated_money, username))
        conn.commit()
        # return result

    conn.close()


