// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let isMouseDown = false;

const c = document.getElementById("canvas");
c.addEventListener("mousedown", () => (isMouseDown = true)); // fires before mouse left btn is released
// c.addEventListener("mousemove", helper);
// c.addEventListener("mousemove", move);
c.addEventListener("mousedown", () => {
    isMouseDown = true;
    socket.send("Clicking mouse");
});
// c.addEventListener("mouseup", send);
c.width = window.innerWidth;
c.height = window.innerHeight;


const ctx = c.getContext("2d");

function coordinates(e) {
    const {x, y} = c.getBoundingClientRect();
    lastX = e.clientX - x;
    lastY = e.clientY - y;
    console.log("x: " + lastX + " " + "y: " + lastY);
    
    // var data = {
    //     x: lastX,
    //     y: lastY
    // }

    // socket.send(data)
}

function helper(e) {
    if (e.buttons !== 1) {
        return; // left button is not pushed yet
    }
    draw(e);
}

function draw(e) {
    const {x, y} = c.getBoundingClientRect();
    const newX = e.clientX - x;
    const newY = e.clientY - y;
    
    ctx.beginPath();
    ctx.lineWidth = 5;
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(newX, newY);
    ctx.strokeStyle = 'black';
    ctx.stroke();
    ctx.closePath();
    
    lastX = newX;
    lastY = newY;
    console.log("x: " + lastX + " " + "y: " + lastY);

    var data = {
        x: lastX,
        y: lastY
    }
}

function send(e) {
    socket.send(JSON.stringify({"up":1}));
}
function down(e) {
    socket.send(JSON.stringify({"down":1}));
}
function move(e) {
    socket.send(JSON.stringify({"move":1}));
}

let lastX = 0;
let lastY = 0;  
