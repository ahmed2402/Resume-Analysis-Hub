// Job Description Result page JavaScript functionality

// Animate progress bar on page load
document.addEventListener('DOMContentLoaded', function() {
    const progressFill = document.querySelector('.progress-fill');
    const width = progressFill.style.width;
    progressFill.style.width = '0%';
    setTimeout(() => {
        progressFill.style.width = width;
    }, 500);
}); 