import models

models.db.connect()

# This is for 2nd and others migrations
try:
    print("Try to remove table Measures...")
    models.db.drop_table(models.Measures)
except:
    print("Table Measures does not exists!")
finally:
    print("Try to create table Measures...")
    models.db.create_table(models.Measures)

# This id for 1st migration
#print("Try to create table Measures...")
#models.db.create_table(models.Measures)

models.db.close()