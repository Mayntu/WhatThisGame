from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    String,
    Integer,
    FLOAT,
    CHAR,
    Boolean,
    ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BaseModel(Base):
    __tablename__ = "people"

    pk = Column(name="pk", type_=Integer, autoincrement=True, primary_key=True)
    title = Column(name="title", type_=String)
    description = Column(name="description", type_=String)
    amount = Column(name="amount", type_=Integer)

    def __init__(self, title : str, description : str, amount : int) -> None:
        self.title = title
        self.description = description
        self.amount = amount


class User(Base):
    __tablename__ = "users"

    pk = Column(name="pk", type_=Integer, autoincrement=True, primary_key=True)
    login = Column(name="login", type_=String)
    password = Column(name="password", type_=String)
    is_admin = Column(name="is_admin", type_=Boolean, default=False)
    game_id = Column("game_id", ForeignKey("gamelobbies.pk"), default=None)
    team = Column(name="team", type_=String, default=None)

    def __init__(self, login : str, password : str, is_admin : bool = False):
        self.login = login
        self.password = password
        self.is_admin = is_admin


class GameLobby(Base):
    __tablename__ = "gamelobbies"

    pk = Column(name="pk", type_=Integer, autoincrement=True, primary_key=True)
    code = Column(name="code", type_=String)
    name = Column(name="name", type_=String)
    root = Column("root", ForeignKey("users.pk"))
    max_players = Column(name="max_players", type_=Integer)
    teams_count = Column(name="teams_count", type_=Integer)
    players_in_team = Column(name="players_in_team", type_=Integer)
    current_players = Column(name="current_players", type_=Integer)
    game_status = Column(name="game_status", type_=String)

    def __init__(self, 
                name : str, root : int, max_players : int,
                teams_count : int,
                players_in_team : int,
                current_players : int = 1, 
                game_status : str = "waiting"
        ) -> None:
        
        self.code = GameLobby.generate_game_code()
        self.name = name
        self.root = root
        self.max_players = max_players
        self.teams_count = teams_count
        self.players_in_team = players_in_team
        self.current_players = current_players
        self.game_status = game_status

    
    @staticmethod
    def generate_game_code() -> str:
        from string import ascii_uppercase
        NUMS : str = "123456789" + ascii_uppercase
        from random import randint

        result : str = "".join([NUMS[randint(0, len(NUMS) - 1)] for x in range(0, 6)])
        return result
            

class TeamPreset(Base):
    __tablename__ = "teamspresets"

    pk = Column(name="pk", type_=Integer, autoincrement=True, primary_key=True)
    name = Column(name="name", type_=String)
    flag = Column(name="flag", type_=String)


class CityPreset(Base):
    __tablename__ = "citiespresets"

    pk = Column(name="pk", type_=Integer, autoincrement=True, primary_key=True)
    team = Column("team", ForeignKey("teamspresets.pk"))
    name = Column(name="name", type_=String)
    default_income = Column(name="default_income", type_=FLOAT)
    default_level_of_living = Column(name="default_level_of_living", type_=FLOAT)
    default_is_shield = Column(name="default_is_shield", type_=Boolean, default=False)


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

SessionDB = sessionmaker(bind=engine)
session_db = SessionDB()