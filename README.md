Maktab 89(Python) Group 5 FastAPI weblog project

1. clone the repository
2. cd into weblog folder
3. use this command to activate the virtual environment: "source venv/bin/activate"
4. now run the app with this command: "uvicorn main:app --reload"
5. open 127.0.0.1:8000 on your browser

IF IT DOESNT RUN: (use sqlite instead of postgres)
1. go to this directory: /weblog/app/router/DataBase
2. open my_database.py
3. comment line 5 (postgresURL)
4. uncomment line 6 (sqliteURL)
