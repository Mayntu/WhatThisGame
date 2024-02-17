from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
)
# from services.database.database import (
#     DATABASE as db
# )
import json
from services.database.countries import (
    Country,
    to_country,
    to_countries
)
from services.database.models import (
    User,
    GameLobby,
    session_db
)


app : Flask = Flask(__name__)
app.secret_key = "akgmwagwawagagwagagklmga"


@app.route("/", methods=["GET", "POST"])
def main() -> str:
    if session.get("auth"):
        return render_template("home.html")
    return redirect("/authorization")


@app.route("/authorization", methods=["GET", "POST"])
def auth_view() -> str:
    if session.get("auth"):
        return redirect("/")
    return render_template("authorization.html")


@app.route("/registration", methods=["GET", "POST"])
def reg_view() -> str:
    return render_template("registration.html")


@app.route("/deauth", methods=["GET"])
def api_death():
    session.clear()
    return json.dumps({"status" : "cleared"})


@app.route("/createGame", methods=["GET"])
def create_game():
    if session.get("auth"):
        if session.get("current_game_id"):
            return redirect("/currentGame")
        return render_template("createGame.html")
    
    return redirect("/authorization")


@app.route("/joinGame", methods=["GET"])
def join_game():
    if session.get("auth"):
        if session.get("current_game_id"):
            return redirect("/currentGame")
        
        return render_template("joinGame.html")
    
    return redirect("/authorization")


@app.route("/currentGame", methods=["GET"])
def current_game():
    if session.get("current_game_id"):
        print(GameLobby.generate_game_code())
        current_game = session_db.query(GameLobby).get(int(session.get("current_game_id")))
        context : dict = {}
        context["game"] = current_game.__dict__
        print(context["game"])
        return render_template("current_game.html", context=context)
    
    return redirect("/createGame")


@app.route("/api/v1/authorization", methods=["POST"])
def api_authorization():
    data = request.form
    login = data.get("login")
    password = data.get("password")

    users = session_db.query(User).filter(User.login == login).filter(User.password == password).all()
    if len(users) > 0:
        user = users[0]
        session["auth"] = True
        session["user_id"] = user.pk
        print(user.pk)
        return redirect("/")
    
    return "not valid data"


@app.route("/api/v1/registration", methods=["POST"])
def api_registration():
    data = request.form
    login = data.get("login")
    password = data.get("password")

    user = session_db.query(User).filter_by(login=login)
    if user.count() > 0:
        return redirect("/authorization")
    
    user : User = User(login=login, password=password)
    session_db.add(user)
    session_db.commit()

    session["auth"] = True
    session["user_id"] = user.pk
    return redirect("/")


@app.route("/api/v1/createGame", methods=["GET", "POST"])
def api_create_game():
    if session.get("auth"):
        data = request.form
        game_name : str = data.get("game_name")
        max_players = data.get("game_players_amount")
        root_id : int = session.get("user_id")
        game_lobby=GameLobby(game_name,root_id,max_players)
        session_db.add(game_lobby)
        session_db.commit()
        session["current_game_id"] = game_lobby.pk
        return redirect("/currentGame")
    
    return redirect("/authorization")


@app.route("/api/v1/joinGame", methods=["GET", "POST"])
def api_join_game():
    data = request.form
    code : str = data.get("game_code")
    lobbies = session_db.query(GameLobby).filter_by(code=code)
    if lobbies.count() > 0:
        lobby = lobbies[0]
        lobby.current_players += 1
        session_db.commit()
        session["current_game_id"] = lobby.pk
        return redirect("/currentGame")
    
    return json.dumps({"status" : "not valid code"})
app.run(
    host="0.0.0.0",
    port="5555",
    debug=True
)



# db.execute(query = "INSERT INTO countries (name, money, nuclear_count, shield_count) VALUES ('USA', 100, 0, 1)")
# db.execute(query = "INSERT INTO countries (name, money, nuclear_count, shield_count) VALUES ('RUSSIA', 100, 0, 1)")
# print(db.execute("SELECT * FROM countries"))

# @to_country
# def get_country(name : str) -> Country:
#     return db.execute("SELECT * FROM countries WHERE name='{}'".format(name))


# print(get_country(name = "USA"))


# @to_countries
# def get_countries() -> list[Country]:
#     print(db.execute("SELECT * FROM countries"))
#     return db.execute("SELECT * FROM countries")


# print(get_countries())