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