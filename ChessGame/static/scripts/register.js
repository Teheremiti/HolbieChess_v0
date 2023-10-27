document.querySelector('form').addEventListener('submit', (err) => {
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;
    if (!username || !password) {
        err.preventDefault();
        alert('Some fields are missing, please fill them out')
    }
})
