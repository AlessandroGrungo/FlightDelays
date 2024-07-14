from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAirportAndNumCompagnie():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.ID as id, count(distinct(f.AIRLINE_ID)) as n
        FROM airports a, flights f
        WHERE (a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID)
        GROUP BY a.ID"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["id"], row["n"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(n1, n2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct(f.ID)) as peso
        from flights f
        where (f.ORIGIN_AIRPORT_ID = %s and f.DESTINATION_AIRPORT_ID = %s)
        or (f.ORIGIN_AIRPORT_ID = %s and f.DESTINATION_AIRPORT_ID = %s)"""

        cursor.execute(query, (n1, n2, n2, n1))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result