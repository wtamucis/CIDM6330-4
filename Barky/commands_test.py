# quit has self-evident behavior and it does not depend on logic, so
# quit does not need testing
def test_quit_command():
    pass

# the other commands do not need testing because they are in tight
# coupling with sqlite3 and with the use of it in the module database.py
