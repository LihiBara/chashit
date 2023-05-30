from CashitDB import CashitDB


def charging(username, amount, current_money):
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


