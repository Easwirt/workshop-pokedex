document.addEventListener('DOMContentLoaded', function() {
    var clearHistoryBtn = document.getElementById("clearBtn");
    var editBioBtn = document.getElementById("editBioBtn");
    var editBioForm = document.getElementById("editBioForm");
    var newBioInput = document.getElementById("newBioInput");
    var saveBioBtn = document.getElementById("saveBioBtn");
    var cancelBioBtn = document.getElementById("cancelBioBtn");
    var currentBio = document.getElementById("currentBio");
    var recentActivity = document.getElementById("recentActivity");
    var changePasswordBtn = document.getElementById("changePasswordBtn");
    var passwordForm = document.getElementById("passwordForm");
    var oldPasswordInput = document.getElementById("oldPassword");
    var newPassword1Input = document.getElementById("newPassword1");
    var newPassword2Input = document.getElementById("newPassword2");
    var savePasswordBtn = document.getElementById("savePasswordBtn");
    var cancelPasswordBtn = document.getElementById("cancelPasswordBtn");
    var privacySettingsBtn = document.getElementById("privacySettingsBtn");


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (clearHistoryBtn) {
        clearHistoryBtn.onclick = function () {
            var userConfirmed = confirm("Are you sure you want to clear your recent activity?");

            if (userConfirmed) {
                fetch('/profile/editprofile/clearrecentactivity/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Network response not ok.');
                    }
                })
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        recentActivity.innerHTML = "<p>Recent activity cleared.</p>";
                    }
                })
                .catch(error => {
                    console.error('Error clearing recent activity:', error);
                });
            } else {
                console.log("You decided to keep your recent activity.");
            }
        };
    }

    if (editBioBtn && editBioForm && newBioInput && saveBioBtn && cancelBioBtn && (currentBio || currentBio == null)) {
        editBioBtn.onclick = function () {
            editBioForm.style.display = 'block';
            currentBio.style.display = 'none';
            newBioInput.value = currentBio.innerText.trim();
        };

        cancelBioBtn.onclick = function () {
            editBioForm.style.display = 'none';
            currentBio.style.display = 'block';
            newBioInput.value = '';
        };
        
        saveBioBtn.onclick = function () {
            var newBio = newBioInput.value.trim();
            if (newBio === '') {
                alert('Bio cannot be empty!');
                return;
            }
        
            fetch('/profile/editprofile/updatebio/' + encodeURIComponent(newBio) + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response not ok.');
                }
            })
            .then(data => {
                console.log('Bio updated:', data);
                currentBio.innerText = newBio;
                editBioForm.style.display = 'none';
                currentBio.style.display = 'block';
            })
            .catch(error => {
                console.error('Error updating bio:', error);
            });
        };
    }

    if (changePasswordBtn && passwordForm && oldPasswordInput && newPassword1Input && newPassword2Input && savePasswordBtn && cancelPasswordBtn) {
        changePasswordBtn.onclick = function () {
            passwordForm.style.display = 'block';
        };

        cancelPasswordBtn.onclick = function () {
            passwordForm.style.display = 'none';
            oldPasswordInput.value = '';
            newPassword1Input.value = '';
            newPassword2Input.value = '';
        };

        savePasswordBtn.onclick = function () {
            var oldPassword = oldPasswordInput.value.trim();
            var newPassword1 = newPassword1Input.value.trim();
            var newPassword2 = newPassword2Input.value.trim();

            if (newPassword1 === '' || newPassword2 === '') {
                alert('Passwords cannot be empty!');
                return;
            }

            if (newPassword1 !== newPassword2) {
                alert('New passwords do not match!');
                return;
            }

            fetch('/profile/editprofile/changepassword/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    'old_password': oldPassword,
                    'new_password1': newPassword1,
                    'new_password2': newPassword2
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response not ok.');
                }
            })
            .then(data => {
                console.log('Password changed successfully:', data);
                alert('Password changed successfully!');
                passwordForm.style.display = 'none';
                oldPasswordInput.value = '';
                newPassword1Input.value = '';
                newPassword2Input.value = '';
                
            })
            .catch(error => {
                console.error('Error changing password:', error);
                alert('Error changing password. Please try again.');
            });
        };
    }

    if (privacySettingsBtn) {
        privacySettingsBtn.onclick = function () {
            var selectedPrivacy = prompt('Choose Privacy Setting:\n\n0. Public\n1. Friends Only\n2. Private');

            if (selectedPrivacy !== null) {
                var newPrivacyValue = parseInt(selectedPrivacy.trim());

                if ([0, 1, 2].includes(newPrivacyValue)) {
                    var formData = new FormData();
                    formData.append('privacy_value', newPrivacyValue);

                    fetch('/profile/editprofile/updateprivacy/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        } else {
                            throw new Error('Network response not ok.');
                        }
                    })
                    .then(data => {
                        console.log('Privacy updated successfully:', data);
                        alert('Privacy setting updated successfully!');
                    })
                    .catch(error => {
                        console.error('Error updating privacy:', error);
                        alert('Error updating privacy. Please try again.');
                    });
                } else {
                    alert('Invalid selection. Please choose 0, 1, or 2.');
                }
            } else {
                console.log('User cancelled privacy settings.');
            }
        };
    }
});