document.addEventListener('DOMContentLoaded', function() {
    const calendarDays = document.querySelector('.calendar-days');
    const monthYearText = document.querySelector('.calendar-header h2');
    const prevMonthBtn = document.querySelector('.calendar-nav:first-child');
    const nextMonthBtn = document.querySelector('.calendar-nav:last-child');
    const scheduleList = document.querySelector('.schedule-list');

    let currentDate = new Date();
    let selectedDate = new Date();

    // Sample events data - replace this with your actual events data from Django
    const events = [
        {
            date: '2025-01-13',
            student: 'Test',
            service: 'Cleaning'
        },
        {
            date: '2025-01-13',
            student: 'Test',
            service: 'Dental Filling'
        },
        {
            date: '2025-01-20',
            student: 'Test',
            service: 'Tooth Extraction'
        }
    ];

    function generateCalendar(date) {
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        const startingDay = firstDay.getDay();
        const monthLength = lastDay.getDate();

        // Update month and year text
        const months = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"];
        monthYearText.textContent = `${months[date.getMonth()]} ${date.getFullYear()}`;

        // Clear previous calendar
        calendarDays.innerHTML = '';

        // Add empty cells for days before the first day of the month
        for (let i = 0; i < startingDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            calendarDays.appendChild(emptyDay);
        }

        // Add days of the month
        for (let day = 1; day <= monthLength; day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;

            // Create date string for comparison
            const dateString = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

            // Check if this day has events
            const dayEvents = events.filter(event => event.date === dateString);
            if (dayEvents.length > 0) {
                dayElement.classList.add('has-event');
            }

            // Highlight current day
            if (date.getMonth() === new Date().getMonth() &&
                date.getFullYear() === new Date().getFullYear() &&
                day === new Date().getDate()) {
                dayElement.classList.add('current-day');
            }

            // Highlight selected day
            if (date.getMonth() === selectedDate.getMonth() &&
                date.getFullYear() === selectedDate.getFullYear() &&
                day === selectedDate.getDate()) {
                dayElement.classList.add('selected-day');
            }

            // Add click event to show schedules
            dayElement.addEventListener('click', () => {
                // Remove previous selection
                document.querySelectorAll('.calendar-day').forEach(day => {
                    day.classList.remove('selected-day');
                });
                
                // Add new selection
                dayElement.classList.add('selected-day');
                
                // Update selected date
                selectedDate = new Date(date.getFullYear(), date.getMonth(), day);
                
                // Update schedule list
                updateScheduleList(dateString);
            });

            calendarDays.appendChild(dayElement);
        }
    }

    function updateScheduleList(dateString) {
        // Filter events for selected date
        const dayEvents = events.filter(event => event.date === dateString);
        
        // Clear previous schedule list
        scheduleList.innerHTML = '';

        if (dayEvents.length > 0) {
            dayEvents.forEach(event => {
                const scheduleItem = document.createElement('div');
                scheduleItem.className = 'schedule-item';
                scheduleItem.innerHTML = `
                    <span class="student-name">${event.student}</span>
                    <span class="service-type">${event.service}</span>
                `;
                scheduleList.appendChild(scheduleItem);
            });
        } else {
            const noEvents = document.createElement('div');
            noEvents.className = 'schedule-item no-events';
            noEvents.textContent = 'No appointments scheduled';
            scheduleList.appendChild(noEvents);
        }
    }

    // Event listeners for navigation buttons
    prevMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        generateCalendar(currentDate);
    });

    nextMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        generateCalendar(currentDate);
    });

    // Initialize calendar
    generateCalendar(currentDate);
    
    // Initialize schedule list with current date
    const initialDateString = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;
    updateScheduleList(initialDateString);
}); 