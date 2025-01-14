document.addEventListener('DOMContentLoaded', function() {
    const calendarDays = document.querySelector('.calendar-days');
    const monthYearText = document.querySelector('.calendar-header h2');
    const prevMonthBtn = document.querySelector('.calendar-nav:first-child');
    const nextMonthBtn = document.querySelector('.calendar-nav:last-child');

    let currentDate = new Date();

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

            // Highlight current day
            if (date.getMonth() === new Date().getMonth() &&
                date.getFullYear() === new Date().getFullYear() &&
                day === new Date().getDate()) {
                dayElement.classList.add('current-day');
            }

            // Add event indicator for days with events
            if (hasEvent(day, date.getMonth(), date.getFullYear())) {
                dayElement.classList.add('has-event');
            }

            calendarDays.appendChild(dayElement);
        }
    }

    function hasEvent(day, month, year) {
        // Example events - replace with your actual event data
        const events = [
            { day: 13, month: 0, year: 2025 },  // January 13, 2025
            { day: 20, month: 0, year: 2025 }   // January 20, 2025
        ];

        return events.some(event => 
            event.day === day && 
            event.month === month && 
            event.year === year
        );
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
}); 