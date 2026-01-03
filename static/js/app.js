// Main JavaScript file for the Flask application

document.addEventListener('DOMContentLoaded', function () {
    // Mobile navigation toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            navToggle.innerHTML = navMenu.classList.contains('active')
                ? '<i class="fas fa-times"></i>'
                : '<i class="fas fa-bars"></i>';
        });

        // Close mobile menu when clicking a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.innerHTML = '<i class="fas fa-bars"></i>';
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Only process internal anchor links
            if (href === '#') return;

            const targetElement = document.querySelector(href);
            if (targetElement) {
                e.preventDefault();

                // Close mobile menu if open
                if (navMenu && navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    navToggle.innerHTML = '<i class="fas fa-bars"></i>';
                }

                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add active class to current page in navigation
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath ||
            (currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });

    // Form validation enhancement
    const contactForm = document.querySelector('form');
    if (contactForm && !contactForm.classList.contains('greet-form')) {
        contactForm.addEventListener('submit', function (e) {
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#f72585';

                    // Add error message if not present
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'This field is required';
                        errorMsg.style.color = '#f72585';
                        errorMsg.style.fontSize = '0.85rem';
                        errorMsg.style.marginTop = '5px';
                        input.parentNode.appendChild(errorMsg);
                    }
                } else {
                    input.style.borderColor = '';

                    // Remove error message if present
                    if (input.nextElementSibling && input.nextElementSibling.classList.contains('error-message')) {
                        input.parentNode.removeChild(input.nextElementSibling);
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();

                // Scroll to first error
                const firstError = this.querySelector('input[style*="border-color"], textarea[style*="border-color"]');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }

    // Add animation on scroll
    function animateOnScroll() {
        const elements = document.querySelectorAll('.feature-card, .demo-card, .stat-card');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;

            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }

    // Set initial state for animation
    document.querySelectorAll('.feature-card, .demo-card, .stat-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    // Run on load and scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    // Update visitor count with animation
    const visitorCountEl = document.getElementById('visitorCount');
    if (visitorCountEl) {
        const count = parseInt(visitorCountEl.textContent.match(/\d+/)[0]);
        let currentCount = 0;

        const updateCounter = () => {
            if (currentCount < count) {
                currentCount += Math.ceil(count / 50);
                if (currentCount > count) currentCount = count;

                visitorCountEl.textContent = `Visitors: ${currentCount}`;
                setTimeout(updateCounter, 30);
            }
        };

        // Start counter after a short delay
        setTimeout(updateCounter, 1000);
    }

    // Theme toggle (optional - can be enabled)
    const themeToggle = document.createElement('button');
    themeToggle.id = 'themeToggle';
    themeToggle.className = 'btn btn-small';
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.style.position = 'fixed';
    themeToggle.style.bottom = '20px';
    themeToggle.style.right = '20px';
    themeToggle.style.zIndex = '1000';

    document.body.appendChild(themeToggle);

    themeToggle.addEventListener('click', function () {
        document.body.classList.toggle('dark-theme');

        if (document.body.classList.contains('dark-theme')) {
            this.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
        } else {
            this.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
        }
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Add dark theme styles
    const darkThemeStyles = document.createElement('style');
    darkThemeStyles.textContent = `
        body.dark-theme {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        body.dark-theme .navbar,
        body.dark-theme .feature-card,
        body.dark-theme .demo-card,
        body.dark-theme .greet-form-container,
        body.dark-theme .contact-form-container {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        
        body.dark-theme .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        
        body.dark-theme .demo {
            background-color: #121212;
        }
        
        body.dark-theme .nav-link {
            color: #e0e0e0;
        }
        
        body.dark-theme .form-input,
        body.dark-theme .form-textarea {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border-color: #444;
        }
        
        body.dark-theme .chat-messages {
            background-color: #1a1a1a;
        }
        
        body.dark-theme .message.bot .message-content {
            background-color: #2d2d2d;
            border-color: #444;
        }
    `;
    document.head.appendChild(darkThemeStyles);
});