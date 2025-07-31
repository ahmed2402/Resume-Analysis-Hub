// Job Description Result page JavaScript functionality

// Function to convert markdown-style text to HTML
function formatAnalysisText(text) {
    // Section headers: [Section] Name
    text = text.replace(/\[Section\] (.+)/g, '<div class="section-header">$1</div>');
    // Bullets: - Item
    text = text.replace(/^- (.*)$/gm, '<li>$1</li>');
    // Wrap consecutive <li> in <ul>
    text = text.replace(/((?:<li>.*?<\/li>\s*)+)/gs, function(match) {
        return '<ul>' + match + '</ul>';
    });
    // Remove extra <ul></ul>
    text = text.replace(/<ul>\s*<\/ul>/g, '');
    return text;
}

document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bar
    const progressFill = document.querySelector('.progress-fill');
    const width = progressFill.style.width;
    progressFill.style.width = '0%';
    setTimeout(() => {
        progressFill.style.width = width;
    }, 500);
    
    // Format analysis text
    const analysisContent = document.querySelector('.analysis-content');
    if (analysisContent) {
        const originalText = analysisContent.innerText;
        const formattedText = formatAnalysisText(originalText);
        analysisContent.innerHTML = formattedText;
    }
}); 