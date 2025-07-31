// Home page JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.feature-button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}); 