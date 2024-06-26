def get_colnames(cursor):
    """Get column names for cursor's result set"""
    return [coldesc[0] for coldesc in cursor.description]


def parse_query(query: str):
    query_lower = query.lower()
    if not ("select " in query_lower or "returning " in query_lower):
        if query.endswith(";"):
            query = query[:-1]

        if "delete" in query_lower or "update" in query_lower or "insert" in query_lower:
            query += " RETURNING *;"

    return query
