
from queryexplorer import connect_db
from queryutils.splunktypes import implemented_commands

names = [c.name for c in implemented_commands]
types = [c.typestr for c in implemented_commands]
cmd_lookup = dict(zip(names, types))

def main():
    db = connect_db()
    select_cursor = db.cursor()
    select_cursor.execute("SELECT command, id FROM commands")
    for (command, id) in select_cursor.fetchall():
        category = lookup_category(command) 
        print "Put command", command, "in category", category 
        update_cursor = db.cursor()
        update_cursor.execute("UPDATE commands SET category=? WHERE id=?", [category, id])
        db.commit()
    db.close()

def lookup_category(command):
    parts = command.split('(')
    main_command = parts[0].lower()
    category = "!!!"
    if main_command == "addtotals": # special case because parameter changes category
        if command.find('COL') > -1:
            category = cmd_lookup["addtotals col"]
        else:
            category = cmd_lookup["addtotals row"]
    else:
        try:
            category = cmd_lookup[main_command]
        except:
            print "Missing category for command: ", parts[0]
    return category


main()
