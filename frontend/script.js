document.getElementById('createUserForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const responseDiv = document.getElementById('response');

    try {
                        const response = await fetch('/api/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, username, password }),
        });

        const result = await response.json();
        responseDiv.className = 'response ' + (response.ok ? 'success' : 'error');
        responseDiv.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        responseDiv.className = 'response error';
        responseDiv.textContent = `Error: ${error.message}`;
    }
});

// Handle login to retrieve Bearer token
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const username = document.getElementById('login_username').value;
        const password = document.getElementById('login_password').value;
        const responseDiv = document.getElementById('response');

        try {
            const form = new URLSearchParams();
            form.append('username', username);
            form.append('password', password);
            form.append('grant_type', 'password');

            const response = await fetch('/api/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: form.toString(),
            });

            const result = await response.json();
            if (response.ok && result.access_token) {
                localStorage.setItem('access_token', result.access_token);
                updateAuthState();
                startAlertsPolling(); // Start polling after successful login
            }
            responseDiv.className = 'response ' + (response.ok ? 'success' : 'error');
            responseDiv.textContent = JSON.stringify(result, null, 2);
        } catch (error) {
            responseDiv.className = 'response error';
            responseDiv.textContent = `Error: ${error.message}`;
        }
    });
}

// Create alert with token
document.getElementById('createAlertForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const base_currency = document.getElementById('base_currency').value;
    const quote_currency = document.getElementById('quote_currency').value;
    const target_rate = document.getElementById('target_rate').value;
    const condition = document.getElementById('condition').value;
    const responseDiv = document.getElementById('response');

    try {
                const response = await fetch('/api/alerts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`,
            },
            body: JSON.stringify({
                base_currency,
                quote_currency,
                target_rate: parseFloat(target_rate),
                condition
            }),
        });

        const result = await response.json();
        responseDiv.className = 'response ' + (response.ok ? 'success' : 'error');
        responseDiv.textContent = JSON.stringify(result, null, 2);
        if (response.ok) {
            // refresh alerts list immediately
            loadAlerts();
        }
    } catch (error) {
        responseDiv.className = 'response error';
        responseDiv.textContent = `Error: ${error.message}`;
    }
});

// Simple auth state indicator and logout
function updateAuthState() {
    const token = localStorage.getItem('access_token');
    const authInfo = document.getElementById('authInfo');
    const logoutBtn = document.getElementById('logoutBtn');
    if (token) {
        if (authInfo) authInfo.textContent = 'Logged in';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        startAlertsPolling();
    } else {
        if (authInfo) authInfo.textContent = 'Logged out';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (typeof alertsIntervalId !== 'undefined' && alertsIntervalId) {
            clearInterval(alertsIntervalId);
        }
        const el = document.getElementById('alertsList');
        if (el) el.textContent = 'Login to load alerts.';
    }
}

const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', function () {
        localStorage.removeItem('access_token');
        updateAuthState();
        const responseDiv = document.getElementById('response');
        responseDiv.className = 'response success';
        responseDiv.textContent = 'Logged out.';
    });
}

updateAuthState();

// helper to render alerts
function renderAlerts(alerts) {
    const el = document.getElementById('alertsList');
    if (!el) return;
    if (!alerts || alerts.length === 0) {
        el.className = 'response';
        el.textContent = 'No alerts found.';
        return;
    }
    el.className = 'response';
    const lines = alerts.map(a => `${a.id}: ${a.base_currency}/${a.quote_currency} ${a.condition} ${a.target_rate}  [${a.status}]`);
    el.textContent = lines.join('\n');
}

async function loadAlerts() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        const el = document.getElementById('alertsList');
        if (el) {
            el.className = 'response';
            el.textContent = 'Login to load alerts.';
        }
        return;
    }
    try {
        const res = await fetch('/api/alerts', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!res.ok) {
            renderAlerts([]);
            return;
        }
        const data = await res.json();
        renderAlerts(data);
    } catch (_) {
        renderAlerts([]);
    }
}

let alertsIntervalId = null;
function startAlertsPolling() {
    if (alertsIntervalId) clearInterval(alertsIntervalId);
    loadAlerts();
    alertsIntervalId = setInterval(loadAlerts, 30000);
}
