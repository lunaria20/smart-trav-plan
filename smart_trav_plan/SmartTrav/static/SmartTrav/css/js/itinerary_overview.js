/**
 * Toast Notification Function
 * Creates and displays a transient success notification.
 * @param {string} title - The main title of the toast.
 * @param {string} message - The detailed message of the toast.
 */
function showToast(title, message) {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = 'success-toast';
    toast.innerHTML = `
        <div class="success-icon">✓</div>
        <div class="toast-message">
            <div class="toast-title">${title}</div>
            <div class="toast-text">${message}</div>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        // Use a reverse animation class if defined in CSS, or manually transition
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Print Handler
 * Initiates the browser's print dialog and shows a toast notification.
 */
function handlePrint() {
    window.print();
    setTimeout(() => {
        showToast('Print Dialog Opened', 'Ready to print your itinerary.');
    }, 500);
}

