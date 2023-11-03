from typing import NamedTuple

class Country(NamedTuple):
    id : int
    name : str
    money : int
    nuclear_count : int
    shield_count : int


def to_country(func) -> Country:
    def wrapper(*args, **kwargs) -> Country:
        country_list : list = func(*args, **kwargs)
        if len(country_list) == 0:
            return []
        country_list = country_list[0]
        return Country(
            id = country_list[0],
            name = country_list[1],
            money = country_list[2],
            nuclear_count = country_list[3],
            shield_count = country_list[4],
        )
    return wrapper


def to_countries(func) -> list[Country]:
    def wrapper(*args, **kwargs) -> list[Country]:
        country_list : list = func(*args, **kwargs)
        if len(country_list) == 0:
            return []
        countries : list[Country] = []
        for country in country_list:
            countries.append(Country(
                id = country[0],
                name = country[1],
                money = country[2],
                nuclear_count = country[3],
                shield_count = country[4],
                ))
        return countries
    return wrapper