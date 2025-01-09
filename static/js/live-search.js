document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const servicesGrid = document.querySelector('#services-grid');
    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        // Add loading state
        servicesGrid.classList.add('opacity-50');
        
        // Debounce the search to prevent too many requests
        searchTimeout = setTimeout(() => {
            const searchQuery = this.value;
            
            // Fetch filtered results
            fetch(`/services/search/?search=${encodeURIComponent(searchQuery)}`)
                .then(response => response.text())
                .then(html => {
                    servicesGrid.innerHTML = html;
                    servicesGrid.classList.remove('opacity-50');
                })
                .catch(error => {
                    console.error('Error:', error);
                    servicesGrid.classList.remove('opacity-50');
                });
        }, 300); // Wait 300ms after user stops typing
    });
}); 