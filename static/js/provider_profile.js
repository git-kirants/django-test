document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.getElementById('id_logo');  // Using standard Django form ID
    const logoPreview = document.getElementById('logoPreview');

    logoInput.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                if (logoPreview.tagName === 'IMG') {
                    logoPreview.src = e.target.result;
                } else {
                    // Replace the placeholder div with an img
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.id = 'logoPreview';
                    img.className = 'w-32 h-32 object-contain bg-gray-50 rounded-lg';
                    img.alt = 'Business Logo';
                    logoPreview.parentNode.replaceChild(img, logoPreview);
                }
            };
            
            reader.readAsDataURL(e.target.files[0]);
        }
    });
}); 