// ============ Theme (dark / light / system) ============
const THEME_KEY = 'pacer_theme';
const modes = ['dark', 'light', 'system'];
const icons = { dark: 'ti-moon', light: 'ti-sun', system: 'ti-device-laptop' };
const labels = { dark: 'Dark', light: 'Light', system: 'System' };

function applyMode(m) {
    document.documentElement.classList.remove('dark', 'light');
    if (m === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.classList.add(prefersDark ? 'dark' : 'light');
    } else {
        document.documentElement.classList.add(m);
    }
    const icon = document.getElementById('modeIcon');
    const label = document.getElementById('modeLabel');
    if (icon) icon.className = 'ti ' + icons[m];
    if (label) label.textContent = labels[m];
}

function cycleMode() {
    const current = localStorage.getItem(THEME_KEY) || 'dark';
    const next = modes[(modes.indexOf(current) + 1) % modes.length];
    localStorage.setItem(THEME_KEY, next);
    applyMode(next);
}

function initTheme() {
    applyMode(localStorage.getItem(THEME_KEY) || 'dark');
}

// ============ Auth (email lookup against existing students) ============
const AUTH_KEY = 'pacer_user';

function openLoginModal() {
    document.getElementById('loginModal').classList.add('show');
}
function closeLoginModal() {
    document.getElementById('loginModal').classList.remove('show');
    const err = document.getElementById('loginError');
    if (err) err.style.display = 'none';
}

async function doLogin() {
    const emailInput = document.getElementById('loginEmail');
    const errorEl = document.getElementById('loginError');
    const email = emailInput.value.trim();
    errorEl.style.display = 'none';

    if (!email) {
        errorEl.textContent = 'Enter your email to continue.';
        errorEl.style.display = 'block';
        return;
    }

    try {
        const res = await fetch(`/get-history?email=${encodeURIComponent(email)}`);
        const data = await res.json();

        if (!data.student) {
            errorEl.textContent = "No account found with that email yet. Generate your first set of questions to create one!";
            errorEl.style.display = 'block';
            return;
        }

        localStorage.setItem(AUTH_KEY, JSON.stringify({
            name: data.student.name,
            email: data.student.email
        }));
        closeLoginModal();
        updateAuthUI();
    } catch (err) {
        errorEl.textContent = 'Something went wrong reaching PACER. Try again in a moment.';
        errorEl.style.display = 'block';
    }
}

function logout() {
    localStorage.removeItem(AUTH_KEY);
    updateAuthUI();
}

function getLoggedInUser() {
    const raw = localStorage.getItem(AUTH_KEY);
    return raw ? JSON.parse(raw) : null;
}

function updateAuthUI() {
    const authArea = document.getElementById('authArea');
    if (!authArea) return;
    const user = getLoggedInUser();

    if (user) {
        const firstName = user.name.split(' ')[0];
        authArea.innerHTML = `
            <span class="text-sm text-on-surface-variant hidden sm:inline">Hi, ${firstName}</span>
            <button onclick="logout()" class="bg-glass-fill border border-glass-stroke text-on-surface text-sm px-4 py-2 rounded hover:bg-white/10 transition-all">Log out</button>
        `;
    } else {
        authArea.innerHTML = `
            <button onclick="openLoginModal()" class="bg-glass-fill border border-glass-stroke text-on-surface text-sm px-4 py-2 rounded hover:bg-white/10 transition-all">Log in</button>
            <button onclick="goToSignup()" class="bg-primary-container text-white px-4 py-2 rounded text-sm font-medium hover:brightness-110 hover-glow transition-all active:scale-95">Sign Up</button>
        `;
    }
}

function goToSignup() {
    if (window.location.pathname === '/') {
        const form = document.getElementById('generate-form');
        if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        window.location.href = '/#generate-form';
    }
}

function googleComingSoon() {
    const msg = document.getElementById('googleMsg');
    if (msg) {
        msg.style.display = 'block';
        clearTimeout(window._googleMsgTimeout);
        window._googleMsgTimeout = setTimeout(() => { msg.style.display = 'none'; }, 4000);
    }
}

// ============ WebGL shader background ============
function initShader() {
    const canvas = document.getElementById('shader-bg');
    if (!canvas) return;
    const gl = canvas.getContext('webgl');
    if (!gl) return;

    const vs = `attribute vec2 position;varying vec2 v_texCoord;void main(){v_texCoord=position*0.5+0.5;gl_Position=vec4(position,0.0,1.0);}`;
    const fsEl = document.getElementById('fragment-shader');
    if (!fsEl) return;
    const fs = fsEl.textContent;

    function mkShader(type, src) {
        const s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        return s;
    }

    const prog = gl.createProgram();
    gl.attachShader(prog, mkShader(gl.VERTEX_SHADER, vs));
    gl.attachShader(prog, mkShader(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(prog);
    gl.useProgram(prog);

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    const pos = gl.getAttribLocation(prog, 'position');
    gl.enableVertexAttribArray(pos);
    gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);

    const tLoc = gl.getUniformLocation(prog, 'u_time');
    const rLoc = gl.getUniformLocation(prog, 'u_resolution');
    const mLoc = gl.getUniformLocation(prog, 'u_mouse');

    let mx = 0, my = 0;
    document.addEventListener('mousemove', e => {
        mx = e.clientX;
        my = window.innerHeight - e.clientY;
    });

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        gl.viewport(0, 0, canvas.width, canvas.height);
    }
    window.addEventListener('resize', resize);
    resize();

    function render(t) {
        gl.uniform1f(tLoc, t * 0.001);
        gl.uniform2f(rLoc, canvas.width, canvas.height);
        gl.uniform2f(mLoc, mx, my);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
}

document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    updateAuthUI();
    initShader();
});