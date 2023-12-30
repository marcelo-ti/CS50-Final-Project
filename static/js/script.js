function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function openDialog(dialogId) {
  window.addEventListener("DOMContentLoaded", () => {
    const modal = new bootstrap.Modal(document.getElementById(dialogId), {});
    modal.toggle();
  });
}

function openContactUsModal() {
  openDialog("alertModal");
}

function openPetModal() {
  openDialog("petModal");
}

function getPetDetails(id) {
  fetch(`/pet/${id}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("petId").value = data.id;
      document.getElementById("petName").innerText = data.name;
      document.getElementById("petType").innerText = data.type;
      document.getElementById("petAge").innerText = data.age;
      document.getElementById("petSize").innerText = data.size;
      document.getElementById("petGender").innerText = data.gender;
      document.getElementById("petAbout").innerText = data.about;
    });
}

function setDateDefaultValues() {
  window.addEventListener("DOMContentLoaded", () => {
    console.log("test");
    document.getElementById("date").min = new Date()
      .toISOString()
      .split("T")[0];

    const today = new Date();
    const currentYear = today.getFullYear();
    document.getElementById("date").max = new Date(
      today.setYear(currentYear + 1)
    )
      .toISOString()
      .split("T")[0];
  });
}
