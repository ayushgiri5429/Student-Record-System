// Custom JavaScript for Student Record System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Search functionality enhancement
    const searchForms = document.querySelectorAll('form[method="get"]');
    searchForms.forEach(function(form) {
        const searchInput = form.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    form.submit();
                }
            });
        }
    });

    // Confirm before delete
    const deleteButtons = document.querySelectorAll('.btn-outline-danger');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });

    // Auto-focus on first input field in forms
    const formInputs = document.querySelectorAll('form input[type="text"], form input[type="email"], form input[type="password"]');
    if (formInputs.length > 0) {
        formInputs[0].focus();
    }

    // Enhanced table functionality
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        // Add zebra striping
        table.classList.add('table-striped');
        
        // Make table rows clickable if they have links
        const tableRows = table.querySelectorAll('tbody tr');
        tableRows.forEach(function(row) {
            const link = row.querySelector('a[href]');
            if (link) {
                row.style.cursor = 'pointer';
                row.addEventListener('click', function(event) {
                    if (event.target.tagName !== 'A' && event.target.tagName !== 'BUTTON') {
                        window.location = link.href;
                    }
                });
            }
        });
    });
});

// Utility functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}