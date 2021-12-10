// Establish a WebSocket connection with the server
const socket = new WebSocket("ws://" + window.location.host + "/websocket");

const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const actionSendCanvas = "SEND_CANVAS";

let startX, startY;

let color = randomColor();

canvas.addEventListener("mousedown", startingCoordinates);
canvas.addEventListener("mousemove", roamingCoordinates);

/**
 * Generates random RGB for each user connected to websocket
 * @returns {String}
 */
function randomColor() {
  let r = Math.random() * 255;
  let g = Math.random() * 255;
  let b = Math.random() * 255;

  r = Math.floor(r);
  g = Math.floor(g);
  b = Math.floor(b);

  return `rgb(${r}, ${g}, ${b})`;
}

/**
 * On receiving socket messages, parses the data and draws on the canvas
 * @param {MessageEvent} message_event
 */
socket.onmessage = function drawLines(message_event) {
  const data = JSON.parse(message_event.data);

  const x = data["x"],
    y = data["y"],
    endX = data["endX"],
    endY = data["endY"],
    color = data["color"];

  context.beginPath();
  context.lineWidth = 5;
  context.moveTo(x, y);
  context.lineTo(endX, endY);
  context.strokeStyle = color;
  context.stroke();
  context.closePath();
};

/**
 * Sets the starting coordinates of the line
 * @param {MouseEvent} event
 */
function startingCoordinates(event) {
  const { x, y } = canvas.getBoundingClientRect();
  startX = event.clientX - x;
  startY = event.clientY - y;
}

/**
 * Sends coordinates of the drawn line to the websocket server
 * @param {MouseEvent} event
 */
function roamingCoordinates(event) {
  if (event.buttons !== 1) return;

  const { x, y } = canvas.getBoundingClientRect();
  const continuousX = event.clientX - x;
  const continuousY = event.clientY - y;

  socket.send(
    JSON.stringify({
      x: startX,
      y: startY,
      endX: continuousX,
      endY: continuousY,
      color: color,
      webSocketAction: actionSendCanvas,
    })
  );

  startX = continuousX;
  startY = continuousY;
}

function clearCanvas() {
  context.clearRect(0, 0, context.canvas.width, context.canvas.height)

}