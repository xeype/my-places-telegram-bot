add_user = "INSERT INTO users (user_id, username) VALUES (?, ?)"
add_place = "INSERT INTO places (user_id, place_name, rating, place_desc) " \
            "VALUES ((SELECT users.id FROM users WHERE users.user_id = (?)), ?, ?, ?)"
get_places = f"SELECT place_name, rating, place_desc FROM places " \
             "WHERE user_id = (SELECT users.id FROM users WHERE users.user_id = {})  ORDER BY rating DESC"
