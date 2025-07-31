// Job Description Analysis page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const resumeUploadArea = document.getElementById('resumeUploadArea');
    const jdUploadArea = document.getElementById('jdUploadArea');
    const resumeFile = document.getElementById('resumeFile');
    const jdFile = document.getElementById('jdFile');
    const resumeFileFallback = document.getElementById('resumeFileFallback');
    const jdFileFallback = document.getElementById('jdFileFallback');

    // Resume file change handler
    resumeFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            updateUploadArea(resumeUploadArea, file.name);
            // Also set the fallback input
            resumeFileFallback.files = e.target.files;
        }
    });

    // Fallback resume file input
    resumeFileFallback.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            updateUploadArea(resumeUploadArea, file.name);
            // Also set the main input
            resumeFile.files = e.target.files;
        }
    });

    // JD file change handler
    jdFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            updateUploadArea(jdUploadArea, file.name);
            // Also set the fallback input
            jdFileFallback.files = e.target.files;
        }
    });

    // Fallback JD file input
    jdFileFallback.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            updateUploadArea(jdUploadArea, file.name);
            // Also set the main input
            jdFile.files = e.target.files;
        }
    });

    // Drag and drop functionality
    [resumeUploadArea, jdUploadArea].forEach(area => {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.add('highlight'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, () => area.classList.remove('highlight'), false);
        });

        // Add drop event handler
        area.addEventListener('drop', handleDrop, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                // Determine which area was dropped on
                const targetArea = e.currentTarget;
                
                if (targetArea === resumeUploadArea) {
                    resumeFile.files = files;
                    resumeFileFallback.files = files;
                    updateUploadArea(resumeUploadArea, file.name);
                } else if (targetArea === jdUploadArea) {
                    jdFile.files = files;
                    jdFileFallback.files = files;
                    updateUploadArea(jdUploadArea, file.name);
                }
            } else {
                alert('Please select a PDF file only.');
            }
        }
    }

    function updateUploadArea(area, fileName) {
        area.innerHTML = `
            <i class="fas fa-check-circle upload-icon" style="color: #28a745;"></i>
            <h4>File Selected</h4>
            <p>${fileName}</p>
        `;
    }

    // Form submission validation
    document.getElementById('jdForm').addEventListener('submit', function(e) {
        const resumeFileInput = document.getElementById('resumeFile');
        const jdFileInput = document.getElementById('jdFile');
        const resumeTextInput = document.querySelector('textarea[name="jd_resume_text"]');
        const jdTextInput = document.querySelector('textarea[name="jd_text"]');
        
        const hasResumeInput = (resumeFileInput.files.length > 0) || (resumeTextInput.value.trim().length > 0);
        const hasJDInput = (jdFileInput.files.length > 0) || (jdTextInput.value.trim().length > 0);
        
        if (!hasResumeInput) {
            e.preventDefault();
            alert('Please provide resume text or upload a resume file.');
            return false;
        }
        
        if (!hasJDInput) {
            e.preventDefault();
            alert('Please provide job description text or upload a job description file.');
            return false;
        }
    });
}); 