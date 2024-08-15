from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json

# Define the Pydantic model matching the schema
class SourceCodeIndex(BaseModel):
    file: str
    lines: int
    md5: str
    name: str
    purpose: str
    classes: str
    functions: str
    tokens: int
    
    def print(self) -> None:
        parsed_json = json.loads(self.json())

        # Convert classes string to json array
        parsed_json["classes"] = json.loads(parsed_json["classes"])
        parsed_json["functions"] = json.loads(parsed_json["functions"])

        # Print non-ASCII string instead unicode for multiple languages
        pretty_json = json.dumps(parsed_json, ensure_ascii=False, indent=2)
        print(pretty_json)


# Define the SqliteUtil class
class SqliteUtil:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS indexes (
                file TEXT PRIMARY KEY,
                lines INTEGER,
                md5 TEXT,
                name TEXT,
                purpose TEXT,
                classes TEXT,
                functions TEXT,
                tokens INTEGER
            )
        ''')
        self.connection.commit()

    def insert_row(self, file, lines, md5, name, purpose, classes, functions, tokens):
        try:
            self.cursor.execute('''
                INSERT INTO indexes (file, lines, md5, name, purpose, classes, functions, tokens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (file, lines, md5, name, purpose, classes, functions, tokens))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting row: {e}")

    def insert_index(self, index: SourceCodeIndex):
        self.insert_row(index.file, index.lines, index.md5, index.name, index.purpose, index.classes, index.functions, index.tokens)

    def update_index(self, index: SourceCodeIndex):
        self.update_row(index.file, index.lines, index.md5, index.name, index.purpose, index.classes, index.functions, index.tokens)

    def update_row(self, file, lines=None, md5=None, name=None, purpose=None, classes=None, functions=None, tokens=None):
        query = "UPDATE indexes SET "
        params = []
        if lines is not None:
            query += "lines = ?, "
            params.append(lines)
        if md5 is not None:
            query += "md5 = ?, "
            params.append(md5)
        if name is not None:
            query += "name = ?, "
            params.append(name)
        if purpose is not None:
            query += "purpose = ?, "
            params.append(purpose)
        if classes is not None:
            query += "classes = ?, "
            params.append(classes)
        if functions is not None:
            query += "functions = ?, "
            params.append(functions)            
        if tokens is not None:
            query += "tokens = ?, "
            params.append(tokens)

        query = query.rstrip(', ')
        query += " WHERE file = ?"
        params.append(file)

        self.cursor.execute(query, tuple(params))
        self.connection.commit()

    def row_exists(self, file):
        self.cursor.execute("SELECT 1 FROM indexes WHERE file = ?", (file,))
        return self.cursor.fetchone() is not None

    def select_row(self, file):
        self.cursor.execute("SELECT * FROM indexes WHERE file = ?", (file,))
        row = self.cursor.fetchone()
        if row:
            return SourceCodeIndex(**{
                "file": row[0],
                "lines": row[1],
                "md5": row[2],
                "name": row[3],
                "purpose": row[4],
                "classes": row[5],
                "functions": row[6],
                "tokens": row[7]
            })
        return None

    def select_all_rows(self) -> List[SourceCodeIndex]:
        self.cursor.execute("SELECT * FROM indexes")
        rows = self.cursor.fetchall()
        return [SourceCodeIndex(**{
            "file": row[0],
            "lines": row[1],
            "md5": row[2],
            "name": row[3],
            "purpose": row[4],
            "classes": row[5],
            "functions": row[6],
            "tokens": row[7]
        }) for row in rows]
    
    def count_all_tokens(self) -> List[SourceCodeIndex]:
        self.cursor.execute("SELECT sum(tokens) FROM indexes")
        rows = self.cursor.fetchall()
        return rows[0][0]

    def delete_row(self, file: str):
        """Delete a row from the indexes table based on the file name."""
        self.cursor.execute("DELETE FROM indexes WHERE file = ?", (file,))
        self.connection.commit()
        
    def close(self):
        self.connection.close()

# Example Usage:
# db_util = SqliteUtil('example.db')
# db_util.insert_row('file1.txt', 100, 'md5hash1', 'File One', 'Purpose One', 'Class One')
# exists = db_util.row_exists('file1.txt')
# print("Row exists:", exists)
# db_util.update_row('file1.txt', lines=200)
# row = db_util.select_row('file1.txt')
# print(row)
# all_rows = db_util.select_all_rows()
# for row in all_rows:
#     print(row)
# db_util.close()


def main():
    db_name = "source_code_index.db"
    db_util = SqliteUtil(db_name)

    file = "/Users/tobe/code/orchard_universe/basket/basket/cli.py"
    print(db_util.row_exists(file))

    row = db_util.select_row(file)
    print(row)

    print(db_util.select_all_rows())

    # db_util.insert_row('file1.txt', 100, 'md5hash1', 'File One', 'Purpose One', 'Class One')
    # exists = db_util.row_exists('file1.txt')
    # print("Row exists:", exists)
    # db_util.update_row('file1.txt', lines=200)
    # row = db_util.select_row('file1.txt')
    # print(row)
    # db_util.close()

if __name__ == "__main__":
    main()