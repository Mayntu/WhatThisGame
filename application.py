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
# from services.database.countries import (
#     Country,
#     to_country,
#     to_countries
# )
from services.database.models import (
    User,
    GameLobby,
    TeamPreset,
    CityPreset,
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
        context["is_root"] = False
        context["team_presets"] = session_db.query(TeamPreset).all()[0:current_game.teams_count]
        print(context["team_presets"])
        if session.get("user_id") == current_game.root:
            context["is_root"] = True
        
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

        teams_count : str = data.get("teams_count")
        teams_count : int = int(teams_count)

        players_in_team : str = data.get("players_in_team_count")
        players_in_team : int = int(players_in_team)

        max_players : int = teams_count

        root_id : int = int(session.get("user_id"))

        game_lobby = GameLobby(
            name=game_name,
            root=root_id,
            max_players=max_players,
            teams_count=teams_count,
            players_in_team=players_in_team
        )
        session_db.add(game_lobby)
        session_db.commit()
        
        user : User = session_db.query(User).get(root_id)
        user.game_id = game_lobby.pk
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
        if lobby.game_status == "waiting":
            lobby.current_players += 1
            session_db.commit()

            user_id : int = int(session.get("user_id"))
            user : User = session_db.query(User).get(user_id)
            user.game_id = lobby.pk
            session_db.commit()

            session["current_game_id"] = lobby.pk
            return redirect("/currentGame")
        
        return json.dumps({"status" : "game is started"})
    
    return json.dumps({"status" : "not valid code"})


@app.route("/api/v1/startGame", methods=["GET"])
def api_start_game():
    data = request.form
    lobby_id : str = session.get("current_game_id")
    lobby_id : int = int(lobby_id)
    lobby = session_db.query(GameLobby).get(lobby_id)
    if lobby.root == session.get("user_id"):
        lobby.game_status = "active"
        session_db.commit()


@app.route("/api/v1/chooseTeam", methods=["GET"])
def api_choose_team():
    data = request.form
    team_preset_id = data.get("team_preset_id")


app.run(
    host="0.0.0.0",
    port="5000",
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