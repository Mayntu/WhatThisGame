from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Boolean
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
    current_players = Column(name="current_players", type_=Integer)
    game_status = Column(name="game_status", type_=String)

    def __init__(self, name : str, root : int, max_players : int, current_players : int = 1, game_status : str = "waiting") -> None:
        self.code = GameLobby.generate_game_code()
        self.name = name
        self.root = root
        self.max_players = max_players
        self.current_players = current_players
        self.game_status = game_status

    
    @staticmethod
    def generate_game_code() -> str:
        from string import ascii_uppercase
        NUMS : str = "123456789" + ascii_uppercase
        from random import randint

        result : str = "".join([NUMS[randint(0, len(NUMS) - 1)] for x in range(0, 6)])
        return result
            


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

SessionDB = sessionmaker(bind=engine)
session_db = SessionDB()