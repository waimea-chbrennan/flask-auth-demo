#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UsersTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            username      TEXT PRIMARY KEY,
            password_hash    TEXT NOT NULL,
            forename        TEXT NOT NULL,
            surname        TEXT NOT NULL
        )
    """

    SEED_DATA = """
        INSERT INTO users (username, password_hash, forename, surname)
        VALUES ("admin","scrypt:32768:8:1$Bqx7M9OF67CbYB4d$a6c1a9d7837c934bcd26ab17b3898580eb4f42a1a30f4de50a288ef88a107b48b739579cce9dfe97c94a922378772a6cf53de828cf2e808b62e8618401eb9c7b", "Super", "Admin")
    
    """

# Add more table classes here...

class MessagesTable:
    
    NAME = "messages"

    SCHEMA = """
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            posted_by TEXT NOT NULL,

            FOREIGN KEY (posted_by) REFERENCES users(id)
        )

    """

    SEED_DATA = """
    INSERT INTO messages (title, body, posted_by)
    VALUES ("Hello, World", "The new site does indeed work!", "admin")

    
    """


#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UsersTable,
    MessagesTable,
    # Add more tables here...
]

