// async function logText(event) {
//   event.preventDefault();
//   let inputField = document.getElementById("text-input");
//   let text = inputField.value;

//   if (text.trim() === "") return;
//   let response = await fetch("/log", {
//       method: "POST",
//       headers: { "Content-Type": "application/x-www-form-urlencoded" },
//       body: "text=" + encodeURIComponent(text)
//   });

//   let result = await response.json();
//   if (result.message) {
//       inputField.value = "";
//       loadLogs(); 
//   }
// }

async function addBook(event) {
  event.preventDefault();
  let title = document.getElementById("title-input").value.trim();
  let author = document.getElementById("author-input").value.trim();

  if (!title || !author ) return;

  let response = await fetch("/add-book", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, author })
  });

  let result = await response.json();
  if (result.message) {
      document.getElementById("title-input").value = "";
      document.getElementById("author-input").value = "";
      loadBooks();
      loadLogs();
  }
}

async function loadLogs() {
  let response = await fetch("/logs");
  let data = await response.json();
  document.getElementById("log-display").innerText = data.logs;
}

async function loadBooks() {
  let response = await fetch("/books");
  let data = await response.json();
  document.getElementById("books-display").innerText = data.books;
}

window.onload = () => {
  loadLogs();
  loadBooks();
};