// JavaScript code
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById('avatarModal');
    var btn = document.getElementById("openModalBtn");
    var span = document.getElementsByClassName("close")[0];
    var avatarOptions = document.querySelectorAll('.avatar');

    // Open modal when the button is clicked
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // Close modal when the close button is clicked
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Close modal when user clicks outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Handle avatar selection
    avatarOptions.forEach(function(avatar) {
        avatar.addEventListener('click', function() {
            var selectedAvatar = this.getAttribute('data-avatar');
            // You can do something with the selected avatar, like updating the user's profile
            console.log("Selected avatar:", selectedAvatar);
            modal.style.display = "none"; // Close the modal after selection
        });
    });
});
