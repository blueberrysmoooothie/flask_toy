# from app import app
# app.run()


from my_website.module import dbModule

db = dbModule.Database()

query = f"SELECT * FROM {dbModule.DB_NAME}.USER_DATA"
row = db.executeOne(query)
db.db.close()
print(row)
