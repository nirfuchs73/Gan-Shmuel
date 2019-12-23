def my_func():
    cdb = db.get_db()
    query="select container_id as id from containers_registered where weight is NULL"
    res = cdb.execute_and_get_all(query)
    return jsonify({'list_id':[ix['id'] for ix in res], 'status':200})