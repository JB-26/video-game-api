class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"User ID: {self.id}"

def authenticate(username, password):
    user = username_table.get(username, None)

    if user and password == user.password:
        return user

users = [User(1, 'Josh', 'mypass'), User(2, 'Lex', 'mypass')]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
