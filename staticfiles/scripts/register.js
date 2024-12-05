document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.sign-up-form');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const idNumber = document.getElementById('idNumber');
    const email = document.getElementById('email');
    const firstName = document.getElementById('firstName');
    const middleInitial = document.getElementById('middleInitial');
    const lastName = document.getElementById('lastName');

    // Password validation function
    function validatePassword() {
        const passwordValue = password.value;
        const rules = {
            length: passwordValue.length >= 8,
            uppercase: /[A-Z]/.test(passwordValue),
            lowercase: /[a-z]/.test(passwordValue),
            number: /[0-9]/.test(passwordValue),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(passwordValue)
        };

        // Update validation UI
        document.querySelectorAll('#passwordValidation li').forEach((li, index) => {
            const rule = Object.values(rules)[index];
            li.style.color = rule ? 'green' : 'red';
        });

        return Object.values(rules).every(rule => rule);
    }

    // Real-time password validation
    password.addEventListener('input', validatePassword);

    // Real-time First Name validation
    firstName.addEventListener('input', function() {
        if (firstName.value.length < 2) {
            firstName.classList.add('error');
        } else {
            firstName.classList.remove('error');
        }
    });

    // Real-time Middle Initial validation
    middleInitial.addEventListener('input', function() {
        if (middleInitial.value.length !== 1) {
            middleInitial.classList.add('error');
        } else {
            middleInitial.classList.remove('error');
        }
    });

    // Real-time Last Name validation
    lastName.addEventListener('input', function() {
        if (lastName.value.length < 2) {
            lastName.classList.add('error');
        } else {
            lastName.classList.remove('error');
        }
    });

    // Real-time ID Number validation
    idNumber.addEventListener('input', function() {
        if (!/^\d{7}$/.test(idNumber.value)) {
            idNumber.classList.add('error');
        } else {
            idNumber.classList.remove('error');
        }
    });

    // Real-time Email validation
    email.addEventListener('input', function() {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            email.classList.add('error');
        } else {
            email.classList.remove('error');
        }
    });

    // Real-time Confirm Password validation
    confirmPassword.addEventListener('input', function() {
        if (password.value !== confirmPassword.value) {
            confirmPassword.classList.add('error');
        } else {
            confirmPassword.classList.remove('error');
        }
    });

    // Form submission handler
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        let isValid = true;
        let errorMessage = '';

        // First Name validation
        if (firstName.value.length < 2) {
            isValid = false;
            errorMessage += 'First name must be at least 2 characters long\n';
            firstName.classList.add('error');
        } else {
            firstName.classList.remove('error');
        }

        // Middle Initial validation
        if (middleInitial.value.length !== 1) {
            isValid = false;
            errorMessage += 'Middle initial must be exactly 1 character\n';
            middleInitial.classList.add('error');
        } else {
            middleInitial.classList.remove('error');
        }

        // Last Name validation
        if (lastName.value.length < 2) {
            isValid = false;
            errorMessage += 'Last name must be at least 2 characters long\n';
            lastName.classList.add('error');
        } else {
            lastName.classList.remove('error');
        }

        // ID Number validation
        if (!/^\d{7}$/.test(idNumber.value)) {
            isValid = false;
            errorMessage += 'ID Number must be exactly 7 digits\n';
            idNumber.classList.add('error');
        } else {
            idNumber.classList.remove('error');
        }

        // Email validation
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            isValid = false;
            errorMessage += 'Please enter a valid email address\n';
            email.classList.add('error');
        } else {
            email.classList.remove('error');
        }

        // Password validation
        if (!validatePassword()) {
            isValid = false;
            errorMessage += 'Password does not meet requirements\n';
            password.classList.add('error');
        } else {
            password.classList.remove('error');
        }

        // Confirm Password validation
        if (password.value !== confirmPassword.value) {
            isValid = false;
            errorMessage += 'Passwords do not match\n';
            confirmPassword.classList.add('error');
        } else {
            confirmPassword.classList.remove('error');
        }

        if (!isValid) {
            alert(errorMessage);
        } else {
            // Form is valid, you can submit it
            form.submit();
        }
    });
});