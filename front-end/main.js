const apiUrl = "http://localhost:8000/pallets/";

const palletTableBody = document.querySelector("#palletTable tbody");
const addPalletForm = document.getElementById("addPalletForm");
const nameInput = document.getElementById("name");
const weightInput = document.getElementById("weight");
const dimensionsInput = document.getElementById("dimensions");

let editingId = null;  // Track whether we're editing an existing pallet

window.onload = loadPallets;

function loadPallets() {
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      palletTableBody.innerHTML = "";
      data.forEach(pallet => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${pallet.id}</td>
          <td>${pallet.name}</td>
          <td>${pallet.weight}</td>
          <td>${pallet.dimensions}</td>
          <td>
            <button class="btn btn-secondary btn-sm me-2" onclick="editPallet(${pallet.id})">Edit</button>
            <button class="btn btn-danger btn-sm" onclick="deletePallet(${pallet.id})">Delete</button>
          </td>
        `;
        palletTableBody.appendChild(row);
      });
    })
    .catch(error => console.error("Error loading pallets:", error));
}

addPalletForm.addEventListener("submit", event => {
  event.preventDefault();

  const palletData = {
    name: nameInput.value,
    weight: parseFloat(weightInput.value),
    dimensions: dimensionsInput.value
  };

  if (editingId === null) {
    // Create new pallet
    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(palletData)
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to add pallet");
        return response.json();
      })
      .then(() => {
        addPalletForm.reset();
        loadPallets();
      })
      .catch(error => console.error("Error adding pallet:", error));
  } else {
    // Update existing pallet
    fetch(apiUrl + editingId, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(palletData)
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to update pallet");
        return response.json();
      })
      .then(() => {
        addPalletForm.reset();
        editingId = null;
        addPalletForm.querySelector("button").textContent = "Add Pallet";
        loadPallets();
      })
      .catch(error => console.error("Error updating pallet:", error));
  }
});

function editPallet(id) {
  fetch(apiUrl + id)
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch pallet");
      return response.json();
    })
    .then(pallet => {
      nameInput.value = pallet.name;
      weightInput.value = pallet.weight;
      dimensionsInput.value = pallet.dimensions;
      editingId = id;
      addPalletForm.querySelector("button").textContent = "Save Changes";
    })
    .catch(error => console.error("Error loading pallet for edit:", error));
}

function deletePallet(id) {
  if (!confirm("Are you sure you want to delete this pallet?")) return;

  fetch(apiUrl + id, {
    method: "DELETE"
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to delete pallet");
      loadPallets();
    })
    .catch(error => console.error("Error deleting pallet:", error));
}
