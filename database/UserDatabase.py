import mysql
import mysql.connector
import os
import bcrypt
from constants import auth_token_salt


class UserDatabase:
    connection = None

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.createUserTable()

    # Used to create user Table
    def createUserTable(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user (userId INT AUTO_INCREMENT, username TEXT NOT NULL, hashedPassword TEXT NOT NULL, profilePicPath TEXT NOT NULL, authToken TEXT, loggedIn BOOLEAN, primary key (userId))")
        print("Successfully created user Table!")

    # Used to drop user Table
    def dropUserTable(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE user")
        print("Successfully dropped user Table!")

    # Used to insert into user Table
    def insertUser(self, username, password, profilePicPath):
        try:
            cursor = self.connection.cursor()
            sqlQuery = "INSERT INTO user (username, hashedPassword, profilePicPath, loggedIn) VALUES (%s, %s, %s, %s)"
            sqlValues = (username, password, profilePicPath, False)
            cursor.execute(sqlQuery, sqlValues)
            self.connection.commit()
            print("Successfully inserted user into user Table!")
        except:
            print("Unable to insert user into user Table!")

    # Used to retrieve all records inside user Table
    def selectAllUser(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Successfully selected all users from user Table!")

            records = []
            for row in result:
                userMap = {}

                userMap["id"] = row[0]
                userMap["username"] = row[1]
                userMap["password"] = row[2]
                userMap["profilePicPath"] = row[3]
                userMap["authToken"] = row[4]
                userMap["loggedIn"] = row[5]
                records.append(userMap)
            return records

        print("No user records were found from user Table!")
        return []

    # Used to retrieve record of user specified by name
    def getUserRecordByName(self, username):
        cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM user WHERE username = %s"
        sqlValues = (username,)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Successfully selected " + username + "'s record from user Table!")

            row = result[0]
            userMap = {}
            userMap["id"] = row[0]
            userMap["username"] = row[1]
            userMap["password"] = row[2]
            userMap["profilePicPath"] = row[3]
            userMap["authToken"] = row[4]
            userMap["loggedIn"] = row[5]
            return userMap

        print(username + "'s record was not found from user Table!")
        return None

    # Used to retrieve record of user specified by token
    def getUserRecordByAuthToken(self, authToken):
        if type(authToken) is str:
            authToken = authToken.encode()
        hashed_auth_token = bcrypt.hashpw(authToken, auth_token_salt)
        cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM user WHERE authToken = %s"
        sqlValues = (hashed_auth_token,)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Successfully selected record by authToken from user Table!")

            row = result[0]
            userMap = {}
            userMap["id"] = row[0]
            userMap["username"] = row[1]
            userMap["password"] = row[2]
            userMap["profilePicPath"] = row[3]
            userMap["authToken"] = row[4]
            userMap["loggedIn"] = row[5]
            return userMap

        print("No record was found from given authToken user Table!")
        return None

    # Used to retrieve the id of username
    def getIdByUsername(self, username):
        userRecord = self.getUserRecordByName(username)
        if userRecord:
            return userRecord["id"]
        else:
            return None

    # Used to retrieve the password of username
    def getPasswordByUsername(self, username):
        userRecord = self.getUserRecordByName(username)
        if userRecord:
            return userRecord["password"]
        else:
            return None

    # Used to retrieve the authToken of username
    def getAuthTokenByUsername(self, username):
        userRecord = self.getUserRecordByName(username)
        if userRecord:
            return userRecord["authToken"]
        else:
            return None

    # Used to retrieve the profilePicPath of username
    def getProfilePicPathByUsername(self, username):
        userRecord = self.getUserRecordByName(username)
        if userRecord:
            return userRecord["profilePicPath"]
        else:
            return None

    # Used to retrieve the username of authToken
    def getUsernameByAuthToken(self, authToken):
        userRecord = self.getUserRecordByAuthToken(authToken)
        if userRecord:
            return userRecord["username"]
        else:
            return None

    # Used to update the authToken of username
    def updateAuthTokenByUsername(self, authToken, username):
        try:
            cursor = self.connection.cursor()
            sqlQuery = "UPDATE user SET authToken = %s WHERE username = %s"
            sqlValues = (authToken, username)
            cursor.execute(sqlQuery, sqlValues)
            self.connection.commit()
            print("Successfully updated " + username + "'s authToken from user Table!")
        except:
            print("Unable to update " + str(username) + "'s authToken from user Table!")

    # Used to update the loggedIn of username
    def updateLoggedInByUsername(self, logInStatus, username):
        try:
            cursor = self.connection.cursor()
            sqlQuery = "UPDATE user SET loggedIn = %s WHERE username = %s"
            sqlValues = (logInStatus, username)
            cursor.execute(sqlQuery, sqlValues)
            self.connection.commit()
            if logInStatus:
                print("Successfully updated " + username + "'s loggIn status to true from user Table!")
            else:
                print("Successfully updated " + username + "'s loggIn status to false from user Table!")
        except:
            print("Unable to update " + str(username) + "'s loggIn status from user Table!")

    # Used to delete record from user table by username
    def deleteUserByName(self, username):
        try:
            cursor = self.connection.cursor()
            sqlQuery = "DELETE FROM user WHERE username = %s"
            sqlValues = (username,)
            cursor.execute(sqlQuery, sqlValues)
            self.connection.commit()
            print("Successfully deleted " + username + "'s record from user Table!")
        except:
            print("Unable to delete " + str(username) + "'s record from user Table!")

    # Retrieve all usernames of logged in users from user table, output excludes the username given in parameter
    def getLoggedInUsers(self, username):
        cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM user WHERE username != %s AND loggedIn = %s"
        sqlValues = (username, 1)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Found other online users from user Table!")

            records = []
            for row in result:
                records.append(row[1])
            return records

        print("No other online user records were found from user Table!")
        return []

    # Retrieve all profilePicPaths of logged in users from user table, output excludes the username given in parameter
    def getLoggedInPics(self, username):
        cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM user WHERE username != %s AND loggedIn = %s"
        sqlValues = (username, 1)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Found other online users from user Table!")

            records = []
            for row in result:
                records.append(row[3])
            return records

        print("No other online user records were found from user Table!")
        return []
