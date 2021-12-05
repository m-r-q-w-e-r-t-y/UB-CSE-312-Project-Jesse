import json

import mysql
import mysql.connector
import os
from database.UserDatabase import UserDatabase


class ChatDatabase:
    connection = None
    userDb = None

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.userDb = UserDatabase()
        self.createChatTable()

    # Used to create chat Table
    def createChatTable(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS chat (user1 TEXT NOT NULL, user2 TEXT NOT NULL, user1Id INT NOT NULL, user2Id INT NOT NULL, conversation JSON, FOREIGN KEY (user1Id) REFERENCES user(userId) ON DELETE CASCADE, FOREIGN KEY (user2Id) REFERENCES user(userId) ON DELETE CASCADE)")
        print("Successfully created chat Table!")

    # Used to chat user Table
    def dropChatTable(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE chat")
        print("Successfully dropped chat Table!")

    # Used to insert chat record inside chat Table
    def initializeChatRecord(self, username, username2):
        sortedName = [username, username2]
        sortedName.sort()
        user1Id = self.userDb.getIdByUsername(sortedName[0])
        user2Id = self.userDb.getIdByUsername(sortedName[1])
        conversation = json.dumps([])

        cursor = self.connection.cursor()
        sqlQuery = "INSERT INTO chat (user1, user2, user1Id, user2Id, conversation) VALUES (%s, %s, %s, %s, %s)"
        sqlValues = (sortedName[0], sortedName[1], user1Id, user2Id, conversation)
        cursor.execute(sqlQuery, sqlValues)
        self.connection.commit()
        print("Successfully inserted user into user Table!")

    def selectAllChatRecords(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM chat")
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Successfully selected all records from chat Table!")

            records = []
            for row in result:
                chatMap = {}

                chatMap["username"] = row[0]
                chatMap["username2"] = row[1]
                chatMap["user1Id"] = row[2]
                chatMap["user2Id"] = row[3]
                chatMap["conversation"] = json.loads(row[4])
                records.append(chatMap)
            return records

        print("No chat records were found from chat Table!")
        return []

    def getChatRecordByNames(self, username, username2):
        sortedName = [username, username2]
        sortedName.sort()

        cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM chat where user1 = %s AND user2 = %s"
        sqlValues = (sortedName[0], sortedName[1])
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            print("Successfully selected chat record for users:" + sortedName[0] + "and " + sortedName[1] + ", from chat Table!")
            row = result[0]
            chatMap = {}

            chatMap["username"] = row[0]
            chatMap["username2"] = row[1]
            chatMap["user1Id"] = row[2]
            chatMap["user2Id"] = row[3]
            chatMap["conversation"] = json.loads(row[4])
            return chatMap

        print("No chat record were found for users:" + sortedName[0] + "and " + sortedName[1] + ", from chat Table!")
        return {}

    def getConversationByNames(self, username, username2):
        chatRecord = self.getChatRecordByNames(username, username2)
        if bool(chatRecord):
            return chatRecord["conversation"]
        else:
            return None

    def insertMessagesByNames(self, senderUsername, message, receiverUsername):

        # check if a record for these two users has been initialize
        record = self.getChatRecordByNames(senderUsername, receiverUsername)
        if not bool(record):
            self.initializeChatRecord(senderUsername, receiverUsername)

        updateConversation = self.getConversationByNames(senderUsername, receiverUsername)
        updateConversation.append({"sentFrom": senderUsername, "message": message})
        updateConversation = json.dumps(updateConversation)

        sortedName = [senderUsername, receiverUsername]
        sortedName.sort()

        cursor = self.connection.cursor()
        sqlQuery = "UPDATE chat SET conversation = %s where user1 = %s AND user2 = %s"
        sqlValues = (updateConversation, sortedName[0], sortedName[1])
        cursor.execute(sqlQuery, sqlValues)
        self.connection.commit()
        print("Successfully updated conversation for users:" + sortedName[0] + "and " + sortedName[1] + ", from chat Table!")
