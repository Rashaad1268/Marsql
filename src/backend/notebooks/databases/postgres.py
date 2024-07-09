import psycopg2
from psycopg2 import sql

from notebooks.models import NoteBookDBConfig


def connect_postgres(db_conf: NoteBookDBConfig):
    return psycopg2.connect(
        f"dbname={db_conf.db_name} user={db_conf.db_user} "
        f"password={db_conf.db_password} host={db_conf.db_host} port={db_conf.db_port} "
    )


def get_postgres_db_metadata(db_config):
    db_schema = {}

    with connect_postgres(db_config) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        )
        all_tables = cursor.fetchall()

        for table in all_tables:
            table_name = table[0]
            db_schema[table_name] = []

            cursor.execute(
                sql.SQL(
                    """
                    SELECT
                        column_name,
                        data_type,
                        is_nullable
                    FROM
                        information_schema.columns
                    WHERE
                        table_name = {};
                    """
                ).format(sql.Literal(table_name))
            )

            for column_name, data_type, is_nullable in cursor.fetchall():
                # is_nullable is either 'YES' or 'NO'
                db_schema[table_name].append(
                    {
                        "name": column_name,
                        "data_type": data_type,
                        "is_nullable": is_nullable == "YES",
                    }
                )

        cursor.close()

    return db_schema


def run_postgres_query(*, db_conf: NoteBookDBConfig, query: str, do_commit: bool):
    colnames = []
    query_results = []

    with connect_postgres(db_conf) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(query)
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

        row_count = cursor.rowcount
        status_message = cursor.statusmessage

        if do_commit:
            conn.commit()

        else:
            conn.rollback()

        if cursor.description:
            colnames = [desc[0] for desc in cursor.description]

            query_results = [row for row in cursor.fetchall()]
        cursor.close()

    return {
        "status": "success",
        "columns": colnames,
        "results": query_results,
        "rows_affected": row_count,
        "status_message": status_message,
    }
