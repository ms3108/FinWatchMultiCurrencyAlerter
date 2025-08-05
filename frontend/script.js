document.getElementById('createUserForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const responseDiv = document.getElementById('response');

    try {
                        const response = await fetch('/api/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();
        responseDiv.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        responseDiv.textContent = `Error: ${error.message}`;
    }
});

document.getElementById('createAlertForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const userId = document.getElementById('user_id').value;
    const symbol = document.getElementById('symbol').value;
    const price = document.getElementById('price').value;
    const responseDiv = document.getElementById('response');

    try {
                const response = await fetch('/api/alerts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                user_id: parseInt(userId),
                symbol: symbol,
                price: parseFloat(price)
            }),
        });

        const result = await response.json();
        responseDiv.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        responseDiv.textContent = `Error: ${error.message}`;
    }
});
