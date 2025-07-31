// Resume Result page JavaScript functionality

// Add animation to confidence bars
document.addEventListener('DOMContentLoaded', function() {
    const confidenceBars = document.querySelectorAll('.confidence-fill');
    confidenceBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}); 