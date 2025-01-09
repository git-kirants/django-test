// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing mobile menu...');
    
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuButtons = document.querySelectorAll('.mobile-menu-button');
    
    // Debug elements found
    console.log('Mobile menu element:', mobileMenu);
    console.log('Mobile menu buttons found:', mobileMenuButtons.length);
    
    if (mobileMenu && mobileMenuButtons.length) {
        // Handle menu toggle
        function toggleMenu(show) {
            console.log('Toggling menu:', show ? 'show' : 'hide');
            if (show) {
                mobileMenu.classList.remove('translate-x-full');
                document.body.style.overflow = 'hidden';
                console.log('Menu opened, classes:', mobileMenu.className);
            } else {
                mobileMenu.classList.add('translate-x-full');
                document.body.style.overflow = '';
                console.log('Menu closed, classes:', mobileMenu.className);
            }
        }

        // Toggle menu for all menu buttons
        mobileMenuButtons.forEach((button, index) => {
            console.log(`Setting up button ${index + 1}`);
            button.addEventListener('click', (e) => {
                console.log(`Button ${index + 1} clicked`);
                e.stopPropagation();
                const isHidden = mobileMenu.classList.contains('translate-x-full');
                console.log('Menu is currently hidden:', isHidden);
                toggleMenu(isHidden);
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            console.log('Document clicked, target:', e.target);
            if (!mobileMenu.contains(e.target) || e.target.closest('.mobile-menu-button')) {
                console.log('Closing menu from outside click');
                toggleMenu(false);
            }
        });

        // Prevent clicks inside menu from closing it
        mobileMenu.addEventListener('click', (e) => {
            if (!e.target.closest('.mobile-menu-button')) {
                console.log('Click inside menu, preventing propagation');
                e.stopPropagation();
            }
        });
        
        console.log('Mobile menu initialization complete');
    } else {
        console.error('Mobile menu elements not found:', {
            menuFound: !!mobileMenu,
            buttonsFound: mobileMenuButtons.length
        });
    }
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.message);
    console.error('Error details:', {
        filename: e.filename,
        lineno: e.lineno,
        colno: e.colno,
        error: e.error
    });
}); 