from services.database.database import (
    DATABASE as db
)
from services.database.countries import (
    Country,
    to_country,
    to_countries
)
db.execute(query = "INSERT INTO countries (name, money, nuclear_count, shield_count) VALUES ('USA', 100, 0, 1)")
db.execute(query = "INSERT INTO countries (name, money, nuclear_count, shield_count) VALUES ('RUSSIA', 100, 0, 1)")
print(db.execute("SELECT * FROM countries"))

@to_country
def get_country(name : str) -> Country:
    return db.execute("SELECT * FROM countries WHERE name='{}'".format(name))


print(get_country(name = "USA"))


@to_countries
def get_countries() -> list[Country]:
    print(db.execute("SELECT * FROM countries"))
    return db.execute("SELECT * FROM countries")


print(get_countries())