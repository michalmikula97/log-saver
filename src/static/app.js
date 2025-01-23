async function logText(event) {
  event.preventDefault();
  let inputField = document.getElementById("text-input");
  let text = inputField.value;

  if (text.trim() === "") return;
  let response = await fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "text=" + encodeURIComponent(text)
  });

  let result = await response.json();
  if (result.message) {
      inputField.value = "";
      loadLogs(); 
  }
}

async function loadLogs() {
  let response = await fetch("/logs");
  let data = await response.json();
  document.getElementById("log-display").innerText = data.logs;
}

window.onload = loadLogs;
