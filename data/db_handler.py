import sqlite3


class LocationsDb:
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
