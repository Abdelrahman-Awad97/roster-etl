import os
import sqlite3
import json
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# connect to the db
with sqlite3.connect('rosterdb.sqlite3') as conn:
    cur = conn.cursor()

    cur.executescript(
        '''
        DROP TABLE IF EXISTS Users;
        DROP TABLE IF EXISTS Courses;
        DROP TABLE IF EXISTS Members;

        CREATE TABLE Users(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
        name TEXT UNIQUE
        );
        
        CREATE TABLE Courses(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
        title TEXT UNIQUE);
        
        CREATE TABLE Members(
        user_id INTEGER,
        course_id INTEGER,
        role INTEGER,
        PRIMARY KEY(user_id, course_id, role)
        );
        '''
    )

    # file_name = input('Enter the file name: ').strip()
    # if len(file_name) < 1:
    #     f_name = 'roster_data.json'

    # while found == False:
    #     f_name = input('Enter the file here: ').strip()
    #     if f_name == 'roster_data.json':
    #         found = True
    #     else:
    #         print('wrong file name')

    found = False
    while not found:
        f_name = input('Enter file name here: ').strip()
        if os.path.exists(f_name):
           found = True
        else:
           print('file is not exist') 
        
        
    with open(f'{f_name}', 'r', encoding='UTF-8') as f:
        fetch_data_s = f.read()
        if not fetch_data_s:
            f.seek(0)
            raise ValueError(f'file {f_name} is empty')
        fetch_data_d = json.loads(fetch_data_s)

        for data in fetch_data_d:   
            if len(data) < 3:
                logging.error('[%s] is missing some data', data)
                continue
            # data extraction
            user_name = data[0]
            course_title = data[1]
            try:
                role = int(data[2])
            except ValueError:
                logging.error('conversion failed at data: %s', data)
                continue

            # load to database
            cur.execute('INSERT OR IGNORE INTO Users (name) VALUES (?)', (user_name,))
            user_id = cur.execute('SELECT id FROM Users WHERE name = ?', (user_name,)).fetchone()[0]
            # print(user_id)

            cur.execute('INSERT OR IGNORE INTO Courses (title) VALUES (?)', (course_title,))
            course_id = cur.execute('SELECT id FROM Courses WHERE title = ?', (course_title,)).fetchone()[0]
            # print(course_id)

            cur.execute(
                '''
                INSERT INTO Members (user_id, course_id, role) VALUES (?, ?, ?)
                ON CONFLICT (user_id, course_id, role)
                DO UPDATE SET role = excluded.role
                ''', (user_id, course_id, role)
            )

        join = cur.execute(
            '''
            SELECT Users.name, Courses.title, Members.role
            FROM Users JOIN Courses JOIN Members
            ON Users.id = Members.user_id AND Courses.id = Members.course_id
            ORDER BY Users.name DESC, Courses.title DESC, Members.role DESC LIMIT 2
            '''
        ).fetchall()

        for j in join:
            print(j)