function openBookingModal(serviceId, serviceTitle) {
    document.getElementById('serviceId').value = serviceId;
    document.getElementById('modalTitle').textContent = `Book ${serviceTitle}`;
    document.getElementById('bookingModal').classList.remove('hidden');
}

function closeBookingModal() {
    document.getElementById('bookingModal').classList.add('hidden');
    document.getElementById('bookingForm').reset();
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('bookingForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = {
            service: formData.get('service'),
            booking_date: formData.get('booking_date'),
            special_requests: formData.get('special_requests')
        };

        try {
            const response = await fetch('/api/bookings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert('Booking submitted successfully!');
                closeBookingModal();
            } else {
                const errorData = await response.json();
                alert('Error: ' + (errorData.detail || 'Could not create booking'));
            }
        } catch (error) {
            alert('Error: Could not submit booking');
            console.error('Error:', error);
        }
    });
});

function loadBookings() {
    fetch('/api/bookings/')
        .then(response => response.json())
        .then(bookings => {
            const bookingsList = document.getElementById('bookingsList');
            if (!bookingsList) return;
            
            bookingsList.innerHTML = '';
            bookings.forEach(booking => {
                const template = document.getElementById('bookingTemplate');
                const bookingElement = template.content.cloneNode(true);
                
                bookingElement.querySelector('.service').textContent = booking.service.title;
                bookingElement.querySelector('.booking-date').textContent = 
                    new Date(booking.booking_date).toLocaleString();
                bookingElement.querySelector('.status').textContent = 
                    booking.status.charAt(0).toUpperCase() + booking.status.slice(1);
                
                // Add action buttons for providers
                const actions = bookingElement.querySelector('.provider-actions');
                if (booking.status === 'pending' && actions) {
                    actions.classList.remove('hidden');
                    actions.querySelector('.accept-btn').onclick = () => updateBookingStatus(booking.id, 'accept');
                    actions.querySelector('.reject-btn').onclick = () => updateBookingStatus(booking.id, 'reject');
                }
                
                bookingsList.appendChild(bookingElement);
            });
        })
        .catch(error => console.error('Error loading bookings:', error));
}

function updateBookingStatus(bookingId, action) {
    fetch(`/api/bookings/${bookingId}/${action}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.ok) {
            loadBookings(); // Refresh the list
        } else {
            throw new Error('Failed to update booking');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update booking status');
    });
}

// Auto-refresh bookings list if we're on the status page
if (document.getElementById('bookingsList')) {
    loadBookings();
    setInterval(loadBookings, 30000); // Refresh every 30 seconds
} 