Prerequisites steps, you may have to perform some or all the first five steps.

1. Exceute these command  one after the other (May / May not be required) - 
	1.a. pip install pysqlite3
	1.b. pip install selenium
2. Download geckoDriver. (I have also attached geckoDriver(zip) where you can use this driver after unzipping OR This can be downloaded by following the steps described in - https://www.guru99.com/gecko-marionette-driver-selenium.html). Make a note of the geckoDriver location (after unzip) and you have to use the same location in the code, "For instance, os.chdir(r'C:\Users\user\Documents\geckoDriver')"
3. Download SQLite, follow steps from https://www.sqlitetutorial.net/download-install-sqlite/
4. Download and Install DBeaver (Community Version), from https://dbeaver.io/download/
5. Create a New Database in SQLite using DBeaver or existing database can be used. I created a new database, follow the below steps for creating a new database.
	5.a. On the left, there is a Database Navigator. Below to that, there will be a default database.
	5.b. Right click on the default database (which in my case is "DBeaver Sample Database (SQLite)").
	5.c. Right Click -> Create -> Connection -> Select SQLite -> Next.
	5.d. Provide a path where you want to create a new database, store this location because this will be used in code (I gave the same location where I have my code which is "E:\xyz\xyzdatabase.db", xyzdatabase.db is the database name, it should end with ".db").
	5.e. Then, click Finish. A new database will be created at the specified location.

6. Open "OdiDataProcessing.ipynb or OdiDataProcessing.py", then modify the following paths accordingly:
	6.a. By default, in a Windows OS any download will go to "Downloads", so the ZipFile will be downloaded at "C:\\Users\\user\\Downloads\\odis_json.zip" (Or else please modify according to the OS).
	6.b. JSONS are downloaded and unzipped in this folder but you may change it, to your convience - "C:\\Users\\user\\Downloads\\odis_json".
	6.c. Use the same above unzipped location in "folder_path" variable - which is "folder_path = 'C:\\Users\\user\\Downloads\\odis_json'".
	6.d. Modify the database location to the location which you have saved in Step.4 "For instance, conn = sqlite3.connect('E:\xyz\xyzdatabase.db')".

7. The python code is now ready to execute.
8. You can either run using jupyter (anaconda) or cmd (command prompt). If using cmd, go to the file location then use "py OdiDataProcessing.py" or "python OdiDataProcessing.py" to execute the python file. If jupyter is used, you can direclty open OdiDataProcessing.ipynb file and run each cell.
9. Tables will be created and data will be loaded into those tables in the database which is created in Step.4.
10. Open sql files "Query1.sql" (1 through 3), execute them in DBeaver which is a GUI, where you can see the query results of each query.

