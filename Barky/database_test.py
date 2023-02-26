# the database module is much more testable and has largely atomic actions
# this database module can be refactored to achieve decoupling
# implementing the Unit of Work or changing to sqlalchemy would achieve that


import os
from datetime import datetime
import sqlite3

import pytest

from database import DatabaseManager


@pytest.fixture
def database_manager() -> DatabaseManager:
    """
    definition of a fixture at https://docs.pytest.org/en/stable/fixture.html#what-fixtures-are
    """
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    # yield defined at https://www.guru99.com/python-yield-return-generator.html
    yield dbm
    dbm.__del__()  # explicitly releases the database manager
    os.remove(filename)


def test_database_manager_create_table(database_manager):
    # arrange and act
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()

    cursor.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name='bookmarks' ''')

    assert cursor.fetchone()[0] == 1

    # cleanup
    # this is most likely not needed
    database_manager.drop_table("bookmarks")


def test_database_manager_add_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()
    }

    # act
    database_manager.add("bookmarks", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')
    assert cursor.fetchone()[0] == 1
