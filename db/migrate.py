"""
FilePath: db/migrate.py
Author: Joel
Date: 2025-08-14 19:10:10
LastEditTime: 2025-08-14 19:11:17
Description: 数据迁移
"""
import sqlite3
import psycopg2
from psycopg2 import sql

# 1. 连接本地 SQLite
sqlite_conn = sqlite3.connect("site.db")
sqlite_cursor = sqlite_conn.cursor()

# 2. 连接 Neon PostgreSQL
pg_conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_cAPUBmlDEI05@ep-winter-fog-adnsxuce-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
)
pg_cursor = pg_conn.cursor()

# 3. 获取 SQLite 中的所有表
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]
    print(f"正在迁移表: {table_name}")

    # 获取列信息
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in sqlite_cursor.fetchall()]
    columns_str = ", ".join(columns)

    # 获取所有数据
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # 在 PostgreSQL 中创建表（简单映射为 text）
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([col + ' TEXT' for col in columns])}
    );
    """
    pg_cursor.execute(create_table_query)

    # 插入数据
    for row in rows:
        placeholders = ", ".join(["%s"] * len(row))
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(columns_str),
            sql.SQL(placeholders)
        )
        pg_cursor.execute(insert_query, row)

# 4. 提交并关闭
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("迁移完成！")
