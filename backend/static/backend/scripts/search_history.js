const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

const clearHistoryButton = document.getElementById("clearHistoryButton");
const searches = JSON.parse(document.getElementById('search-history-data').textContent);

document.addEventListener('DOMContentLoaded', function() {
  const modal3 = document.getElementById('myModal3'); 
  const modal4 = document.getElementById('myModal4');
  const confirmDeleteButton = document.getElementById('confirmDeleteButton1');
  const cancelDeleteButton = document.getElementById('cancelDeleteButton1');
  const closeButton = document.getElementById("close-m3");

  searches.forEach(search => {
    addSearchToPage(search);
  });

  clearHistoryButton.addEventListener("click", function() {  
    modal4.style.display = 'block';
  });

  confirmDeleteButton.addEventListener('click', function() {
    deleteAllSearches();
    modal.style.display = 'none';
  });

  cancelDeleteButton.addEventListener('click', function() {
    modal.style.display = 'none';
  });

  closeButton.addEventListener('click', function() {
    modal.style.display = 'none';
  });
});

function addSearchToPage(search) {
  const searchContainer = document.getElementById('reviews-container');
  const searchBox = document.createElement('div');
  searchBox.className = 'search-box';

  const searchInput = document.createElement('h5');
  searchInput.textContent = search.query;
  searchBox.appendChild(searchInput);

  const timestamp = document.createElement('div');
  timestamp.textContent = new Date(search.timestamp).toLocaleDateString();
  searchBox.appendChild(timestamp);

  const deleteButton = document.createElement('button');
  deleteButton.textContent = 'Delete';
  deleteButton.addEventListener("click", function() {
    deleteSearch(search.id);
  });

  searchBox.appendChild(deleteButton);
  searchContainer.appendChild(searchBox);
}

function deleteSearch(searchId) {
  fetch(`/delete_search/${searchId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ searchId })
  })
  .then(response => {
    if (response.ok) {
      showTemporaryMessage("Search deleted successfully.", "alert-success");
      setTimeout(() => window.location.reload(), 2000);
    } else {
      throw new Error("Failed to delete search.");
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showTemporaryMessage("Error deleting search.", "alert-danger");
  });
}

function deleteAllSearches() {
  fetch(`clear_history/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json',
    }
  })
  .then(response => {
    if (response.ok) {
      showTemporaryMessage("All searches deleted successfully.", "alert-success");
      setTimeout(() => window.location.reload(), 2000);
    } else {
      throw new Error("Failed to delete all searches.");
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showTemporaryMessage("Error deleting all searches.", "alert-danger");
  });
}

function showTemporaryMessage(message, messageType) {
  const tempMessageContainer = document.createElement("div");
  tempMessageContainer.textContent = message;
  tempMessageContainer.classList.add("alert", messageType, "temp-message");

  document.body.appendChild(tempMessageContainer);

  setTimeout(() => {
    tempMessageContainer.remove();
  }, 2500);
}
