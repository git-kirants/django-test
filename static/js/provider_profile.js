document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.querySelector('input[type="file"]');
    const logoError = document.getElementById('logoError');
    const form = document.querySelector('form');
    const submitButton = document.getElementById('submitButton');

    function validateImage(file) {
        // Check if a file was selected
        if (!file) return true;

        // Check file type
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            logoError.classList.remove('hidden');
            return false;
        }

        // Check file size (max 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (file.size > maxSize) {
            logoError.textContent = 'File size must be less than 5MB';
            logoError.classList.remove('hidden');
            return false;
        }

        logoError.classList.add('hidden');
        return true;
    }

    // Validate on file selection
    logoInput.addEventListener('change', function(e) {
        validateImage(this.files[0]);
    });

    // Validate before form submission
    form.addEventListener('submit', function(e) {
        if (logoInput.files.length > 0 && !validateImage(logoInput.files[0])) {
            e.preventDefault();
        }
    });
}); 