// Destination Modal Functions
let currentDestinationId = null;

function openDestinationModal(id, name, location, description, category, priceRange, imageUrl) {
    currentDestinationId = id;

    // Safety checks for elements
    if(document.getElementById('modalDestinationName')) document.getElementById('modalDestinationName').textContent = name;
    if(document.getElementById('modalDestinationLocation')) document.getElementById('modalDestinationLocation').textContent = location;
    if(document.getElementById('modalDestinationDescription')) document.getElementById('modalDestinationDescription').textContent = description;

    // SAFETY CHECK: This is what was crashing before!
    const catSpan = document.getElementById('modalDestinationCategory');
    if (catSpan) {
        catSpan.textContent = category;
    }

    if(document.getElementById('modalDestinationPrice')) document.getElementById('modalDestinationPrice').textContent = '₱' + priceRange;

    // Update save form action
    const saveForm = document.getElementById('modalSaveForm');
    if (saveForm) {
        saveForm.action = `/destination/save/${id}/`;
    }

    // Handle the Modal Image
    const imageContainer = document.getElementById('modalDestinationImage');
    if (imageContainer) {
        if (imageUrl && imageUrl !== 'None' && imageUrl !== '') {
            imageContainer.innerHTML = `<img src="${imageUrl}" style="width: 100%; height: 100%; object-fit: cover;">`;
        } else {
            imageContainer.innerHTML = '';
            imageContainer.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    // Set operating hours
    const operatingHours = {
        'restaurant': '10:00 AM - 10:00 PM',
        'resort': '24 Hours (Check-in: 2PM)',
        'beach': '6:00 AM - 6:00 PM',
        'attraction': '8:00 AM - 6:00 PM',
        'historical': '8:00 AM - 5:00 PM'
    };
    const hours = operatingHours[String(category).toLowerCase()] || '8:00 AM - 6:00 PM';
    if(document.getElementById('modalOperatingHours')) document.getElementById('modalOperatingHours').textContent = hours;

    // Set amenities
    const amenitiesMap = {
        'resort': ['🏊 Swimming Pool', '🍽 Restaurant', '📶 Free WiFi', '🅿 Parking', '🏖 Beach Access', '💆 Spa Services'],
        'beach': ['🏖 Beach Access', '🚿 Shower Facilities', '🏪 Nearby Stores', '🅿 Parking', '🏐 Beach Volleyball', '🏊 Lifeguard'],
        'restaurant': ['🍽 Dine-in', '🥡 Take-out', '🚗 Delivery', '❄ Air-conditioned', '👨‍👩‍👧‍👦 Family-friendly', '💳 Card Payment'],
        'historical': ['📷 Photo Spots', '👥 Guided Tours', '🏛 Museum', '🅿 Parking', '♿ Accessible', '🚻 Restrooms'],
        'attraction': ['🎫 Ticketing', '🅿 Parking', '🚻 Restrooms', '🎁 Gift Shop', '📷 Photo Spots', '♿ Accessible']
    };

    const key = String(category).toLowerCase();
    const amenities = amenitiesMap[key] || amenitiesMap['attraction'];
    const amenitiesHTML = amenities.map(amenity =>
        `<div style="display: flex; align-items: center; color: #4a5568; font-size: 0.95rem; font-weight: 500;">${amenity}</div>`
    ).join('');

    const amenitiesContainer = document.getElementById('modalAmenities');
    if(amenitiesContainer) amenitiesContainer.innerHTML = amenitiesHTML;

    if(document.getElementById('modalAmenitiesTitle')) {
        document.getElementById('modalAmenitiesTitle').textContent = key === 'restaurant' ? 'Features' : 'Amenities';
    }

    const modal = document.getElementById('destinationModal');
    if(modal) modal.classList.add('show');
}

function closeDestinationModal() {
    const modal = document.getElementById('destinationModal');
    if(modal) modal.classList.remove('show');
}

function addToTripFromModal() {
    if (currentDestinationId) {
        closeDestinationModal();
        const nameElem = document.getElementById('modalDestinationName');
        const destName = nameElem ? nameElem.textContent : 'Destination';
        openTripModal(currentDestinationId, destName);
    }
}

// Delete Modal Functions
let deleteForm = null;

function openDeleteModal(tripName, formElement) {
    if(document.getElementById('deleteItemName')) document.getElementById('deleteItemName').textContent = tripName;
    deleteForm = formElement;
    const modal = document.getElementById('deleteModal');
    if(modal) modal.classList.add('show');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if(modal) modal.classList.remove('show');
    deleteForm = null;
}

function confirmDelete() {
    if (deleteForm) {
        deleteForm.submit();
    }
    closeDeleteModal();
}

// Preview uploaded image
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
                if (initial) initial.style.display = 'none';
                if (display) {
                    const img = document.createElement('img');
                    img.id = 'profileImage';
                    img.src = e.target.result;
                    img.alt = 'Profile Picture';
                    img.style.width = '100%';
                    img.style.height = '100%';
                    img.style.objectFit = 'cover';
                    display.appendChild(img);
                }
            }
        };
        reader.readAsDataURL(file);
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    const destModal = document.getElementById('destinationModal');
    const tripModal = document.getElementById('tripModal');
    const deleteModal = document.getElementById('deleteModal');

    if (event.target === destModal) closeDestinationModal();
    if (event.target === tripModal) closeTripModal();
    if (event.target === deleteModal) closeDeleteModal();
}

// Navigation Logic
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.menu-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Only handle section switching if data-section exists
            if (this.getAttribute('data-section')) {
                e.preventDefault();
                const section = this.getAttribute('data-section');
                showSection(section);
            }
        });
    });

    const urlParams = new URLSearchParams(window.location.search);
    const sectionParam = urlParams.get('section');
    if (sectionParam) {
        showSection(sectionParam);
    }
});

function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
        setTimeout(() => targetSection.classList.add('active'), 10);
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
        form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
    }
}

function openTripModal(destinationId, destinationName) {
    document.getElementById('destinationId').value = destinationId;
    document.getElementById('destinationName').textContent = destinationName;
    const modal = document.getElementById('tripModal');
    if(modal) modal.classList.add('show');
}

function closeTripModal() {
    const modal = document.getElementById('tripModal');
    if(modal) modal.classList.remove('show');
}