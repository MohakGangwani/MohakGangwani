// Enhanced Main JavaScript for Mohak Gangwani Website
// Features: Lazy loading, progressive images, performance optimization, accessibility

class WebsiteEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.setupLazyLoading();
        this.setupProgressiveImages();
        this.setupScrollToTop();
        this.setupTypedText();
        this.setupSmoothScrolling();
        this.setupPerformanceOptimizations();
        this.setupAccessibility();
        this.setupFormEnhancements();
        this.setupAnimations();
    }

    // Lazy Loading Implementation
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  const img = entry.target;
                        this.loadImage(img);
                  observer.unobserve(img);
              }
          });
      });

            // Observe all images with data-src attribute
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            this.loadAllImages();
        }
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;

        // Create a new image to preload
        const tempImage = new Image();
        
        tempImage.onload = () => {
            img.src = src;
            img.classList.remove('lazy-image');
            img.classList.add('loaded');
            img.removeAttribute('data-src');
            
            // Trigger custom event for other components
            img.dispatchEvent(new CustomEvent('imageLoaded'));
        };

        tempImage.onerror = () => {
            img.classList.add('image-error');
            img.alt = 'Image failed to load';
        };

        tempImage.src = src;
    }

    loadAllImages() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }

    // Progressive Image Loading
    setupProgressiveImages() {
        document.querySelectorAll('.progressive-image').forEach(container => {
            const img = container.querySelector('img');
            if (!img) return;

            container.classList.add('loading');

            img.onload = () => {
                container.classList.remove('loading');
                container.classList.add('loaded');
            };

            img.onerror = () => {
                container.classList.remove('loading');
                container.classList.add('error');
            };
        });
    }

    // Enhanced Scroll to Top
    setupScrollToTop() {
        const scrollTopBtn = document.getElementById('scrollTop');
        if (!scrollTopBtn) return;

        let isScrolling = false;

        const showScrollButton = () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('visible');
      } else {
                scrollTopBtn.classList.remove('visible');
            }
        };

        const smoothScrollToTop = (e) => {
            e.preventDefault();
            if (isScrolling) return;

            isScrolling = true;
            const startPosition = window.pageYOffset;
            const targetPosition = 0;
            const distance = targetPosition - startPosition;
            const duration = 1000;
            let start = null;

            const animation = (currentTime) => {
                if (start === null) start = currentTime;
                const timeElapsed = currentTime - start;
                const run = this.easeInOutCubic(timeElapsed, startPosition, distance, duration);
                window.scrollTo(0, run);
                if (timeElapsed < duration) {
                    requestAnimationFrame(animation);
      } else {
                    isScrolling = false;
                }
            };

            requestAnimationFrame(animation);
        };

        // Throttled scroll event
        let ticking = false;
        const updateScrollButton = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    showScrollButton();
                    ticking = false;
                });
                ticking = true;
            }
        };

        window.addEventListener('scroll', updateScrollButton, { passive: true });
        scrollTopBtn.addEventListener('click', smoothScrollToTop);
    }

    // Easing function for smooth scrolling
    easeInOutCubic(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t * t + b;
        t -= 2;
        return c / 2 * (t * t * t + 2) + b;
    }

    // Typed Text Animation
    setupTypedText() {
        if (typeof Typed !== 'undefined' && window.typedStrings) {
      const typedElement = document.getElementById('typed-text');
      if (typedElement) {
                new Typed(typedElement, {
                    strings: window.typedStrings,
              typeSpeed: 50,
              backSpeed: 30,
              backDelay: 2000,
              loop: true,
              showCursor: true,
                    cursorChar: '|',
                    autoInsertCss: true
                });
            }
        }
    }

    // Smooth Scrolling for Anchor Links
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Performance Optimizations
    setupPerformanceOptimizations() {
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Defer non-critical JavaScript
        this.deferNonCriticalScripts();
        
        // Optimize images on viewport change
        this.optimizeImagesOnResize();
    }

    preloadCriticalResources() {
        const criticalResources = [
            '/static/css/main.css',
            '/static/js/main.js'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
        });
    }

    deferNonCriticalScripts() {
        // Defer loading of non-critical scripts
        const deferredScripts = [
            'https://unpkg.com/aos@2.3.1/dist/aos.js'
        ];

        deferredScripts.forEach(src => {
            const script = document.createElement('script');
            script.src = src;
            script.defer = true;
            document.body.appendChild(script);
        });
    }

    optimizeImagesOnResize() {
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.updateImageSizes();
            }, 250);
        });
    }

    updateImageSizes() {
        // Update image sizes based on viewport
        const images = document.querySelectorAll('img[data-srcset]');
        images.forEach(img => {
            const srcset = img.dataset.srcset;
            if (srcset) {
                img.srcset = srcset;
            }
        });
    }

    // Accessibility Enhancements
    setupAccessibility() {
        // Skip to main content link
        this.addSkipToContentLink();
        
        // Enhanced keyboard navigation
        this.enhanceKeyboardNavigation();
        
        // Focus management
        this.setupFocusManagement();
        
        // ARIA live regions
        this.setupAriaLiveRegions();
    }

    addSkipToContentLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link sr-only sr-only-focusable';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            z-index: 1001;
            color: white;
            background: #000;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    enhanceKeyboardNavigation() {
        // Enhanced tab navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    setupFocusManagement() {
        // Focus trap for modals
        this.setupFocusTrap();
        
        // Focus restoration
        this.setupFocusRestoration();
    }

    setupFocusTrap() {
        // Implementation for focus trapping in modals
        // This would be used if modals are added later
    }

    setupFocusRestoration() {
        let lastFocusedElement;
        
        document.addEventListener('focusin', (e) => {
            lastFocusedElement = e.target;
        });
        
        // Restore focus when needed
        this.restoreFocus = () => {
            if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
                lastFocusedElement.focus();
            }
        };
    }

    setupAriaLiveRegions() {
        // Create ARIA live regions for dynamic content
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
        
        this.announceToScreenReader = (message) => {
            liveRegion.textContent = message;
        };
    }

    // Form Enhancements
    setupFormEnhancements() {
        // Enhanced form validation
        this.setupFormValidation();
        
        // Auto-save form data
        this.setupFormAutoSave();
        
        // Enhanced form accessibility
        this.setupFormAccessibility();
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
          inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
                
                input.addEventListener('input', () => {
                    this.clearFieldError(input);
                });
            });
            
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                  }
              });
          });
    }

    validateField(field) {
              const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }

        // Length validation
        if (field.hasAttribute('minlength')) {
            const minLength = parseInt(field.getAttribute('minlength'));
            if (value.length < minLength) {
                isValid = false;
                errorMessage = `Minimum ${minLength} characters required`;
            }
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        }

        return isValid;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        errorDiv.setAttribute('role', 'alert');
        
        field.parentNode.appendChild(errorDiv);
        
        // Announce error to screen reader
        this.announceToScreenReader(message);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    setupFormAutoSave() {
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const formId = form.dataset.autosave || 'default';
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.saveFormData(formId, form);
                });
            });
            
            // Restore form data on page load
            this.restoreFormData(formId, form);
        });
    }

    saveFormData(formId, form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem(`form_${formId}`, JSON.stringify(data));
    }

    restoreFormData(formId, form) {
        const savedData = localStorage.getItem(`form_${formId}`);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const field = form.querySelector(`[name="${key}"]`);
                    if (field && !field.value) {
                        field.value = data[key];
                    }
                });
            } catch (e) {
                console.warn('Failed to restore form data:', e);
            }
        }
    }

    setupFormAccessibility() {
        // Enhanced form labels and descriptions
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                if (!input.id) {
                    input.id = `input_${Math.random().toString(36).substr(2, 9)}`;
                }
                
                const label = input.parentNode.querySelector('label');
                if (label && !label.getAttribute('for')) {
                    label.setAttribute('for', input.id);
                  }
              });
          });
      }

    // Animation Enhancements
    setupAnimations() {
        // Intersection Observer for animations
        this.setupIntersectionAnimations();
        
        // Parallax effects
        this.setupParallaxEffects();
        
        // Smooth reveal animations
        this.setupRevealAnimations();
    }

    setupIntersectionAnimations() {
        if ('IntersectionObserver' in window) {
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });

            document.querySelectorAll('[data-animate]').forEach(element => {
                animationObserver.observe(element);
            });
        }
    }

    setupParallaxEffects() {
        // Simple parallax effect for hero section
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                heroSection.style.transform = `translateY(${rate}px)`;
            }, { passive: true });
        }
    }

    setupRevealAnimations() {
        // Counter animations for stats
        this.setupCounterAnimations();
        
        // Progress bar animations
        this.setupProgressAnimations();
    }

    setupCounterAnimations() {
        const counters = document.querySelectorAll('.counter');
        if (counters.length === 0) return;

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.dataset.target);
                    this.animateCounter(counter, target);
                    counterObserver.unobserve(counter);
                }
              });
          });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    animateCounter(counter, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current);
        }, 20);
    }

    setupProgressAnimations() {
        const progressBars = document.querySelectorAll('.progress-bar');
        if (progressBars.length === 0) return;

        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const width = progressBar.dataset.width || '100%';
                    progressBar.style.width = width;
                    progressObserver.unobserve(progressBar);
                }
            });
        });

        progressBars.forEach(progressBar => {
            progressObserver.observe(progressBar);
        });
    }

    // Utility Methods
    debounce(func, wait) {
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

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new WebsiteEnhancer();
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('Page Load Performance:', {
                    'DOM Content Loaded': perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    'Load Complete': perfData.loadEventEnd - perfData.loadEventStart,
                    'Total Time': perfData.loadEventEnd - perfData.fetchStart
                });
            }
        }, 0);
    });
}

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}