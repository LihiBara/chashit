from CashitDB import CashitDB

def charging(username, amount , current_money):

    updated_money = current_money + amount

    # Validate that user is existed in DB

    submit_button = Button(self.recieve_window, text="Submit", command=self.submit_receive)
     submit_button.pack(pady=5)

    conn = CashitDB().create_connection()
    with conn:
        query = "UPDATE users SET sum = ? WHERE username = ?"
        result = conn.execute(query, (updated_money, username))
        conn.commit()
        # return result

    conn.close()
