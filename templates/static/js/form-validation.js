// static/js/form-validation.js
// Simple client-side validation for forms with class="needs-validation"
// Works with Bootstrap 5 form-control / invalid-feedback markup.

(function () {
  'use strict';

  // Wait for DOM
  document.addEventListener('DOMContentLoaded', function () {
    // Find all forms that should be validated
    var forms = Array.prototype.slice.call(document.querySelectorAll('.needs-validation'));

    if (!forms.length) return;

    forms.forEach(function (form) {
      // Add submit listener
      form.addEventListener('submit', function (event) {
        // Trigger browser validation (will set validity states)
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();

          // optional: focus first invalid input
          var firstInvalid = form.querySelector(':invalid');
          if (firstInvalid && typeof firstInvalid.focus === 'function') {
            firstInvalid.focus();
          }
        }

        // add bootstrap validated class for styling
        form.classList.add('was-validated');
      }, false);

      // Add input listeners to remove validation UI on change
      var inputs = form.querySelectorAll('input, textarea, select');
      inputs.forEach(function (inp) {
        inp.addEventListener('input', function () {
          if (form.classList.contains('was-validated')) {
            // re-run validation styling
            if (inp.checkValidity()) {
              inp.classList.remove('is-invalid');
              inp.classList.add('is-valid');
            } else {
              inp.classList.remove('is-valid');
              inp.classList.add('is-invalid');
            }
          }
        });
      });
    });
  });
})();
