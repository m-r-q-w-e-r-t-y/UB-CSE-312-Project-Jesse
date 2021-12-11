// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let actionOnlineUser = "ONLINE_USERS";
let actionLoadChat = "LOAD_CHAT";
let actionSendMessage = "SEND_MESSAGE";
let username2 = ""

socket.onmessage = addMessage;


function getOnlineUsers() {
    let request = {webSocketAction:actionOnlineUser};
    socket.send(JSON.stringify(request));
    socket.onmessage = addOnlineUsers;
}

function addOnlineUsers(messageEvent) {
    let data = JSON.parse(messageEvent.data);
    openForm(data);
}

function openForm(data) {

    let onlineUsers = data[0]
    let profilePics = data[1]
    let index = 0
    document.getElementById("messenger").style.display = "block";
    let messengerContent = '<button class="close-messaging-tab" onclick="closeForm()" >Messages</button>' +
        '<div class="user-container">';

    if(onlineUsers.length>0) {
        onlineUsers.forEach(user => {
        messengerContent=messengerContent+'<div class="user-tab" id="'+user+'" onclick="loadChat(this.id)"><img src="'+profilePics[index]+'"">' +
            '<p class="center-user-name">'+user+'</p></div>';
        index+=1
        })
    }
    else {
        messengerContent=messengerContent+"<h4 class=\"none-online\" >No users are online!</h4>"
    }

    messengerContent = messengerContent + '</div>';
    document.getElementById("messenger").innerHTML=messengerContent;
    socket.onmessage = addMessage;
}

function closeForm() {
    document.getElementById("messenger").style.display = "none";
}

function playGame() {
    window.location.href = "/canvas.html"
}

function loadChat(userClicked) {
    let request = {webSocketAction:actionLoadChat, "userClicked":userClicked};
    username2 = userClicked
    socket.send(JSON.stringify(request));
    socket.onmessage = openChat;
}

function openChat(messageEvent) {

    let messageLog = JSON.parse(messageEvent.data);
    let user = username2

    let chatContent = '<button class="close-messaging-tab" onclick="openForm()" >'+user+'</button>\n' +
        '<div class="chat-container">\n' +
        '<form >\n' +
        '<div class="message-window" id="message-panel">'

    if (messageLog.length>0){

        for (const dialog of messageLog) {
            for (const [userName, message] of Object.entries(dialog)) {
                chatContent=chatContent+'<p><b>'+userName+':</b> '+message+'</p>'
            }
        }
    }

    chatContent = chatContent+'</div>\n' +
        '<textarea placeholder="Type message.." id="msg" required></textarea>\n' +
        '<button type="button" class="btn" onclick="sendMessage(username2)">Send</button>\n' +
        '<button type="button" class="btn cancel" onclick="closeForm()">Close</button>\n' +
        '<button type="button" class="btn playGame" onclick="playGame()">Canvas</button>\n' +
        '</form></div>'

    document.getElementById("messenger").innerHTML=chatContent;
    socket.onmessage = addMessage;
}

function sendMessage(sendingTo) {
    let text = document.getElementById("msg").value
    let request = {webSocketAction:actionSendMessage, "sendingTo":sendingTo, "message":text};
    socket.send(JSON.stringify(request));
    socket.onmessage = addMessage;
}

function addMessage(messageEvent) {

    let messageDetails = JSON.parse(messageEvent.data);
    let notifyingUser = messageDetails[0].client2;
    messageDetails.shift()

    if(document.getElementById("message-panel") != null) {
        let chatContent = document.getElementById("message-panel").innerHTML
        for (const dialog of messageDetails) {
            for (const [userName, message] of Object.entries(dialog)) {
                chatContent=chatContent+'<p><b>'+userName+':</b> '+message+'</p>'
            }
        }
        document.getElementById("message-panel").innerHTML=chatContent;
    }

    let userValue = document.getElementById("username").innerText;
    let username = userValue.substring(8);

    if(username === notifyingUser) {
        messageMap = messageDetails[0]
        for(name in messageMap) {
            showNotifications(name)
        }
    }
}

function disableNotifications(){
    document.getElementById("notify").style.visibility = "hidden";
}

function showNotifications(sender){
    document.getElementById("notify").innerHTML="New Message from: "+sender;
    document.getElementById("notify").style.visibility = "visible";
    window.setTimeout(disableNotifications, 3000);
}