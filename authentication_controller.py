from utility import err_resp, internal_err_resp, message
from flask_jwt_extended import create_refresh_token
from bson.objectid import ObjectId

class AuthenticationController():
    def __init__(self, db):
        self.collection = db['authentication_collection']

    def login(self, username, password):
        # Assign vars
        try:
            # Fetch user data
            if not (user := self.collection.find_one({"username":username},{"_id":1,"username":1,"password":1})):
                return err_resp(
                    "The user you have entered does not match any account.",
                    "user_404",
                    404,
                )

            elif username == user['username'] and password == user['password']:
                print(ObjectId(user['_id']))
                # Create access token
                access_token = create_refresh_token(identity=str(ObjectId(user['_id'])))
                print(access_token)
                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["user"] = username

                return resp, 200

            return err_resp(
                "Failed to log in, password may be incorrect.", "password_invalid", 401
            )

        except Exception as error:
            print(error)
            return internal_err_resp()

    def register(self, username,password):

        value = self.collection.find_one({"username":username},{"_id":0,"username":1})
        if value:
            return err_resp("Username is already being used.", "username_taken", 403)

        try:
            data = {"username":username,"password":password}
            inserted_id = self.collection.insert_one(data).inserted_id
            access_token = create_refresh_token(identity=str(ObjectId(inserted_id)))
            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = data["username"]

            return resp, 201


        except Exception as error:
            return internal_err_resp()

    def logout(self, token):
        return self.authentication_service.logout(token)


def test_new_register():
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client['authentication']

    # Test register
    auth = AuthenticationController(db)
    resp = auth.register(username="admin",password="cryptography")
    print(resp)

def test_exsisting_register():
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client['authentication']

    # Test register
    auth = AuthenticationController(db)
    resp = auth.register(username="admin",password="cryptography")
    if resp[1] == 403:
        print("Test passed")

def test_login():
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client['authentication']

    # Test login
    auth = AuthenticationController(db)
    resp = auth.login(username="admin",password="cryptography")
    print(resp)
