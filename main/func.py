def get_data(query,db,params=[]):
    
    db.execute(query,params)
    data = db.fetchall()
    return data
