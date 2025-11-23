// Page exit animation
function animateExit(url) {
    document.body.classList.add("page-exit");
    setTimeout(() => {
        window.location.href = url;
    }, 500);
}

// Scroll animation
window.addEventListener("scroll", () => {
    document.querySelectorAll(".card").forEach(card => {
        if (card.getBoundingClientRect().top < window.innerHeight - 50) {
            card.classList.add("show");
        }
    });
});
