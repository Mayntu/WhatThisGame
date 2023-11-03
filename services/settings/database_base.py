DB_NAME : str = "game.db"

TABLES : dict = {
    "countries" : {
        "id" : "INTEGER PRIMARY KEY AUTOINCREMENT,",
        "name" : "VARCHAR(16) NOT NULL,",
        "money" : "INTEGER NOT NULL,",
        "nuclear_count" : "INTEGER NOT NULL,",
        "shield_count" : "INTEGER NOT NULL",
    },
    "cities" : {
        "country_id" : "INTEGER NOT NULL,",
        "city" : "VARCHAR(16) NOT NULL,",
        "money_produce" : "INTEGER NOT NULL,",
        "live_level" : "INTEGER NOT NULL,",
        "have_shield" : "INTEGER NOT NULL",
    },
    "world" : {
        "ecology_level" : "INTEGER NOT NULL",
    }
}