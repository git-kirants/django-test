document.addEventListener('DOMContentLoaded', function() {
    let currentSlide = 0;
    let slides = [];

    // Make openServiceModal available globally
    window.openServiceModal = function(serviceId) {
        fetch(`/services/services/${serviceId}/details/`)
            .then(response => response.json())
            .then(data => {
                const modal = document.getElementById('serviceModal');
                const detailsContainer = document.getElementById('serviceDetails');
                const carousel = document.getElementById('serviceImageCarousel');
                
                // Set up images for carousel
                slides = [data.image, ...data.additional_images].filter(Boolean);
                currentSlide = 0;
                updateCarousel();

                // Create the rating stars HTML
                const ratingStars = Array(5).fill('').map((_, index) => {
                    const filled = index < Math.floor(data.average_rating);
                    return `<svg class="w-5 h-5 ${filled ? 'text-yellow-400' : 'text-gray-300'}" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>`;
                }).join('');

                // Populate service details
                detailsContainer.innerHTML = `
                    <div class="flex justify-between items-start mb-6">
                        <h2 class="text-3xl font-bold text-gray-900">${data.title}</h2>
                        ${data.permissions.can_change_availability ? `
                            <button onclick="toggleAvailability(${data.id}, ${!data.is_available})" 
                                    class="px-4 py-2 rounded-lg ${data.is_available ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-green-100 text-green-700 hover:bg-green-200'}">
                                ${data.is_available ? 'Mark Unavailable' : 'Mark Available'}
                            </button>
                        ` : ''}
                    </div>

                    <!-- Enquiry Section -->
                    ${data.gardener.phone ? `
                        <div class="bg-green-50 rounded-xl p-4 mb-6 border border-green-200">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center">
                                    <svg class="w-6 h-6 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                    </svg>
                                    <div>
                                        <p class="text-green-800 font-medium">For Enquiries</p>
                                        <a href="tel:${data.gardener.phone}" class="text-green-600 text-lg font-semibold hover:text-green-700 transition-colors">
                                            ${data.gardener.phone}
                                        </a>
                                    </div>
                                </div>
                                <a href="tel:${data.gardener.phone}" 
                                   class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors inline-flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                    </svg>
                                    Call Now
                                </a>
                            </div>
                        </div>
                    ` : ''}

                    <div class="flex items-center mb-6">
                        <span class="text-2xl font-bold text-green-600">$${data.price}</span>
                        <span class="mx-4 text-gray-400">|</span>
                        <span class="text-gray-600">${data.duration} minutes</span>
                        <span class="mx-4 text-gray-400">|</span>
                        <span class="text-gray-600">${data.category}</span>
                    </div>

                    <div class="flex items-center mb-6">
                        <div class="flex items-center">
                            ${ratingStars}
                        </div>
                        <span class="ml-2 text-sm text-gray-600">
                            ${data.average_rating > 0 
                                ? `${data.average_rating.toFixed(1)} (${data.total_ratings} review${data.total_ratings !== 1 ? 's' : ''})`
                                : 'No reviews yet'}
                        </span>
                    </div>
                    
                    <div class="prose max-w-none mb-8">
                        <h3 class="text-xl font-semibold mb-2">Description</h3>
                        <p>${data.description}</p>
                    </div>

<div class="border-t pt-6">
    <h3 class="text-xl font-semibold mb-4">Service Provider</h3>
    <div class="flex items-center justify-between">
        <div>
            <a href="/users/provider/${data.gardener.id}/" class="font-medium text-gray-900 hover:text-green-600 transition-colors">
                ${data.gardener.business_name || data.gardener.name}
            </a>
            <p class="text-gray-600 mt-1">${data.gardener.description || ''}</p>
        </div>
    </div>
</div>

                    <div class="mt-8 flex gap-4">
                        <button onclick="closeServiceModal()" 
                                class="flex-1 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200">
                            Close
                        </button>
                        ${data.permissions.can_edit ? `
                            <a href="/services/update/${data.id}/" 
                               class="flex-1 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 text-center">
                                Edit Service
                            </a>
                        ` : data.can_book ? `
                            <a href="/bookings/create/${data.id}/" 
                               class="flex-1 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 text-center">
                                Book Now
                            </a>
                        ` : ''}
                    </div>
                `;

                modal.classList.remove('hidden');
            });
    };

    window.closeServiceModal = function() {
        document.getElementById('serviceModal').classList.add('hidden');
    };

    function updateCarousel() {
        const carousel = document.getElementById('serviceImageCarousel');
        if (slides.length > 0) {
            carousel.innerHTML = `
                <img src="${slides[currentSlide]}" 
                     class="w-full h-full object-cover" 
                     alt="Service image ${currentSlide + 1}">
            `;
        }
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateCarousel();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateCarousel();
    }

    // Event listeners for carousel controls
    document.getElementById('nextButton').addEventListener('click', nextSlide);
    document.getElementById('prevButton').addEventListener('click', prevSlide);
}); 
function openServiceModal(serviceId) {
    fetch(`/services/services/${serviceId}/details/`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('serviceModal');
            const detailsContainer = document.getElementById('serviceDetails');
            
            // Create the rating stars HTML
            const ratingStars = Array(5).fill('').map((_, index) => {
                const filled = index < Math.floor(data.average_rating);
                return `<svg class="w-5 h-5 ${filled ? 'text-yellow-400' : 'text-gray-300'}" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>`;
            }).join('');

            detailsContainer.innerHTML = `
                <div class="flex justify-between items-start mb-6">
                    <h2 class="text-3xl font-bold text-gray-900">${data.title}</h2>
                    ${data.permissions.can_change_availability ? `
                        <button onclick="toggleAvailability(${data.id}, ${!data.is_available})" 
                                class="px-4 py-2 rounded-lg ${data.is_available ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-green-100 text-green-700 hover:bg-green-200'}">
                            ${data.is_available ? 'Mark Unavailable' : 'Mark Available'}
                        </button>
                    ` : ''}
                </div>

                <!-- Enquiry Section -->
                ${data.gardener.phone ? `
                    <div class="bg-green-50 rounded-xl p-4 mb-6 border border-green-200">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <svg class="w-6 h-6 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                </svg>
                                <div>
                                    <p class="text-green-800 font-medium">For Enquiries</p>
                                    <a href="tel:${data.gardener.phone}" class="text-green-600 text-lg font-semibold hover:text-green-700 transition-colors">
                                        ${data.gardener.phone}
                                    </a>
                                </div>
                            </div>
                            <a href="tel:${data.gardener.phone}" 
                               class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors inline-flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                </svg>
                                Call Now
                            </a>
                        </div>
                    </div>
                ` : ''}

                <div class="flex items-center mb-6">
                    <span class="text-2xl font-bold text-green-600">$${data.price}</span>
                    <span class="mx-4 text-gray-400">|</span>
                    <span class="text-gray-600">${data.duration} minutes</span>
                    <span class="mx-4 text-gray-400">|</span>
                    <span class="text-gray-600">${data.category}</span>
                </div>

                <div class="flex items-center mb-6">
                    <div class="flex items-center">
                        ${ratingStars}
                    </div>
                    <span class="ml-2 text-sm text-gray-600">
                        ${data.average_rating > 0 
                            ? `${data.average_rating.toFixed(1)} (${data.total_ratings} review${data.total_ratings !== 1 ? 's' : ''})`
                            : 'No reviews yet'}
                    </span>
                </div>

                <div class="prose max-w-none mb-8">
                    <h3 class="text-xl font-semibold mb-2">Description</h3>
                    <p>${data.description}</p>
                </div>

                <div class="border-t pt-6">
                    <h3 class="text-xl font-semibold mb-4">Service Provider</h3>
                    <div class="flex items-center justify-between">
                        <div>
                            <a href="/provider-details/${data.gardener.id}/" class="font-medium text-gray-900 hover:text-green-600 transition-colors">
                                ${data.gardener.business_name || data.gardener.name}
                            </a>
                            <p class="text-gray-600 mt-1">${data.gardener.description || ''}</p>
                        </div>
                    </div>
                </div>

                <div class="mt-8 flex gap-4">
                    <button onclick="closeServiceModal()" 
                            class="flex-1 px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200">
                        Close
                    </button>
                    ${data.permissions.can_edit ? `
                        <a href="/services/update/${data.id}/" 
                           class="flex-1 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 text-center">
                            Edit Service
                        </a>
                    ` : data.can_book ? `
                        <a href="/bookings/create/${data.id}/" 
                           class="flex-1 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 text-center">
                            Book Now
                        </a>
                    ` : ''}
                </div>
            `;

            modal.classList.remove('hidden');
        });
}

function closeServiceModal() {
    document.getElementById('serviceModal').classList.add('hidden');
}

function updateCarousel() {
    const carousel = document.getElementById('serviceImageCarousel');
    if (slides.length > 0) {
        carousel.innerHTML = `
            <img src="${slides[currentSlide]}" 
                 class="w-full h-full object-cover" 
                 alt="Service image ${currentSlide + 1}">
        `;
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    updateCarousel();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    updateCarousel();
}

// Event listeners for carousel controls
document.getElementById('nextButton').addEventListener('click', nextSlide);
document.getElementById('prevButton').addEventListener('click', prevSlide); 

// Add function to toggle availability
function toggleAvailability(serviceId, newStatus) {
    fetch(`/services/toggle-availability/${serviceId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ is_available: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            openServiceModal(serviceId); // Refresh the modal
        }
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 