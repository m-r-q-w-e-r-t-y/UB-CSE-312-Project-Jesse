// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let actionOnlineUser = "ONLINE_USERS";
let actionGetUsername = "GET_USERNAME";

// Once socket is open, getUsername will be called
socket.addEventListener('open', function(){getUsername()});

function getUsername() {

    if (checkACookieExists("authToken")) {
        socket.onmessage = populateUsername;
        let authToken = getCookie("authToken")
        let request = {webSocketAction: actionGetUsername, "authToken": authToken};
        socket.send(JSON.stringify(request));
    }
}

function populateUsername(message) {
     document.getElementById("username").innerHTML= JSON.parse(message.data);
}

function checkACookieExists(cookieName) {
    if (document.cookie.split(';').some((item) => item.trim().startsWith(cookieName+'='))) {
      return true
    }
    return false
}

function getCookie(cookieName) {
    return document.cookie.split('; ').find(row => row.startsWith(cookieName+'=')).split('=')[1];
}

function getOnlineUsers() {
    let username = document.getElementById("username").innerHTML
    let request = {webSocketAction:actionOnlineUser, "username": username};
    socket.send(JSON.stringify(request));
    socket.onmessage = addOnlineUsers;
}

function addOnlineUsers(message) {
    let contacts = JSON.parse(message.data);
    openForm(contacts);
}

function openForm(contacts) {

    document.getElementById("messenger").style.display = "block";
    let messengerContent = '<button class="close-messaging-tab" onclick="closeForm()" >Messages</button>' +
        '<div class="user-container">';

    if(contacts.length>0) {
        contacts.forEach(user => {
        messengerContent=messengerContent+'<div class="user-tab" id="'+user+'" onclick="openChat(this.id)" ><p class="center-user-name">'+user+'</p></div>';
        })
    }
    else {
        messengerContent=messengerContent+"<h4 class=\"none-online\" >No users are online!</h4>"
    }
    // contacts.forEach(user => {
    //     messengerContent=messengerContent+'<div class="user-tab" id="'+user+'" onclick="openChat(this.id)" ><p class="center-user-name">'+user+'</p></div>';
    // })
    messengerContent = messengerContent + '</div>';

    document.getElementById("messenger").innerHTML=messengerContent;
}

function closeForm() {
    document.getElementById("messenger").style.display = "none";
}

function openChat(user) {

    // @TODO Ajax call should be made to retrieve the conversation between Logged in account user and the user passed via argument
    let messageLog = [
        {'User': 'Hey!'},
        {'User2': 'Hey, whats up'},
        {'User': 'Want to play tic tac toe? Bet you cant beat me!'},
        {'User2': 'Sure, lets go!'},
        {'User': "Sending invite"},
        {'User2': "GG"},
        {'User': "That was beginners luck! Run it back!"},
        {'User2': "If you say, Im down"},]

    let chatContent = '<button class="close-messaging-tab" onclick="openForm()" >'+user+'</button>\n' +
        '<div class="chat-container">\n' +
        '<form >\n' +
        '<div class="message-window">'


    for (const dialog of messageLog) {
            for (const [userName, message] of Object.entries(dialog)) {
        chatContent=chatContent+'<p><b>'+userName+':</b> '+message+'</p>'
        }
    }

    //TODO Need to add post a method that will send the typed to the database and update the chat
    chatContent = chatContent+'</div>\n' +
        '<textarea placeholder="Type message.." id="msg" required></textarea>\n' +
        '<button type="button" class="btn">Send</button>\n' +
        '<button type="button" class="btn cancel" onclick="closeForm()">Close</button>\n' +
        '<button type="button" class="btn playGame">Play Tic Tac Toe</button>\n' +
        '</form></div>'

    document.getElementById("messenger").innerHTML=chatContent;
}