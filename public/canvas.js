// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let actionSendCanvas = "SEND_CANVAS";

let mouseDown = false;
let color = randomColor();

canvas.addEventListener("mousedown", startingCoordinates);
canvas.addEventListener("mousemove", roamingCoordinates);

function randomColor() {
    let r = Math.random() * 255;
    let g = Math.random() * 255;
    let b = Math.random() * 255;
    return `rgb(${r}, ${g}, ${b})`;
}

socket.onmessage = function receivingData(data) {
    roamingCoordinates(JSON.parse(data));
}

function startingCoordinates(data) {
    mouseDown = true;
    const {x, y} = canvas.getBoundingClientRect();
    startX = data.clientX - x;
    startY = data.clientY - y;
    console.log("x: " + startX + ", y: " + startY)
    socket.send(JSON.stringify({"x":startX, "y":startY, webSocketAction:actionSendCanvas}));
}

function roamingCoordinates(data) {
    if (data.buttons !== 1) 
        return;

    const {x, y} = canvas.getBoundingClientRect();
    const continuousX = data.clientX - x;
    const continuousY = data.clientY - y;

    context.beginPath();
    context.lineWidth = 5;
    context.moveTo(startX, startY);
    context.lineTo(continuousX, continuousY);
    context.strokeStyle = color;
    context.stroke();
    context.closePath();

    startX = continuousX;
    startY = continuousY;
    console.log("x: " + startX + ", y: " + startY)
}

let startX = 0;
let startY = 0;