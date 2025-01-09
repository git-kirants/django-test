document.addEventListener('DOMContentLoaded', function() {
    // Handle star rating selection
    document.querySelectorAll('.rating-star').forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const form = this.closest('.rating-form');
            const stars = form.querySelectorAll('.rating-star');
            
            stars.forEach(s => {
                if (s.dataset.rating <= rating) {
                    s.classList.remove('text-gray-400');
                    s.classList.add('text-yellow-400');
                } else {
                    s.classList.remove('text-yellow-400');
                    s.classList.add('text-gray-400');
                }
            });
            
            form.dataset.selectedRating = rating;
        });
    });

    // Handle rating form submission
    document.querySelectorAll('.rating-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const bookingId = this.dataset.bookingId;
            const rating = this.dataset.selectedRating;
            const review = this.querySelector('textarea[name="review"]').value;
            
            if (!rating) {
                alert('Please select a rating');
                return;
            }
            
            const formData = new FormData();
            formData.append('rating', rating);
            formData.append('review', review);
            
            fetch(`/bookings/rate/${bookingId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken  // This will be defined in the template
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to submit rating');
            });
        });
    });
}); 