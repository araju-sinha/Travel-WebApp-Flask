# import pymysql
# #pymysql.install_as_MySQLdb()
# import aws_credentials as rds
# conn = pymysql.connect(
#         host = rds.database.cpffxsfmdxow.ap-south-1.rds.amazonaws.com,
#         port = rds.3306,
#         user = rds.admin,
#         password = rds.aarju1234,
#         db = rds.aarju,
#         )
#
# cursor=conn.cursor()
# create_table="""
# create table Details (name varchar(200),email varchar(200),phone varchar(20) )
#
# """
# cursor.execute(create_table)
#
# def insert_details(name,email,phone):
#     cur=conn.cursor()
#     cur.execute("INSERT INTO DETAILS (name,email,phone) VALUES (%s,%s,%s)", (name,email,phone))
#     conn.commit()
