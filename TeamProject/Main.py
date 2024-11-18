
import config as cfg
import mysql.connector
from mysql.connector import errorcode

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

def setup_db_connection(user, password, host, database):
    try:
        return mysql.connector.connect(user=user, password=password, host=host, database=database)

    except mysql.connector as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not")
        else:
            print("Something is wrong with your user name or")

def get_degrees(conn):
    cursor = conn.cursor(dictionary=True)

    stmt = """
    SELECT
        name,
        level
    FROM degree    
    """

    cursor.execute(stmt)
    rows = cursor.fetchall()

    return rows



db_conn = setup_db_connection(cfg.mysql["user"], cfg.mysql["password"], cfg.mysql["host"], cfg.mysql["db"])

#print("welcome to " + db_conn.get_server_info())



columns = [
    {'field': 'name', 'editable': True, 'sortable': True},
    {'field': 'level', 'editable': True},
]
rows = get_degrees(db_conn)


@ui.page('/')
def page():
    def add_row():
        new_id = max((dx['id'] for dx in rows), default=-1) + 1
        rows.append({'id': new_id, 'name': 'New name', 'age': None})
        ui.notify(f'Added row with ID {new_id}')
        aggrid.update()

    def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]

    async def delete_selected():
        selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
        rows[:] = [row for row in rows if row['id'] not in selected_id]
        ui.notify(f'Deleted row with ID {selected_id}')
        aggrid.update()

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    ui.button('Delete selected', on_click=delete_selected)
    ui.button('New row', on_click=add_row)


ui.run()


db_conn.close()