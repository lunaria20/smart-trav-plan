// --- GLOBAL VARIABLES ---
let currentDestinationId = null;
let deleteForm = null;

// --- DESTINATION MODAL FUNCTIONS ---
function openDestinationModal(id, name, location, description, category, priceRange, imageUrl) {
    currentDestinationId = id;

    // Populate Text Fields
    if(document.getElementById('modalDestinationName')) document.getElementById('modalDestinationName').textContent = name;
    if(document.getElementById('modalDestinationLocation')) document.getElementById('modalDestinationLocation').textContent = location;
    if(document.getElementById('modalDestinationDescription')) document.getElementById('modalDestinationDescription').textContent = description;

    // Category Label
    const catSpan = document.getElementById('modalDestinationCategory');
    if (catSpan) {
        catSpan.textContent = category;
    }

    // Price
    if(document.getElementById('modalDestinationPrice')) document.getElementById('modalDestinationPrice').textContent = '₱' + priceRange;

    // Update Save Form Action
    const saveForm = document.getElementById('modalSaveForm');
    if (saveForm) {
        saveForm.action = `/destination/save/${id}/`;
    }

    // Handle Image Display
    const imageContainer = document.getElementById('modalDestinationImage');
    if (imageContainer) {
        if (imageUrl && imageUrl !== 'None' && imageUrl !== '') {
            imageContainer.innerHTML = `<img src="${imageUrl}" style="width: 100%; height: 100%; object-fit: cover;">`;
        } else {
            imageContainer.innerHTML = '';
            // Default SmartTrav Gradient if no image
            imageContainer.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    }

    // Set Operating Hours Logic
    const operatingHours = {
        'restaurant': '10:00 AM - 10:00 PM',
        'resort': '24 Hours (Check-in: 2PM)',
        'beach': '6:00 AM - 6:00 PM',
        'attraction': '8:00 AM - 6:00 PM',
        'historical': '8:00 AM - 5:00 PM'
    };
    const hours = operatingHours[String(category).toLowerCase()] || '8:00 AM - 6:00 PM';
    if(document.getElementById('modalOperatingHours')) document.getElementById('modalOperatingHours').textContent = hours;

    // Set Amenities Logic
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

    // Show Modal
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

// --- DELETE MODAL FUNCTIONS ---
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

// --- PROFILE PICTURE PREVIEW ---
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

// --- CLOSE MODALS ON OUTSIDE CLICK ---
window.onclick = function(event) {
    const destModal = document.getElementById('destinationModal');
    const tripModal = document.getElementById('tripModal');
    const deleteModal = document.getElementById('deleteModal');

    if (event.target === destModal) closeDestinationModal();
    if (event.target === tripModal) closeTripModal();
    if (event.target === deleteModal) closeDeleteModal();
}

// --- MAIN INITIALIZATION & LOGIC ---
document.addEventListener('DOMContentLoaded', function() {

    // 1. Navigation Switching Logic
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

    // Handle URL parameters for direct section access
    const urlParams = new URLSearchParams(window.location.search);
    const sectionParam = urlParams.get('section');
    if (sectionParam) {
        showSection(sectionParam);
    }

    // ============================================================
    // 2. TAG CART LOGIC (Type -> Enter -> Add Tag -> Click Search)
    // ============================================================
    const tagInput = document.getElementById('tagInput');
    const tagsContainer = document.getElementById('tagsContainer');
    const hiddenInput = document.getElementById('hiddenTagsInput');

    // Array to store current tags
    let tags = [];

    // A. Initialize from existing hidden input (if page reloaded after search)
    if (hiddenInput && hiddenInput.value) {
        const existing = hiddenInput.value.split(',').map(t => t.trim()).filter(t => t);
        existing.forEach(tag => {
            if(tag) tags.push(tag.toLowerCase());
        });
        renderTags();
    }

    // B. Keydown Listener: Handle Enter Key
    if(tagInput) {
        tagInput.addEventListener('keydown', function(e) {
            // If user presses ENTER or COMMA
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault(); // <--- CRITICAL: Prevents form from submitting!

                const val = tagInput.value.trim().replace(',', '');
                if (val.length > 0) {
                    addTag(val);
                    tagInput.value = ''; // Clear input field
                }
            }
            // Handle Backspace (delete last tag if input is empty)
            else if (e.key === 'Backspace' && tagInput.value === '' && tags.length > 0) {
                removeTag(tags.length - 1);
            }
        });
    }

    // Helper: Add Tag to Array
    function addTag(text) {
        // Prevent duplicates
        if (tags.includes(text.toLowerCase())) return;
        tags.push(text.toLowerCase());
        renderTags();
        updateHiddenInput();
    }

    // Helper: Remove Tag from Array
    function removeTag(index) {
        tags.splice(index, 1);
        renderTags();
        updateHiddenInput();
    }

    // Helper: Render the Visual Pills
    function renderTags() {
        // Clear existing visual pills (but keep the input field logic safe)
        const existingPills = tagsContainer.querySelectorAll('.tag-pill');
        existingPills.forEach(p => p.remove());

        // Create new pills based on tags array
        tags.forEach((tag, index) => {
            const pill = document.createElement('div');
            pill.className = 'tag-pill';

            // Text + X button
            pill.innerHTML = `${tag} <span class="tag-remove">&times;</span>`;

            // Click listener for the X button
            pill.querySelector('.tag-remove').addEventListener('click', function(e) {
                e.stopPropagation(); // Stop click from bubbling up
                removeTag(index);
            });

            // Insert pill BEFORE the text input
            tagsContainer.insertBefore(pill, tagInput);
        });
    }

    // Helper: Update Hidden Input (Sent to Backend)
    function updateHiddenInput() {
        hiddenInput.value = tags.join(',');
    }
});

// --- HELPER FUNCTIONS ---

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

// --- NEW HELPER FUNCTIONS FOR NO TRIP MODAL ---
function closeNoTripModal() {
    const modal = document.getElementById('noTripModal');
    if (modal) modal.classList.remove('show');
}

function redirectToCreateTrip() {
    closeNoTripModal();
    // Switch to My Trips tab
    showSection('itineraries');
    // Scroll to top
    window.scrollTo(0, 0);
    // Open the creation form
    const form = document.getElementById('itinerary-form');
    if (form && (form.style.display === 'none' || form.style.display === '')) {
        toggleForm('itinerary-form');
    }
}

// --- UPDATED OPEN TRIP MODAL FUNCTION ---
function openTripModal(destinationId, destinationName) {
    // 1. Check if there are any trip radio buttons in the modal
    const tripOptions = document.querySelectorAll('#tripModal input[name="itinerary_id"]');

    if (tripOptions.length === 0) {
        // 2. TRIGGER THE CUSTOM MODAL instead of confirm()
        const noTripModal = document.getElementById('noTripModal');
        if (noTripModal) {
            noTripModal.classList.add('show');

            // Allow closing by clicking outside
            noTripModal.onclick = function(e) {
                if (e.target === noTripModal) closeNoTripModal();
            }
        }
        return;
    }

    // 3. Normal behavior if trips exist
    document.getElementById('destinationId').value = destinationId;
    document.getElementById('destinationName').textContent = destinationName;
    const modal = document.getElementById('tripModal');
    if(modal) modal.classList.add('show');
}

function closeTripModal() {
    const modal = document.getElementById('tripModal');
    if(modal) modal.classList.remove('show');
}

// --- DATE VALIDATION FOR TRIP CREATION ---
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];

    // 1. Target only 'start_date' inputs to avoid blocking expense dates
    const startDateInputs = document.querySelectorAll('input[name="start_date"]');

    startDateInputs.forEach(input => {
        // Set minimum date to today
        input.min = today;

        // 2. Add listener to update 'End Date' constraint automatically
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                const endDateInput = form.querySelector('input[name="end_date"]');
                if (endDateInput) {
                    // End date cannot be before start date
                    endDateInput.min = this.value;

                    // If current end date is invalid, clear it
                    if (endDateInput.value && endDateInput.value < this.value) {
                        endDateInput.value = this.value;
                    }
                }
            }
        });
    });
});