// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

const canvas = document.querySelector("canvas");
const context = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

context.fillStyle = "black"

let mouseDown = false;

canvas.addEventListener("mousedown", () => {
    mouseDown = true;
    socket.send("Client is clicking their mouse!");
});
canvas.addEventListener("mouseup", () => (mouseDown = false));
canvas.addEventListener("mousemove", e => {
    if(mouseDown){
        context.fillRect(e.offsetX, e.offsetY, 15, 15);
    }
});