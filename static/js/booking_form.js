document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0] + 'T00:00';
    document.getElementById('booking_date').setAttribute('min', tomorrowStr);

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
                window.location.href = bookingsUrl; // This will be defined in the template
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