document.addEventListener('DOMContentLoaded', function() {
    // Function to handle "None" checkbox logic
    function handleNoneCheckbox(noneId, groupName, otherDivClass) {
        const noneCheckbox = document.getElementById(noneId);
        const otherCheckboxes = document.querySelectorAll(`input[name="${groupName}"]:not(#${noneId})`);
        const otherDiv = document.querySelector(`.${otherDivClass}`);

        if (noneCheckbox) {
            noneCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    otherCheckboxes.forEach(cb => cb.checked = false);
                    if (otherDiv) otherDiv.style.display = 'none';
                }
            });

            otherCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    if (this.checked) {
                        noneCheckbox.checked = false;
                        if (otherDiv) otherDiv.style.display = 'block';
                    }
                    // Hide other div if no checkboxes are checked
                    const anyChecked = Array.from(otherCheckboxes).some(cb => cb.checked);
                    if (!anyChecked && otherDiv) otherDiv.style.display = 'none';
                });
            });
        }
    }

    // Initialize checkbox handlers for each section
    handleNoneCheckbox('allergy_none', 'allergies', 'other-allergies');
    handleNoneCheckbox('history_none', 'medical_history', 'other-medical-history');
    handleNoneCheckbox('family_none', 'family_history', 'other-family-history');
    handleNoneCheckbox('risk_none', 'risk_assessment', 'pwd-details');

    // Special handler for PWD checkbox
    const pwdCheckbox = document.getElementById('pwd');
    const pwdDetails = document.querySelector('.pwd-details');
    if (pwdCheckbox && pwdDetails) {
        pwdCheckbox.addEventListener('change', function() {
            pwdDetails.style.display = this.checked ? 'block' : 'none';
        });
    }

    // Add this to your existing DOMContentLoaded event listener
    const contactInput = document.getElementById('parent_guardian_contact');
    if (contactInput) {
        contactInput.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Remove any non-numeric characters
            value = value.replace(/[^0-9]/g, '');
            
            // Ensure it starts with '09'
            if (value.length >= 2 && !value.startsWith('09')) {
                value = '09' + value.slice(2);
            }
            
            // Limit to 11 digits
            value = value.slice(0, 11);
            
            // Update input value
            e.target.value = value;
        });
    }
});