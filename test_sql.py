import sqlite3

# conn = sqlite3.connect('data/userdata.db')
# conn = sqlite3.connect('data/admins.db')
conn = sqlite3.connect('data/doctors.db')

# print ("Ma'lumotlar bazasi muvaffaqiyatli ochildi");

# conn.execute('''CREATE TABLE USERS
#          (ID INT PRIMARY KEY     NOT NULL,
#          FISH            TEXT    NOT NULL,
#          PAROL           TEXT    NOT NULL);''')
# print ("Jadval muvaffiqaytli yaratildi!");

# conn.execute('''CREATE TABLE ADMINS
#          (ID INT PRIMARY  KEY     NOT NULL,
#          LOGIN            TEXT    NOT NULL,
#          PAROL            TEXT    NOT NULL);''')
# print ("Jadval muvaffiqaytli yaratildi!");
# conn.execute("INSERT INTO ADMINS (ID,LOGIN,PAROL) VALUES (1, 'shohabbosdev', 'Shoh@bbosdev1441')");

# conn.execute('''CREATE TABLE DOCTORS
#          (ID INT PRIMARY  KEY     NOT NULL,
#          LOGIN            TEXT    NOT NULL,
#          PAROL            TEXT    NOT NULL);''')
# print ("Jadval muvaffiqaytli yaratildi!");
# conn.execute("INSERT INTO DOCTORS (ID,LOGIN,PAROL) VALUES (1, 'doctor', 'doctor123')");

# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (1, 'Saidov Sardor Malik o''g''li', '1234')");
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (2,'Rahimov Farrux Javlon o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (3,'Xolmatova Laylo Rustam qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (4,'Tursunov Shaxzod Baxtiyor o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (5,'Abdullayeva Dilnoza Toshpo''lat qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (6,'Yusupov Bekzod Mansur o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (7,'Jumaboyev Komiljon Sobir o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (8,'Davlatova Nigora Orif qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (9,'Xudoyberdiyev Shuhrat Aziz o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (10,'Shirinova Shohista Ali qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (11,'Karimov Otabek Sanjar o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (12,'Ibragimova Sevinch Shavkat qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (13,'Omonov Dilshod Orifjon o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (14,'Xaydarov Ulug''bek Bekmurod o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (15,'Nazarova Madina Anvar qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (16,'Sobirov Azizbek Ilhom o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (17,'Qodirova Mehriniso Toxir qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (18,'Bozorov Kamol Sherali o''g''li', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (19,'Eshmatova Muqaddas Akrom qizi', '1234')")
# conn.execute("INSERT INTO USERS (ID,FISH,PAROL) VALUES (20,'Rahmonov Sarvar Abdulla o''g''li', '1234')")

# # O'zgarishlarni saqlash  
# conn.commit()  

cursor = conn.execute("SELECT * from DOCTORS")
for row in cursor:
   print("ID = ", row[0])
   print("LOGIN= ", row[1])
   print("parol = ", row[2], "\n")

conn.close()