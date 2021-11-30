var mysql = require('mysql2');
const dbConfig = require("./databaseConfig");

class Database {

    /* database connection will be assigned to this variable */
    connection = null;

    constructor() {
        
        this.connection = mysql.createConnection({
            host: dbConfig.HOST,
            user: dbConfig.USER,
            password: dbConfig.PASSWORD,
            database:"gameDB"
        });
          
        this.connection.connect(function(err) {
            if (err) {
                console.log("Refused Connetion!");
                throw err
            } 
            console.log("Connected!");
        });

        this.createUserTable();
    }

    createUserTable() {

        var sqlStatement = "CREATE TABLE IF NOT EXISTS user (email TEXT, name TEXT)";
        this.connection.query(sqlStatement, function (err) {
        if (err) {
            console.log("Unable to create user Table!");
            throw err;
        }
        console.log("Successfully created user Table!");
        });
    }

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

    insertUser(values) {

        /* using mysql.format allows use to escape the values, however values should be escaped when passed */
        var sqlStatement = "INSERT INTO user (email, name) VALUES (?, ?)";
        sqlStatement = mysql.format(sqlStatement, values)

        this.connection.query(sqlStatement, function (err) {
        if (err) {
            console.log("Unable to insert into user Table!");
            throw err;
        }
        console.log("Successfully interted into user Table created!");
        });
    }

    selectAllUser() {

        var sqlStatement = "SELECT * FROM user";
        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to select all from user Table!");
            throw err;
        }
        console.log("Successfully selected all from user Table created!");
        console.log(result)
        });
    }

    selectUserByName(name) {

        var sqlStatement = "SELECT * FROM user WHERE name = ?";
        sqlStatement = mysql.format(sqlStatement, name)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to select by name from user Table!");
            throw err;
        }
        console.log("Successfully selected by name from user Table created!");
        console.log(result)
        });
    }

    deleteUserByName(name) {

        var sqlStatement = "DELETE FROM user WHERE name = ?";
        sqlStatement = mysql.format(sqlStatement, name)

        this.connection.query(sqlStatement, function (err, result) {
        if (err) {
            console.log("Unable to delete by name from user Table!");
            throw err;
        }
        console.log("Successfully deleted by name from user Table created!");
        console.log("Number of records deleted: " + result.affectedRows);
        });
    }

};

module.exports = Database
