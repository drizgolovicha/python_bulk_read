import csv
import psycopg2
from cStringIO import StringIO
import time


def getResults(stream):
    """
    get result generator
    """

    f = StringIO(stream)
    result = csv.DictReader(f, restkey=None)

    for item in result:
        yield item

    f.close()


class BulkSelect:
    def __init__(self):
        """
        Init connection
        """
        conStr = "postgresql://<user>:<pwd>@localhost:5432/<db_name>"
        self.conn = psycopg2.connect(conStr)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """
        Clean memory, close connections
        """
        self.cursor.close()
        self.conn.close()

    def getData(self):
        """
        Common way to load big data set

        :return List:
        """
        start_time = time.time()
        query = """
            SELECT * from big_data inner join big_data as t1 USING(fname)
        """

        self.cursor.execute(query)

        result = list()
        for item in self.cursor:
            result.append(item)

        print("--- %s seconds ---" % (time.time() - start_time))
        return result

    def getDataCopy(self):
        """
        COPY approach to load big data set

        :return List:
        """
        start_time = time.time()
        query = """
            SELECT * from big_data inner join big_data as t1 USING(fname)
        """

        output = StringIO()
        self.cursor.copy_expert("COPY (%s) TO STDOUT (FORMAT 'csv', HEADER true)" % query, output)

        data = output.getvalue()
        output.close()

        result = list()
        for item in getResults(data):
            # do whatever we need
            item = {k: None if v == "" else v for k, v in item.items()}

            result.append(item)

        print("--- %s seconds ---" % (time.time() - start_time))
        return result

dalc = BulkSelect()
dalc.getData()
dalc.getDataCopy()
