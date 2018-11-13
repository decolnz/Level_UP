import sqlite3
import datetime
import random

__tables = ['Users', 'Projects', 'Projects_Roster', 'Roles', 'Positions', 'Departments',
            'Objectives', 'Objectives_Roster', 'Object_Types', 'Object_Types_Roster',
            'Awards', 'Awards_Roster', 'Courses', 'Courses_Roster']

__logged_users = {}


class SQLite:
    def __init__(self):
        self.primary_key = 'integer PRIMARY KEY autoincrement'
        self.connection_string = 'Database/Level_UP.db'
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.connection_string)
        return self.connection


def register_database():
    _base = SQLite()
    return _base


def table_creation(_base, _connection):
    def users(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[0]}(
        idx {_primary_key},
        name text,
        last_name text,
        start_date date,
        level int not null,
        username text,
        password text,
        position_fk int not null,
        foreign key(position_fk) references {__tables[4]}(idx))
        '''
        _cursor.execute(create_table)

    def projects(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[1]}(
        idx {_primary_key},
        name text,
        start_date date,
        deadline date,
        details text,
        client text)
        '''
        _cursor.execute(create_table)

    def projects_roster(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[2]}(
        user_fk int not null,
        project_fk int not null,
        foreign key (user_fk) references {__tables[0]}(idx),
        foreign key (project_fk) references {__tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def roles(_cursor):
        create_table = f'''
        create table {__tables[3]}(
        name text,
        user_fk int not null,
        project_fk int not null,
        foreign key (user_fk) references {__tables[0]}(idx),
        foreign key (project_fk) references {__tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def positions(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[4]}(
        idx {_primary_key},
        name text,
        details text,
        department_fk int not null,
        foreign key (department_fk) references {__tables[5]}(idx))
        '''
        _cursor.execute(create_table)

    def departments(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[5]}(
        idx {_primary_key},
        name text,
        details text)
        '''
        _cursor.execute(create_table)

    def objectives(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[6]}(
        idx {_primary_key},
        name text,
        details text,
        done int not null,
        quantity_needed int not null)
        '''
        _cursor.execute(create_table)

    def objectives_roster(_cursor):
        create_table = f'''
        create table {__tables[7]}(
        position_fk int not null,
        objective_fk int not null,
        foreign key (position_fk) references {__tables[4]}(idx),
        foreign key (objective_fk) references {__tables[6]}(idx))
        '''
        _cursor.execute(create_table)

    def object_types(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[8]}(
        idx {_primary_key},
        object_type text)
        '''
        _cursor.execute(create_table)

    def object_types_roster(_cursor):
        create_table = f'''
        create table {__tables[9]}(
        objective_fk int not null,
        object_type_fk int not null,
        foreign key (objective_fk) references {__tables[6]}(idx),
        foreign key (object_type_fk) references {__tables[8]}(idx))
        '''
        _cursor.execute(create_table)

    def awards(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[10]}(
        idx {_primary_key},
        name text,
        details text,
        date_given date,
        project_fk int not null,
        foreign key (project_fk) references {__tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def awards_roster(_cursor):
        create_table = f'''
        create table {__tables[11]}(
        user_fk int not null,
        award_fk int not null,
        foreign key (user_fk) references {__tables[0]}(idx),
        foreign key (award_fk) references {__tables[10]}(idx))
        '''
        _cursor.execute(create_table)

    def courses(_cursor, _primary_key):
        create_table = f'''
        create table {__tables[12]}(
        idx {_primary_key},
        name text,
        details text,
        start_date date,
        end_date date)
        '''
        _cursor.execute(create_table)

    def courses_roster(_cursor):
        create_table = f'''
        create table {__tables[13]}(
        user_fk int not null,
        course_fk int not null,
        foreign key (user_fk) references {__tables[0]}(idx),
        foreign key (course_fk) references {__tables[12]}(idx))
        '''
        _cursor.execute(create_table)

    def table_delete(_cursor):
        for table in __tables:
            _drop = f'DROP TABLE {table}'
            try:
                _cursor.execute(_drop)
            except Exception:
                pass
                # raise Exception('Error! Tables deletion failed!')

    _cursor = _connection.cursor()
    table_delete(_cursor)
    users(_cursor, _base.primary_key)
    projects(_cursor, _base.primary_key)
    projects_roster(_cursor, _base.primary_key)
    roles(_cursor)
    positions(_cursor, _base.primary_key)
    departments(_cursor, _base.primary_key)
    objectives(_cursor, _base.primary_key)
    objectives_roster(_cursor)
    object_types(_cursor, _base.primary_key)
    object_types_roster(_cursor)
    awards(_cursor, _base.primary_key)
    awards_roster(_cursor)
    courses(_cursor, _base.primary_key)
    courses_roster(_cursor)


def create_records(_connection):
    def users(_cursor, _connection):
        tmp_users = f'''
        insert into {__tables[0]} (name, last_name, start_date, level, username, password, position_fk) values
        ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_users % ('Janusz', 'Kowalski', datetime.datetime.today().strftime('%d-%m-%Y'), 1,
                                     'Jkowalski', 'jkowalski', 1))
        _cursor.execute(tmp_users % ('Anna', 'Wesołowska', datetime.datetime.today().strftime('%d-%m-%Y'), 1,
                                     'Awesolowska', 'awesolowska', 1))
        _connection.commit()

    def projects(_cursor, _connection):
        tmp_projects = f'''
        insert into {__tables[1]} (name, start_date, deadline, details, client) values ('%s', '%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_projects % ('Testowy 1', datetime.datetime.today().strftime('%d-%m-%Y'), '12-12-2020',
                                        'Szczegóły projektu', 'Klient 1'))
        _connection.commit()

    def projects_roster(_cursor, _connection):
        tmp_projects_roster = f'''
        insert into {__tables[2]} (user_fk, project_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_projects_roster % (1, 1))
        _cursor.execute(tmp_projects_roster % (2, 1))
        _connection.commit()

    def roles(_cursor, _connection):
        tmp_roles = f'''
        insert into {__tables[3]} (name, user_fk, project_fk) values ('%s', '%s', '%s')
        '''
        _cursor.execute(tmp_roles % ('Programista', 1, 1))
        _cursor.execute(tmp_roles % ('Menedżer', 2, 1))
        _connection.commit()

    def positions(_cursor, _connection):
        tmp_positions = f'''
        insert into {__tables[4]} (name, details, department_fk) values ('%s', '%s', '%s')
        '''
        _cursor.execute(tmp_positions % ('Stanowisko 1', 'Szczegóły stanowiska 1', 1))
        _connection.commit()

    def departments(_cursor, _connection):
        tmp_departments = f'''
        insert into {__tables[5]} (name, details) values ('%s', '%s')
        '''
        _cursor.execute(tmp_departments % ('Dział 1', 'Szczegóły działu 1'))
        _connection.commit()

    def objectives(_cursor, _connection):
        tmp_objectives = f'''
        insert into {__tables[6]} (name, details, done, quantity_needed) values ('%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_objectives % ('Zadanie 1', 'Szczegóły zadania 1', 0, 5))
        _connection.commit()

    def objectives_roster(_cursor, _connection):
        tmp_objectives_roster = f'''
        insert into {__tables[7]} (position_fk, objective_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_objectives_roster % (1, 1))
        _connection.commit()

    def object_types(_cursor, _connection):
        tmp_object_types = f'''
        insert into {__tables[8]} (object_type) values ('Years worked')
        '''
        _cursor.execute(tmp_object_types)
        _connection.commit()

    def object_types_roster(_cursor, _connection):
        tmp_object_types_roster = f'''
        insert into {__tables[9]} (objective_fk, object_type_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_object_types_roster % (1, 1))
        _connection.commit()

    def awards(_cursor, _connection):
        tmp_awards = f'''
        insert into {__tables[10]} (name, details, date_given, project_fk) values ('%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_awards % ('Wyróżnienie 1', 'Szczegóły wyróżnienia 1',
                                      datetime.datetime.today().strftime('%d-%m-%Y'), 1))
        _cursor.execute(tmp_awards % ('Wyróżnienie 3', 'Szczegóły wyróżnienia 2',
                                      datetime.datetime.today().strftime('%d-%m-%Y'), 1))
        _cursor.execute(tmp_awards % ('Wyróżnienie 3', 'Szczegóły wyróżnienia 3',
                                      datetime.datetime.today().strftime('%d-%m-%Y'), 1))
        _connection.commit()

    def awards_roster(_cursor, _connection):
        tmp_awards_roster = f'''
        insert into {__tables[11]} (user_fk, award_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_awards_roster % (1, 1))
        _cursor.execute(tmp_awards_roster % (1, 2))
        _cursor.execute(tmp_awards_roster % (2, 3))
        _connection.commit()

    def courses(_cursor, _connection):
        tmp_courses = f'''
        insert into {__tables[12]} (name, details, start_date, end_date) values ('%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_courses % ('Szkolenie 1', 'Szczegóły szkolenia 1',
                                       datetime.datetime.today().strftime('%d-%m-%Y'), '12-12-2018'))
        _cursor.execute(tmp_courses % ('Szkolenie 2', 'Szczegóły szkolenia 2',
                                       datetime.datetime.today().strftime('%d-%m-%Y'), '20-12-2018'))
        _connection.commit()

    def courses_roster(_cursor, _connection):
        tmp_courses_roster = f'''
        insert into {__tables[13]} (user_fk, course_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_courses_roster % (2, 1))
        _cursor.execute(tmp_courses_roster % (2, 2))
        _connection.commit()

    _cursor = _connection.cursor()
    users(_cursor, _connection)
    projects(_cursor, _connection)
    projects_roster(_cursor, _connection)
    roles(_cursor, _connection)
    positions(_cursor, _connection)
    departments(_cursor, _connection)
    objectives(_cursor, _connection)
    objectives_roster(_cursor, _connection)
    object_types(_cursor, _connection)
    object_types_roster(_cursor, _connection)
    awards(_cursor, _connection)
    awards_roster(_cursor, _connection)
    courses(_cursor, _connection)
    courses_roster(_cursor, _connection)


def print_table(_connection, _name):
    _sql = f'select * from {_name}'
    _cursor = _connection.cursor()
    _cursor.execute(_sql)
    results = _cursor.fetchall()
    return results


def login(_connection, username, password):
    _get_user = f'''select username
    from Users
    where username = '{username}' and
    password = '{password}'
    '''

    _cursor = _connection.cursor()
    try:
        _cursor.execute(_get_user)
    except sqlite3.Error as er:
        print('Error:', er)

    control_number = random.randint(1, 999)
    logged_user = {str(username): control_number}
    __logged_users.update(logged_user)

    return logged_user


def demo(_base):
    _connection = _base.connect()

    print('\nCreating tables...')
    table_creation(_base, _connection)
    print('Finished!\n')

    print('Creating demo data...')
    create_records(_connection)
    print('Finished!\n')

    print('-' * 150)

    print('Printing database records:')
    for _table in __tables:
        print('\tTable content: ', _table, end=' - ')
        print(print_table(_connection, _table))

    print('-' * 150)

    _connection.close()


if __name__ == '__main__':
    base = register_database()
    demo(base)
