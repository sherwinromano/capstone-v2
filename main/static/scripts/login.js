const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    const showIcon = document.querySelector('#showIcon');
    const hideIcon = document.querySelector('#hideIcon');

    togglePassword.addEventListener('click', function (e) {
        // Toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        // Toggle the icons
        if (type === 'password') {
            showIcon.style.display = 'block';
            hideIcon.style.display = 'none';
        } else {
            showIcon.style.display = 'none';
            hideIcon.style.display = 'block';
        }
    });

    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get the current CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(this.action, {
            method: 'POST',
            body: new FormData(this),
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                Swal.fire({
                    icon: 'success',
                    title: 'Welcome back!',
                    text: 'Login successful',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.href = data.redirect_url;
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Login Failed',
                    text: data.message
                });
            }
        })
        .catch(error => {
            // If there's a CSRF error, reload the page to get a fresh token
            if (error.message.includes('CSRF')) {
                window.location.reload();
                return;
            }
            
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong! Please try again.'
            });
        });
    });