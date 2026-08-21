from ..library import sql_Connection, deps

class Documentation:
    db: sql_Connection

class Hierarchy(Documentation):
    db = deps.doc.hierarchy

    def __init__(self, id_name: int | str):
        with self.db as connect:
            cursor = connect.cursor()
            if isinstance(id_name,int): 
                cursor.execute("""
                            SELECT *
                            FROM roles
                            WHERE id = ? 
                """, (id_name, ))
            else:
                cursor.execute("""
                            SELECT *
                            FROM roles
                            WHERE name = ?
                """, (id_name, ))
            fetch = dict(cursor.fetchone())
            self.name = fetch.get('name')
            self.id = fetch.get('id')
            self.description = fetch.get('description')
            self.buttons: dict[str, str] = {}
            for name_desc in (fetch.get('buttons', '') or '').split(r'\;'):
                if not name_desc: return
                name, desc = name_desc.split(r'\:')
                self.buttons[name] = desc

    @classmethod
    def all(cls):
        with cls.db as connect:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT id
                FROM roles
            """)
            rows = cursor.fetchall()
            return [cls(row['id']) for row in rows]