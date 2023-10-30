const url = new URL(window.location.href);
url.protocol = url.protocol.replace("http", "ws");
url.pathname = "/ws" + url.pathname.replace(/\/[^/]+$/, "");

const ws = new WebSocket(url.href);
ws.onopen = () => {
  console.log("WS connected");
}

ws.onclose = () => {
  console.log("WS disconnected");
  setTimeout(window.location.reload.bind(window.location), 5000);
}

ws.onerror = (e) => {
  console.error(e);
  setTimeout(window.location.reload.bind(window.location), 5000);
}

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log(data);
  updateQueue(data);
}
