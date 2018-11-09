import datetime


tables = ['Users', 'Projects', 'Projects_Roster', 'Roles', 'Positions', 'Departments',
          'Objectives', 'Objectives_Roster', 'Object_Types', 'Object_Types_Roster',
          'Awards', 'Awards_Roster', 'Courses', 'Courses_Roster']


class SQLite:
    def __init__(self):
        self.primary_key = 'integer PRIMARY KEY autoincrement'
        self.connection_string = 'Database/Level_UP.db'
        self.connection = None

    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect(self.connection_string)
        return self.connection


def register_database():
    _base = SQLite()
    return _base


def table_creation(_base, _connection):
    def users(_cursor, _primary_key):
        create_table = f'''
        create table {tables[0]}(
        idx {_primary_key},
        name text,
        last_name text,
        start_date date,
        level int not null,
        position_fk int not null,
        foreign key(position_fk) references {tables[4]}(idx))
        '''
        _cursor.execute(create_table)

    def projects(_cursor, _primary_key):
        create_table = f'''
        create table {tables[1]}(
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
        create table {tables[2]}(
        user_fk int not null,
        project_fk int not null,
        foreign key (user_fk) references {tables[0]}(idx),
        foreign key (project_fk) references {tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def roles(_cursor):
        create_table = f'''
        create table {tables[3]}(
        name text,
        user_fk int not null,
        project_fk int not null,
        foreign key (user_fk) references {tables[0]}(idx),
        foreign key (project_fk) references {tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def positions(_cursor, _primary_key):
        create_table = f'''
        create table {tables[4]}(
        idx {_primary_key},
        name text,
        details text,
        department_fk int not null,
        foreign key (department_fk) references {tables[5]}(idx))
        '''
        _cursor.execute(create_table)

    def departments(_cursor, _primary_key):
        create_table = f'''
        create table {tables[5]}(
        idx {_primary_key},
        name text,
        details text)
        '''
        _cursor.execute(create_table)

    def objectives(_cursor, _primary_key):
        create_table = f'''
        create table {tables[6]}(
        idx {_primary_key},
        name text,
        detail text,
        quantity_needed int not null)
        '''
        _cursor.execute(create_table)

    def objectives_roster(_cursor):
        create_table = f'''
        create table {tables[7]}(
        position_fk int not null,
        objective_fk int not null,
        foreign key (position_fk) references {tables[4]}(idx),
        foreign key (objective_fk) references {tables[6]}(idx))
        '''
        _cursor.execute(create_table)

    def object_types(_cursor, _primary_key):
        create_table = f'''
        create table {tables[8]}(
        idx {_primary_key},
        object int not null)
        '''
        _cursor.execute(create_table)

    def object_types_roster(_cursor):
        create_table = f'''
        create table {tables[9]}(
        objective_fk int not null,
        object_type_fk int not null,
        foreign key (objective_fk) references {tables[6]}(idx),
        foreign key (object_type_fk) references {tables[8]}(idx))
        '''
        _cursor.execute(create_table)

    def awards(_cursor, _primary_key):
        create_table = f'''
        create table {tables[10]}(
        idx {_primary_key},
        name text,
        details text,
        date_given date,
        project_fk int not null,
        foreign key (project_fk) references {tables[1]}(idx))
        '''
        _cursor.execute(create_table)

    def awards_roster(_cursor):
        create_table = f'''
        create table {tables[11]}(
        user_fk int not null,
        award_fk int not null,
        foreign key (user_fk) references {tables[0]}(idx),
        foreign key (award_fk) references {tables[10]}(idx))
        '''
        _cursor.execute(create_table)

    def courses(_cursor, _primary_key):
        create_table = f'''
        create table {tables[12]}(
        idx {_primary_key},
        name text,
        details text,
        start_date date,
        end_date date)
        '''
        _cursor.execute(create_table)

    def courses_roster(_cursor):
        create_table = f'''
        create table {tables[13]}(
        user_fk int not null,
        course_fk int not null,
        foreign key (user_fk) references {tables[0]}(idx),
        foreign key (course_fk) references {tables[12]}(idx))
        '''
        _cursor.execute(create_table)

    def table_delete(_cursor):
        for table in tables:
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
        insert into {tables[0]} (name, last_name, start_date, level, position_fk) values ('%s', '%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_users % ('Janusz', 'Kowalski', datetime.datetime.today().strftime('%d-%m-%Y'), 1, 1))
        _cursor.execute(tmp_users % ('Anna', 'Wesołowska', datetime.datetime.today().strftime('%d-%m-%Y'), 1, 1))
        _connection.commit()

    def projects(_cursor, _connection):
        tmp_projects = f'''
        insert into {tables[1]} (name, start_date, deadline, details, client) values ('%s', '%s', '%s', '%s', '%s')
        '''
        _cursor.execute(tmp_projects % ('Testowy 1', datetime.datetime.today().strftime('%d-%m-%Y'), '12-12-2020',
                                        'Szczegóły projektu', 'Klient 1'))
        _connection.commit()

    def projects_roster(_cursor, _connection):
        tmp_projects_roster = f'''
        insert into {tables[2]} (user_fk, project_fk) values ('%s', '%s')
        '''
        _cursor.execute(tmp_projects_roster % (1, 1))
        _cursor.execute(tmp_projects_roster % (2, 1))
        _connection.commit()

    def roles(_cursor, _connection):
        tmp_roles = f'''
        insert into {tables[3]} (name, user_fk, project_fk) values ('%s', '%s', '%s')
        '''
        _cursor.execute(tmp_roles % ('Programista', 1, 1))
        _cursor.execute(tmp_roles % ('Menedżer', 2, 1))
        _connection.commit()

    def positions(_cursor, _connection):
        tmp_positions = f'''
        insert into {tables[4]} (name, details, department_fk) values ('%s', '%s', '%s')
        '''
        _cursor.execute(tmp_positions % ('Stanowisko 1', 'Szczegóły stanowiska 1', 1))
        _connection.commit()

    _cursor = _connection.cursor()
    users(_cursor, _connection)
    projects(_cursor, _connection)
    projects_roster(_cursor, _connection)
    roles(_cursor, _connection)
    positions(_cursor, _connection)


def print_table(_connection, _name):
    _sql = f'select * from {_name}'
    _cursor = _connection.cursor()
    _cursor.execute(_sql)
    results = _cursor.fetchall()
    return results


def demo(_base):
    _connection = _base.connect()

    print('\nCreating tables...')
    table_creation(_base, _connection)
    print('Finished!\n')

    print('Creating demo data...')
    create_records(_connection)
    print('Finished!\n')

    print('-' * 190)

    print('Printing database records:')
    for _table in tables:
        print('\tTable content: ', _table, end=' - ')
        print(print_table(_connection, _table))

    print('-' * 190)

    _connection.close()


if __name__ == '__main__':
    base = register_database()
    demo(base)
