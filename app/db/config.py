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
            surname        TEXT NOT NULL,
            is_admin        INTEGER NOT NULL
        )
    """

    SEED_DATA = """
        INSERT INTO users (username, password_hash, forename, surname, is_admin)
        VALUES ("admin","scrypt:32768:8:1$Bqx7M9OF67CbYB4d$a6c1a9d7837c934bcd26ab17b3898580eb4f42a1a30f4de50a288ef88a107b48b739579cce9dfe97c94a922378772a6cf53de828cf2e808b62e8618401eb9c7b", "Super", "Admin", 1), 
               ("erinrune","scrypt:32768:8:1$Bqx7M9OF67CbYB4d$a6c1a9d7837c934bcd26ab17b3898580eb4f42a1a30f4de50a288ef88a107b48b739579cce9dfe97c94a922378772a6cf53de828cf2e808b62e8618401eb9c7b", "Erin", "Rune", 0),
               ("abrain","scrypt:32768:8:1$Bqx7M9OF67CbYB4d$a6c1a9d7837c934bcd26ab17b3898580eb4f42a1a30f4de50a288ef88a107b48b739579cce9dfe97c94a922378772a6cf53de828cf2e808b62e8618401eb9c7b", "Arthur", "Brain", 0)
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
        VALUES ("Hello, World", "The new site does indeed work!", "admin"),
                ("Industrial Washing Machines", "Screw these new smart front loaders that break after 2 years. Get a proper one that you can even turn into a go cart.", "erinrune"),
                ("CANIPOST", "HELP ME I AM A MESSAGE", "abrain")
    """
class RepliesTable:

    NAME = "replies"

    SCHEMA = """
        CREATE TABLE replies (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id  INTEGER NOT NULL,
            is_active  BOOLEAN NOT NULL CHECK (is_active IN (0,1)) DEFAULT 1,
            body        TEXT NOT NULL,
            posted_by   TEXT NOT NULL,

            FOREIGN KEY (posted_by) REFERENCES users(id),
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )

    """

    SEED_DATA = """
        INSERT INTO replies (message_id, body, posted_by)
        VALUES (3,"Woah that sucks", "erinrune")
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
    RepliesTable,
    # Add more tables here...
]

