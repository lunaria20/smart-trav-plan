// Destination Modal Functions
let currentDestinationId = null;

function openDestinationModal(id, name, location, description, category, priceRange) {
    currentDestinationId = id;

    document.getElementById('modalDestinationName').textContent = name;
    document.getElementById('modalDestinationLocation').textContent = location;
    document.getElementById('modalDestinationDescription').textContent = description;
    document.getElementById('modalDestinationCategory').textContent = category;
    document.getElementById('modalDestinationPrice').textContent = '₱' + priceRange;

    // Update save form action
    document.getElementById('modalSaveForm').action = `/destination/save/${id}/`;

    // Set operating hours based on category
    const operatingHours = {
        'restaurant': '10:00 AM - 10:00 PM',
        'resort': '24 Hours (Check-in: 2PM)',
        'beach': '6:00 AM - 6:00 PM',
        'attraction': '8:00 AM - 6:00 PM',
        'historical': '8:00 AM - 5:00 PM'
    };
    document.getElementById('modalOperatingHours').textContent = operatingHours[category] || '8:00 AM - 6:00 PM';

    // Set amenities based on category
    const amenitiesMap = {
        'resort': ['🏊 Swimming Pool', '🍽 Restaurant', '📶 Free WiFi', '🅿 Parking', '🏖 Beach Access', '💆 Spa Services'],
        'beach': ['🏖 Beach Access', '🚿 Shower Facilities', '🏪 Nearby Stores', '🅿 Parking', '🏐 Beach Volleyball', '🏊 Lifeguard'],
        'restaurant': ['🍽 Dine-in', '🥡 Take-out', '🚗 Delivery', '❄ Air-conditioned', '👨‍👩‍👧‍👦 Family-friendly', '💳 Card Payment'],
        'historical': ['📷 Photo Spots', '👥 Guided Tours', '🏛 Museum', '🅿 Parking', '♿ Accessible', '🚻 Restrooms'],
        'attraction': ['🎫 Ticketing', '🅿 Parking', '🚻 Restrooms', '🎁 Gift Shop', '📷 Photo Spots', '♿ Accessible']
    };

    const amenities = amenitiesMap[category] || amenitiesMap['attraction'];
    const amenitiesHTML = amenities.map(amenity =>
        `<div style="display: flex; align-items: center; color: #4a5568; font-size: 0.95rem; font-weight: 500;">${amenity}</div>`
    ).join('');

    document.getElementById('modalAmenities').innerHTML = amenitiesHTML;
    document.getElementById('modalAmenitiesTitle').textContent = category === 'restaurant' ? 'Features' : 'Amenities';

    document.getElementById('destinationModal').classList.add('show');
}

function closeDestinationModal() {
    document.getElementById('destinationModal').classList.remove('show');
}

function addToTripFromModal() {
    if (currentDestinationId) {
        closeDestinationModal();
        const destName = document.getElementById('modalDestinationName').textContent;
        openTripModal(currentDestinationId, destName);
    }
}

// Delete Modal Functions
let deleteForm = null;

function openDeleteModal(tripName, formElement) {
    document.getElementById('deleteItemName').textContent = tripName;
    deleteForm = formElement;
    document.getElementById('deleteModal').classList.add('show');
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('show');
    deleteForm = null;
}

function confirmDelete() {
    if (deleteForm) {
        deleteForm.submit();
    }
    closeDeleteModal();
}

// Preview uploaded image before saving
function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const display = document.getElementById('profilePictureDisplay');
            const initial = document.getElementById('profileInitial');
            const existingImg = document.getElementById('profileImage');

            if (existingImg) {
                existingImg.src = e.target.result;
            } else {
                if (initial) {
                    initial.style.display = 'none';
                }
                const img = document.createElement('img');
                img.id = 'profileImage';
                img.src = e.target.result;
                img.alt = 'Profile Picture';
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.objectFit = 'cover';
                display.appendChild(img);
            }
        };
        reader.readAsDataURL(file);
    }
}

// Remove profile picture
function removeProfilePicture() {
    if (confirm('Are you sure you want to remove your profile picture?')) {
        // Create a form to submit the removal
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/remove-profile-picture/'; // Update this URL to match your Django URL

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;

        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
    }
}

// Close modals when clicking outside
document.getElementById('deleteModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeDeleteModal();
    }
});

document.getElementById('destinationModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeDestinationModal();
    }
});

document.getElementById('tripModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeTripModal();
    }
});

// Menu link functionality
document.querySelectorAll('.menu-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const section = this.getAttribute('data-section');
        showSection(section);

        document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
    const activeLink = document.querySelector(`.menu-link[data-section="${sectionId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
    }
}

function openTripModal(destinationId, destinationName) {
    document.getElementById('destinationId').value = destinationId;
    document.getElementById('destinationName').textContent = destinationName;
    document.getElementById('tripModal').classList.add('show');
}

function closeTripModal() {
    document.getElementById('tripModal').classList.remove('show');
}

// Initialize the page - Show the correct section on load
document.addEventListener('DOMContentLoaded', function() {
    // Get the active section from the template variable or default to 'overview'
    const urlParams = new URLSearchParams(window.location.search);
    const sectionParam = urlParams.get('section');

    // Try to get from URL parameter, then from template variable, then default to 'overview'
    let initialSection = sectionParam || 'overview';

    // Check if there's a template variable (this will be replaced by Django)
    const templateSection = "{{ active_section|default:'overview' }}";
    if (templateSection && templateSection !== "{{ active_section|default:'overview' }}") {
        initialSection = templateSection;
    }

    // Show the initial section
    showSection(initialSection);
});