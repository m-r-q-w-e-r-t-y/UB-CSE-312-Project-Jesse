// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// Call the addMessage function whenever data is received from the server over the WebSocket
socket.onmessage = getOnlineUsers;

let actionOnlineUser = "ONLINE_USERS";

function getOnlineUsers() {
    let request = {webSocketAction:actionOnlineUser};
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

    contacts.forEach(user => {
        messengerContent=messengerContent+'<div class="user-tab" id="'+user+'" onclick="openChat(this.id)" ><p class="center-user-name">'+user+'</p></div>';
    })
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


function playGame() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
       if (this.readyState === 4 && this.status === 200){
          console.log(this.response)
       }
    }

    // For security purposes, use a POST request
    request.open("GET", "/tictactoe");
    // request.send(jsonData);
}

if(window.attachEvent) {
    window.attachEvent('onload', playGame());
} else {
    if(window.onload) {
        var curronload = window.onload;
        var newonload = function(evt) {
            curronload(evt);
            yourFunctionName(evt);
        };
        window.onload = newonload;
    } else {
        window.onload = playGame();
    }
}