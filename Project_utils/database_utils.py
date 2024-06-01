import sqlite3
from typing import Dict, Optional, List, Any, Union, Tuple


def dict_factory(cursor, row) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = dict_factory
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def select(self, table_name: str, method: str, conditions: Optional[Dict[str, Any]] = None,
               columns: Optional[List[str]] = None,
               join_conditions: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        Выборка данных из базы данных
        :param table_name: Название талицы. Например: 'users'
        :param method: Метод выборки. Например: 'fetchall', 'fetchone'
        :param conditions: Условия выборки. Например: {'id': 1}
        :param columns: Колонки для выборки. Например: ['id', 'name']. Если используем JOIN и хотим поменять название
         колонки, используем "AS". Например: ['users.id AS user_id', 'users.name AS user_name']
        :param join_conditions: Соединение таблиц. Например: {'users': {'id': 'users.id'}}
        :return:
        """
        conditions_list = []
        join_conditions_list = []
        if columns:
            query = f'SELECT {", ".join(columns)} FROM {table_name}'
        else:
            query = f'SELECT * FROM {table_name}'
        if join_conditions is not None:
            for join_table, join_values in join_conditions.items():
                for key, value in join_values.items():
                    join_conditions_list.append(f"{key} = {value}")
                query += f' INNER JOIN {join_table} ON {" AND ".join(join_conditions_list)}'
        if conditions is not None:
            for key, value in conditions.items():
                conditions_list.append(f"{key} = '{value}'")
            query += f' WHERE {" AND ".join(conditions_list)}'
        cursor = self.connection.cursor()
        cursor.execute(query)
        if method == 'fetchone':
            result = cursor.fetchone()
            return result
        elif method == 'fetchall':
            result = cursor.fetchall()
            return result

    def insert(self, table_name: str, data: Dict[str, Any]):
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        query = f'INSERT INTO {table_name} ({columns}) VALUES {values}'
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def update(self, table_name: str, data: Dict[str, Any], conditions: Dict[str, Any]):
        update_conditions = []
        if conditions is not None:
            for key, value in conditions.items():
                update_conditions.append(f"{key} = '{value}'")
        update_values = []
        for key, value in data.items():
            update_values.append(f"{key} = '{value}'")
        query = f'UPDATE {table_name} SET {", ".join(update_values)} WHERE {" AND ".join(update_conditions)}'
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
