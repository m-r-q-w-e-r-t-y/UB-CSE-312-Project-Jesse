var mysql = require('mysql2');
const Database = require("../database");

class UserDatabase {

    /* database connection will be assigned to this variable */
    connection = null;

    constructor() {

        let database = new Database();
        this.connection = database.getConnection();
        this.createUserTable();
    }

    /* Used to create user Table */
    createUserTable() {

        var sqlStatement = "CREATE TABLE IF NOT EXISTS user (userId INT AUTO_INCREMENT, username TEXT NOT NULL, hashedPassword TEXT NOT NULL, profilePicPath TEXT, authToken TEXT, primary key (userId))";
        this.connection.query(sqlStatement, function (err) {
        if (err) {
            console.log("Unable to create user Table!");
            throw err;
        }
        console.log("Successfully created user Table!");
        });
    }

    /* Used to deop user Table */
    dropUserTable() {

        var sqlStatement = "DROP TABLE user";
        this.connection.query(sqlStatement, function (err) {
        if (err) {
            console.log("Unable to drop user Table!");
            throw err;
        }
        console.log("Successfully dropped user Table!");
        });
    }


    /* Used to insert into user Table, ex: values=['bob','password','picture/path'] */
    insertUser(values) {

        var sqlStatement = "INSERT INTO user (username, hashedPassword, profilePicPath) VALUES (?, ?, ?)";
        sqlStatement = mysql.format(sqlStatement, values)

        this.connection.query(sqlStatement, function (err) {
        if (err) {
            console.log("Unable to insert into user Table!");
            throw err;
        }
        console.log("Successfully interted into user Table!");
        });
    }

    /* Used to retrieve all records inside user Table */
    selectAllUser(callback) {

        var sqlStatement = "SELECT * FROM user";
        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to select all from user Table!");
            throw err;
        }

        if(result.length > 0) {

            console.log("Successfully selected by name from user Table!");
            const records = [];

            for (var row of result) {

                const userMap = new Map();
                userMap.set("id", row.userId);
                userMap.set("username", row.username);
                userMap.set("password", row.hashedPassword);
                userMap.set("profilePicPath", row.profilePicPath);
                userMap.set("authToken", row.authToken);

                records.push(userMap);
                
            }
            callback(records);
        }
        else {
            console.log("No records were found!");
            callback([]);
        }
        
        });
    }

    /* Used to retrieve record of user specified by name, ex: name = ['bob'] */
    getUserRecordByName(name, callback) {

        var sqlStatement = "SELECT * FROM user WHERE username = ?";
        sqlStatement = mysql.format(sqlStatement, name)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to select by username = "+name[0]+" from user Table!");
            throw err;
        }

        if(result.length > 0) {

            console.log("Successfully selected by name from user Table!");
            
            const userMap = new Map();
            userMap.set("id", result[0].userId);
            userMap.set("username", result[0].username);
            userMap.set("password", result[0].hashedPassword);
            userMap.set("profilePicPath", result[0].profilePicPath);
            userMap.set("authToken", result[0].authToken);

            callback(userMap);
        }
        else {
            console.log("No records were found!");
            callback(null);
        }

        });
    }

    /* Used to retrieve record of user specified by token, ex: token = ['token1'] */
    getUserRecordByAuthToken(token, callback) {

        var sqlStatement = "SELECT * FROM user WHERE authToken = ?";
        sqlStatement = mysql.format(sqlStatement, token)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to select by authToken = "+token[0]+" from user Table!");
            throw err;
        }

        if(result.length > 0) {

            console.log("Successfully selected by token from user Table!");
            
            const userMap = new Map();
            userMap.set("id", result[0].userId);
            userMap.set("username", result[0].username);
            userMap.set("password", result[0].hashedPassword);
            userMap.set("profilePicPath", result[0].profilePicPath);
            userMap.set("authToken", result[0].authToken);

            callback(userMap);
        }
        else {
            console.log("No records were found!");
            callback(null);
        }

        });
    }

    /* Used to retrieve the id of username, ex: username = ['bob'] */
    getIdByUsername(username, callback) {

        this.getUserRecordByName(username, function(result) {
            if(result == null) {
                callback(result)
            }
            else {
                callback(result.get('id'));
            }
        });
    }

    /* Used to retrieve the password of username, ex: username = ['bob'] */
    getPasswordByUsername(username, callback) {

        this.getUserRecordByName(username, function(result) {
            if(result == null) {
                callback(result)
            }
            else {
                callback(result.get('password'));
            }
        });
    }

    /* Used to retrieve the authToken of username, ex: username = ['bob'] */
    getAuthTokenByUsername(username, callback) {
        
        this.getUserRecordByName(username, function(result) {
            if(result == null) {
                callback(result)
            }
            else {
                callback(result.get('authToken'));
            }
        });
    }

    /* Used to retrieve the profilePicPath of username, ex: username = ['bob'] */
    getProfilePicPathByUsername(username, callback) {
        
        this.getUserRecordByName(username, function(result) {
            if(result == null) {
                callback(result)
            }
            else {
                callback(result.get('profilePicPath'));
            }
        });
    }

    /* Used to retrieve the username of authToken, ex: token = ['token1'] */
    getUsernameByAuthToken(token, callback) {
        
        this.getUserRecordByAuthToken(token, function(result) {
            if(result == null) {
                callback(result)
            }
            else {
                callback(result.get('username'));
            }
        });
    }

    /* Used to update the authToken of username, ex: username = ['bob'] */
    updateUserAuthTokenByName(values) {

        var sqlStatement = "UPDATE user SET authToken = ? WHERE username = ?";
        sqlStatement = mysql.format(sqlStatement, values)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to update authToken by name from user Table!");
            throw err;
        }
        console.log("Successfully updated authToken by name from user Table!");
        console.log(result.affectedRows + " record(s) updated");
        });
    }

    /* Used to delete record from user table by username, ex: username = ['bob'] */
    deleteUserByName(username) {

        var sqlStatement = "DELETE FROM user WHERE username = ?";
        sqlStatement = mysql.format(sqlStatement, username)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to delete by name from user Table!");
            throw err;
        }
        console.log("Successfully deleted by name from user Table!");
        console.log("Number of records deleted: " + result.affectedRows);
        });
    }

};

module.exports = UserDatabase