file = 'imagefile.png'
ext = ['png', 'jpg']

sql = 'SELECT {tn} FROM {tn} WHERE {cn}="Hi World" LIMIT 10'
sql = sql.format(tn='table_name', cn='column_2')

print(sql)


