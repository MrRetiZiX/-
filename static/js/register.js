document.querySelector('input[name="verification_code"]').addEventListener('blur', function() {
    const code = this.value;
    fetch('/verify-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({code: code})
    })
    .then(response => response.json())
    .then(data => {
        if (data.valid) {
            document.getElementById('registration-fields').classList.remove('hidden');
        }
    });
});
