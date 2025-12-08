// Remove the preventDefault - let Django handle the form submission
// The form will now POST to the backend and Django will handle it

// Optional: Add form validation or loading states here if needed
document.getElementById('contactForm').addEventListener('submit', function(e) {
    // You can add a loading spinner here if you want
    const submitBtn = this.querySelector('.submit-btn');
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
});