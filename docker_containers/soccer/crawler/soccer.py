from pyfutebol import search
from datetime import datetime
from opendata import pgbind

def get_matches(teams):
    match_list = []

    for team in teams.keys():
        matches = search.buscar_jogo_por_time(team)
        for match in matches:
            match_list.append(match)

    return match_list

def filter_championship(matches, championship):
    championship_matches = []

    for match in matches:
        if match["league"] == championship:
            championship_matches.append(match)
    
    return championship_matches

def has_game(teams, championship_matches):
    for team in teams.keys():
        for match in championship_matches:
            if team in match["match"].lower():
                teams[team] = True
    
    return teams

def get_features(data):
    timestamp = datetime.now()
    features = {}
    features["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    for key, value in data.items():
        if key == "são paulo":
            features["sao_paulo"] = value
        else:
            features[key] = value
    
    return features

if __name__ == '__main__':
    teams = {
        "são paulo": False,
        "corinthians": False,
        "palmeiras": False,
        "santos": False
    }

    matches = get_matches(teams)
    # print(matches)
    brasileiro = filter_championship(matches, "Campeonato Brasileiro")
    # print(brasileiro)
    teams = has_game(teams, brasileiro)
    # print(teams)

    features = get_features(teams)
    print(features)
    
    # sql = pgbind.build_sql_query(features, "soccer")
    # print(sql)

    # pgbind.insert_into_db(features, "soccer")