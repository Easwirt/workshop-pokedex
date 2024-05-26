// JavaScript code
document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById('avatarModal');
    var btn = document.getElementById("openModalBtn");
    var span = document.getElementsByClassName("close")[0];
    var avatarOptions = document.querySelectorAll('.avatar');

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    avatarOptions.forEach(function(avatar) {
        avatar.addEventListener('click', function() {
            var selectedAvatar = this.getAttribute('data-avatar');
            window.location.href = 'changeavatar/' + selectedAvatar;
            modal.style.display = "none";
        });
    });
});
