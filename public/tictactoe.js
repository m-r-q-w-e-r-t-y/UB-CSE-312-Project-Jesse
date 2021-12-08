// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let colors = ['black', 'blue', 'red', 'pink', 'purple', 'orange', 'yellow', 'green'];

context.strokeStyle = colors[Math.floor(Math.random() * colors.length)];

let actionSendCanvas = "SEND_CANVAS";

let mouseDown = false;

canvas.addEventListener("mousedown", startingCoordinates);
canvas.addEventListener("mousemove", roamingCoordinates);

function startingCoordinates(e) {
    mouseDown = true;
    const {x, y} = canvas.getBoundingClientRect();
    startX = e.clientX - x;
    startY = e.clientY - y;
    console.log("x: " + startX + ", y: " + startY)
    socket.send(JSON.stringify({"x":startX, "y":startY, webSocketAction:actionSendCanvas}));
}

function roamingCoordinates(e) {
    if (e.buttons !== 1) 
        return;

    const {x, y} = canvas.getBoundingClientRect();
    const continuousX = e.clientX - x;
    const continuousY = e.clientY - y;

    context.beginPath();
    context.lineWidth = 5;
    context.moveTo(startX, startY);
    context.lineTo(continuousX, continuousY);
    context.strokeStyle = 'black';
    context.stroke();
    context.closePath();

    startX = continuousX;
    startY = continuousY;
    console.log("x: " + startX + ", y: " + startY)
}

let startX = 0;
let startY = 0;