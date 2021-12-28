add_user = "INSERT INTO users (user_id, username) VALUES (?, ?)"
add_place = "INSERT INTO places (user_id, place_name, rating) " \
            "VALUES ((SELECT users.id FROM users WHERE users.user_id = (?)), ?, ?)"
