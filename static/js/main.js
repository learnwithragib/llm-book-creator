// This file can be used for any additional JavaScript functionality
// that's not specific to the book generation process.

document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add responsive navigation menu for mobile devices
    const navToggle = document.createElement('button');
    navToggle.textContent = '☰';
    navToggle.classList.add('nav-toggle');
    document.querySelector('nav').prepend(navToggle);

    navToggle.addEventListener('click', () => {
        document.querySelector('nav ul').classList.toggle('show');
    });
});
