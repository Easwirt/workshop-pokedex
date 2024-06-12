document.addEventListener("DOMContentLoaded", function() {
    const itemsPerPage = 4;

    let currentAchievementPage = 1;
    const achievementCards = document.querySelectorAll(".achievement-card");
    const totalAchievementPages = Math.ceil(achievementCards.length / itemsPerPage);
    const achievementNavigation = document.getElementById("achievement-navigation");

    
    if (achievementCards.length <= itemsPerPage) {
        achievementNavigation.style.display = 'none';
    } else {
        achievementNavigation.style.display = 'flex';
    }

    function showAchievementPage(page) {
        achievementCards.forEach((card, index) => {
            card.style.display = (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) ? 'block' : 'none';
        });
    }

    document.getElementById("next-page-achievement").addEventListener("click", function() {
        if (currentAchievementPage < totalAchievementPages) {
            currentAchievementPage++;
            showAchievementPage(currentAchievementPage);
        }
    });

    document.getElementById("prev-page-achievement").addEventListener("click", function() {
        if (currentAchievementPage > 1) {
            currentAchievementPage--;
            showAchievementPage(currentAchievementPage);
        }
    });

    showAchievementPage(currentAchievementPage);

    let currentFriendsPage = 1;
    const friendCards = document.querySelectorAll(".friend-card");
    const totalFriendsPages = Math.ceil(friendCards.length / itemsPerPage);
    const friendsNavigation = document.getElementById("friends-navigation");

    if (friendCards.length <= itemsPerPage) {
        friendsNavigation.style.display = 'none';
    } else {
        friendsNavigation.style.display = 'flex';
    }

    function showFriendsPage(page) {
        friendCards.forEach((card, index) => {
            card.style.display = (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) ? 'block' : 'none';
        });
    }

    document.getElementById("next-page-friends").addEventListener("click", function() {
        if (currentFriendsPage < totalFriendsPages) {
            currentFriendsPage++;
            showFriendsPage(currentFriendsPage);
        }
    });
    
    document.getElementById("prev-page-friends").addEventListener("click", function() {
        if (currentFriendsPage > 1) {
            currentFriendsPage--;
            showFriendsPage(currentFriendsPage);
        }
    });

    showFriendsPage(currentFriendsPage);
});