/**
* Template Name: DevFolio
* Template URL: https://bootstrapmade.com/devfolio-bootstrap-portfolio-html-template/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  // Initialize AOS
  AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true,
      offset: 100,
      delay: 0
  });

  // Lazy loading for images
  function lazyLoadImages() {
      const images = document.querySelectorAll('img[data-src]');
      const imageObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  const img = entry.target;
                  img.src = img.dataset.src;
                  img.classList.add('loaded');
                  observer.unobserve(img);
              }
          });
      });

      images.forEach(img => imageObserver.observe(img));
  }

  // Initialize lazy loading
  document.addEventListener('DOMContentLoaded', lazyLoadImages);

  // Scroll to top functionality
  const scrollTop = document.getElementById('scrollTop');
  window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
          scrollTop.classList.add('show');
      } else {
          scrollTop.classList.remove('show');
      }
  });

  scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Navbar background on scroll
  window.addEventListener('scroll', () => {
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 50) {
          navbar.style.background = 'rgba(255, 255, 255, 0.98)';
          navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
      } else {
          navbar.style.background = 'rgba(255, 255, 255, 0.95)';
          navbar.style.boxShadow = 'none';
      }
  });

  // Performance optimization: Debounce scroll events
  function debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
          const later = () => {
              clearTimeout(timeout);
              func(...args);
          };
          clearTimeout(timeout);
          timeout = setTimeout(later, wait);
      };
  }

  // Apply debouncing to scroll events
  const debouncedScrollHandler = debounce(() => {
      // Navbar scroll effect
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 50) {
          navbar.style.background = 'rgba(255, 255, 255, 0.98)';
          navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
      } else {
          navbar.style.background = 'rgba(255, 255, 255, 0.95)';
          navbar.style.boxShadow = 'none';
      }

      // Scroll to top button
      if (window.pageYOffset > 300) {
          scrollTop.classList.add('show');
      } else {
          scrollTop.classList.remove('show');
      }
  }, 10);

  window.addEventListener('scroll', debouncedScrollHandler);

  // Preload critical images
  function preloadCriticalImages() {
      // Get the profile image URL from a data attribute
      const profileImg = document.querySelector('img[src*="about-me"]');
      if (profileImg && profileImg.src) {
          const link = document.createElement('link');
          link.rel = 'preload';
          link.as = 'image';
          link.href = profileImg.src;
          document.head.appendChild(link);
      }
  }

  // Initialize preloading
  document.addEventListener('DOMContentLoaded', preloadCriticalImages);

  // Register service worker
  if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
          navigator.serviceWorker.register('/static/js/sw.js')
              .then(registration => {
                  console.log('SW registered: ', registration);
              })
              .catch(registrationError => {
                  console.log('SW registration failed: ', registrationError);
              });
      });
  }

  // Typed.js initialization for home page
  document.addEventListener('DOMContentLoaded', function() {
      const typedElement = document.getElementById('typed-text');
      if (typedElement) {
          new Typed('#typed-text', {
              strings: window.typedStrings || ['Data Scientist', 'Machine Learning Engineer', 'Analytics Consultant'],
              typeSpeed: 50,
              backSpeed: 30,
              backDelay: 2000,
              loop: true,
              showCursor: true,
              cursorChar: '|'
          });
      }
      
      // Animated counters
      const counters = document.querySelectorAll('.counter');
      const animateCounters = () => {
          counters.forEach(counter => {
              const target = parseInt(counter.getAttribute('data-target'));
              const count = parseInt(counter.innerText);
              const increment = target / 100;
              
              if (count < target) {
                  counter.innerText = Math.ceil(count + increment);
                  setTimeout(animateCounters, 20);
              } else {
                  counter.innerText = target + '+';
              }
          });
      };
      
      // Skill progress bars
      const skillCards = document.querySelectorAll('.skill-card');
      const animateProgressBars = () => {
          skillCards.forEach(card => {
              const progressBar = card.querySelector('.progress-bar');
              const targetWidth = progressBar.getAttribute('data-width');
              
              setTimeout(() => {
                  progressBar.style.width = targetWidth + '%';
              }, 500);
          });
      };
      
      // Intersection Observer for animations
      const observerOptions = {
          threshold: 0.5,
          rootMargin: '0px 0px -100px 0px'
      };
      
      const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  if (entry.target.classList.contains('stat-card')) {
                      animateCounters();
                  } else if (entry.target.classList.contains('skill-card')) {
                      animateProgressBars();
                  }
              }
          });
      }, observerOptions);
      
      // Observe elements
      document.querySelectorAll('.stat-card').forEach(card => observer.observe(card));
      document.querySelectorAll('.skill-card').forEach(card => observer.observe(card));
      
      // Interactive skill badges
      const skillBadges = document.querySelectorAll('.skill-badge');
      skillBadges.forEach(badge => {
          badge.addEventListener('mouseenter', function() {
              this.style.transform = 'scale(1.1)';
              this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
          });
          
          badge.addEventListener('mouseleave', function() {
              this.style.transform = 'scale(1)';
              this.style.boxShadow = 'none';
          });
      });
      
      // Scroll indicator functionality
      const scrollIndicator = document.querySelector('.scroll-indicator');
      if (scrollIndicator) {
          scrollIndicator.addEventListener('click', function() {
              const nextSection = document.querySelector('.section');
              if (nextSection) {
                  nextSection.scrollIntoView({ 
                      behavior: 'smooth',
                      block: 'start'
                  });
              }
          });
      }
  });

  // Contact form handling
  document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('contactForm');
      if (form) {
          const submitBtn = document.getElementById('submitBtn');
          const btnText = submitBtn.querySelector('.btn-text');
          const btnLoading = submitBtn.querySelector('.btn-loading');
          const messageInput = document.getElementById('message');
          const charCountSpan = document.getElementById('charCount');

          // Update character count
          if (messageInput && charCountSpan) {
              messageInput.addEventListener('input', function() {
                  const currentLength = this.value.length;
                  charCountSpan.textContent = currentLength;
                  
                  // Change color based on length
                  if (currentLength < 10) {
                      charCountSpan.style.color = '#dc3545';
                  } else if (currentLength > 1800) {
                      charCountSpan.style.color = '#ffc107';
                  } else {
                      charCountSpan.style.color = '#198754';
                  }
              });
          }

          // Real-time validation
          const inputs = form.querySelectorAll('input, textarea');
          inputs.forEach(input => {
              input.addEventListener('blur', function() {
                  validateField(this);
              });
              
              input.addEventListener('input', function() {
                  if (this.classList.contains('is-invalid')) {
                      validateField(this);
                  }
              });
          });

          function validateField(field) {
              const value = field.value.trim();
              const isValid = field.checkValidity();
              
              if (isValid && value.length > 0) {
                  field.classList.remove('is-invalid');
                  field.classList.add('is-valid');
              } else {
                  field.classList.remove('is-valid');
                  field.classList.add('is-invalid');
              }
          }

          form.addEventListener('submit', function(e) {
              // Prevent submission if form is invalid
              if (!form.checkValidity()) {
                  e.preventDefault();
                  e.stopPropagation();
                  
                  // Show validation messages
                  form.classList.add('was-validated');
                  
                  // Focus on first invalid field
                  const firstInvalid = form.querySelector('.is-invalid');
                  if (firstInvalid) {
                      firstInvalid.focus();
                  }
                  return;
              }
              
              // Show loading state
              btnText.classList.add('d-none');
              btnLoading.classList.remove('d-none');
              submitBtn.disabled = true;
          });

          // Bootstrap form validation
          const forms = document.querySelectorAll('.needs-validation');
          Array.from(forms).forEach(form => {
              form.addEventListener('submit', event => {
                  if (!form.checkValidity()) {
                      event.preventDefault();
                      event.stopPropagation();
                  }
                  form.classList.add('was-validated');
              }, false);
          });

          // Add floating labels effect
          const floatingLabels = document.querySelectorAll('.form-control');
          floatingLabels.forEach(input => {
              input.addEventListener('focus', function() {
                  this.parentElement.classList.add('focused');
              });
              
              input.addEventListener('blur', function() {
                  if (this.value.length === 0) {
                      this.parentElement.classList.remove('focused');
                  }
              });
          });
      }
  });

  // Project details modal functionality
  document.addEventListener('DOMContentLoaded', function() {
      const projectDetailsBtns = document.querySelectorAll('.project-details-btn');
      const projectModal = document.getElementById('projectModal');
      
      if (projectModal && projectDetailsBtns.length > 0) {
          const projectModalInstance = new bootstrap.Modal(projectModal);
          const projectDetails = document.getElementById('projectDetails');
          const projectLink = document.getElementById('projectLink');
          
          projectDetailsBtns.forEach(btn => {
              btn.addEventListener('click', function() {
                  const title = this.getAttribute('data-project');
                  const description = this.getAttribute('data-description');
                  const tags = this.getAttribute('data-tags').split(', ');
                  
                  // Find the project link
                  const projectCard = this.closest('.project-card');
                  const linkElement = projectCard.querySelector('a[href*="github"]');
                  const link = linkElement ? linkElement.href : '#';
                  
                  // Populate modal
                  projectDetails.innerHTML = `
                      <h4 class="mb-3">${title}</h4>
                      <p class="mb-4">${description}</p>
                      <div class="mb-3">
                          <h6>Technologies Used:</h6>
                          <div class="tags-container">
                              ${tags.map(tag => `<span class="badge bg-primary me-1 mb-1">${tag}</span>`).join('')}
                          </div>
                      </div>
                  `;
                  
                  projectLink.href = link;
                  projectModalInstance.show();
              });
          });
      }
  });

})();