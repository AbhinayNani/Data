document.addEventListener('DOMContentLoaded', () => {
    const fetchButton = document.getElementById('fetchLocation');
    const locationInput = document.getElementById('locationName');
    const locationDataDiv = document.getElementById('locationData');

    fetchButton.addEventListener('click', async () => {
        const locationName = encodeURIComponent(locationInput.value.trim()); // Get and encode the location name

        if (!locationName) {
            locationDataDiv.innerHTML = 'Please enter a location name.';
            return;
        }

        try {
            const response = await fetch(`/location/${locationName}`);
            if (response.ok) {
                const data = await response.json();   
                locationDataDiv.innerHTML = `Latitude: ${data.latitude}, Longitude: ${data.longitude}`;
            } else {
                locationDataDiv.innerHTML = 'Location not found or an error occurred.';
            }
        } catch (error) {
            locationDataDiv.innerHTML = 'An error occurred while fetching data.';
            console.error('Error fetching location data:', error);
        }
    });
});
