setTimeout(() => {
    let notifications = document.querySelectorAll(".alert");
    notifications.forEach(notification => {
        notification.style.display = "none";
    });
}, 2000);
