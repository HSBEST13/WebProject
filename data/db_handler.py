import sqlite3


class Db:
    def __init__(self):
        self.con = sqlite3.connect("db/ecology.db")
        self.cur = self.con.cursor()

    def select_category(self, category) -> list:
        returned = []
        result = self.cur.execute(f"""SELECT name, coords, address FROM locations 
        WHERE type = '{category}'""").fetchall()
        for name, coordinates, address in result:
            lat, lon = float(coordinates.split(",")[0]), float(coordinates.split(",")[1])
            returned.append([name, lat, lon, address])
        return returned

    def init_all_users(self) -> None:
        self.cur.execute("""UPDATE users SET index = 0""")
        self.con.commit()

    def init_user(self, user_id) -> None:
        self.cur.execute(f"""INSERT INTO users VALUES ('{user_id}', 0)""")
        self.con.commit()

    def set_user_index(self, user_id, count) -> None:
        self.cur.execute(f"""UPDATE users SET index += {count} WHERE user_id = '{user_id}'""")
        self.con.commit()

    def reinit_user(self, user_id) -> None:
        self.cur.execute(f"""UPDATE users SET index = 0 WHERE user_id = '{user_id}'""")
        self.con.commit()

    def get_index(self, user_id) -> str:
        result = self.cur.execute(f"""SELECT * FROM users WHERE user_id = '{user_id}'""").fetchall()
        print(result[0])
        return result[0][-1]

    def check_user(self, user_id) -> None:
        result = self.cur.execute(f"""SELECT * FROM users WHERE user_id = '{user_id}'""").fetchall()
        if len(result) == 0:
            self.init_user(user_id)
