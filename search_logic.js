document.addEventListener('DOMContentLoaded', () => {
    // 1. Check if Search Button exists
    const searchBtn = document.getElementById('search-button');
    if (!searchBtn) return; // Exit if no button

    // 2. Create Modal HTML
    const modalHTML = `
        <div id="aris-search-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.8); z-index:9999; backdrop-filter:blur(4px); align-items:flex-start; justify-content:center; padding-top:5rem;">
            <div style="background:white; width:90%; max-width:600px; border-radius:1rem; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.25); overflow:hidden; display:flex; flex-direction:column; max-height:80vh;">
                <!-- Header -->
                <div style="padding:1rem; border-bottom:1px solid #e2e8f0; display:flex; align-items:center; gap:0.5rem;">
                    <span style="font-size:1.5rem;">🔍</span>
                    <input type="text" id="aris-search-input" placeholder="Search lessons, units, games..." style="flex:1; padding:0.75rem; font-size:1.1rem; border:2px solid #e2e8f0; border-radius:0.5rem; outline:none; transition:border 0.2s;">
                    <button id="aris-search-close" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#64748b;">&times;</button>
                </div>
                <!-- Results -->
                <div id="aris-search-results" style="padding:0; overflow-y:auto; flex:1;">
                    <div style="padding:2rem; text-align:center; color:#94a3b8;">Type to start searching...</div>
                </div>
                <!-- Footer -->
                <div style="padding:0.75rem; background:#f8fafc; border-top:1px solid #e2e8f0; font-size:0.8rem; color:#64748b; text-align:right;">
                    ArisEdu Search
                </div>
            </div>
        </div>
    `;

    // 3. Inject Modal into Body
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // 4. Logic Variables
    const modal = document.getElementById('aris-search-modal');
    const input = document.getElementById('aris-search-input');
    const resultsContainer = document.getElementById('aris-search-results');
    const closeBtn = document.getElementById('aris-search-close');

    // 5. Functions
    function openSearch() {
        modal.style.display = 'flex';
        input.value = '';
        input.focus();
        renderResults([]); // Clear previous
    }

    function closeSearch() {
        modal.style.display = 'none';
    }

    function performSearch(query) {
        if (!query || query.length < 2) {
            resultsContainer.innerHTML = '<div style="padding:2rem; text-align:center; color:#94a3b8;">Type at least 2 characters...</div>';
            return;
        }
        
        const q = query.toLowerCase();
        
        // Ensure index exists
        if (typeof ARIS_EDU_SEARCH_INDEX === 'undefined') {
            resultsContainer.innerHTML = '<div style="padding:1rem; color:#ef4444;">Search index not loaded.</div>';
            return;
        }

        const matches = ARIS_EDU_SEARCH_INDEX.filter(item => {
            return (item.title && item.title.toLowerCase().includes(q)) || 
                   (item.subtitle && item.subtitle.toLowerCase().includes(q)) ||
                   (item.content && item.content.toLowerCase().includes(q));
        }).slice(0, 10); // Limit to 10 results

        renderResults(matches);
    }

    function renderResults(items) {
        if (items.length === 0 && input.value.length >= 2) {
            resultsContainer.innerHTML = '<div style="padding:2rem; text-align:center; color:#94a3b8;">No results found.</div>';
            return;
        } else if (items.length === 0) {
            return; // Already handled empty state
        }

        let html = '';
        items.forEach(item => {
            html += `
                <a href="${item.url}" style="display:block; padding:1rem; border-bottom:1px solid #f1f5f9; text-decoration:none; color:inherit; transition:background 0.2s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='white'">
                    <div style="font-weight:600; color:#334155; font-size:1rem;">${highlight(item.title, input.value)}</div>
                    <div style="font-size:0.85rem; color:#64748b;">${highlight(item.subtitle, input.value)}</div>
                </a>
            `;
        });
        resultsContainer.innerHTML = html;
    }

    function highlight(text, query) {
        if(!text) return '';
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<span style="background:#fef08a; color:#854d0e;">$1</span>');
    }

    // 6. Event Listeners
    searchBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openSearch();
    });

    closeBtn.addEventListener('click', closeSearch);
    
    // Close when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeSearch();
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeSearch();
        }
        // Easy open with Ctrl+K or / (optional, maybe distracting)
    });

    // Search Input Listener
    input.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });
    
    // Dark Mode Support for Modal
    const isDarkMode = document.body.classList.contains('dark-mode');
    if(isDarkMode) {
        // Simple dark mode styles via JS
        const modalContent = modal.querySelector('div[style*="background:white"]');
        if(modalContent) {
           modalContent.style.background = '#1e293b'; 
           modalContent.style.color = '#e2e8f0'; 
        }
        const inputEl = document.getElementById('aris-search-input');
        if(inputEl) {
            inputEl.style.background = '#0f172a';
            inputEl.style.color = 'white';
            inputEl.style.border = '2px solid #334155';
        }
        const footer = modal.querySelector('div[style*="background:#f8fafc"]');
        if(footer) {
            footer.style.background = '#0f172a';
            footer.style.borderTop = '1px solid #334155';
        }
    }

    // 7. Global Theme Application (Enhanced for Full Site Coverage)
    function applyGlobalTheme() {
        try {
            const theme = localStorage.getItem('arisEduColorTheme') || 'blue-green';
            
            // Define Gradients
            const AURORA_GRADIENT = 'linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%)';
            const AURORA_GRADIENT_NO_ANGLE = 'linear-gradient(#3b82f6 0%, #10b981 50%, #8b5cf6 100%)';
            const AURORA_GRADIENT_REVERSED = 'linear-gradient(135deg, #8b5cf6 0%, #10b981 50%, #3b82f6 100%)';
            
            const themes = {
                'blue-green': AURORA_GRADIENT,
                'sunset': 'linear-gradient(to right, #FF7E5F, #00C9A7, #1A2A6C)',
                'forest': 'linear-gradient(to right, #228B22, #87CEEB, #E6E6FA)',
                'aurora-veil': 'linear-gradient(to right, #32CD32, #00FFFF, #8A2BE2)',
                'coral': 'linear-gradient(to right, #FF6F61, #40E0D0, #4B0082)',
                'twilight': 'linear-gradient(to right, #50C878, #0F52BA, #FF00FF)',
                'solar': 'linear-gradient(to right, #FFD700, #DC143C, #2E0854)',
                'autumn': 'linear-gradient(to right, #CC5500, #DAA520, #8B4513)',
                'crimson': 'linear-gradient(to right, #FFC0CB, #C21E56, #420D09)',
                'sunrise': 'linear-gradient(to right, #FFDAB9, #FF7F50, #FFFACD)',
                'ocean-mist': 'linear-gradient(to right, #001F3F, #3D9970, #E0FFFF)',
                'lavender': 'linear-gradient(to right, #C8A2C8, #9DC183, #FFFDD0)',
                'monochrome': 'linear-gradient(to right, #2C2C2C, #C0C0C0, #FFFFFF)',
                'cyber': 'linear-gradient(to right, #000000, #00FFFF)',
                'horizon': 'linear-gradient(to right, #708090, #4682B4, #FFFFF0)'
            };

            const activeGradient = themes[theme];

            if (activeGradient) {
                document.documentElement.style.setProperty('--rubric-border-gradient', activeGradient);
                
                // 1. Taskbar
                const taskbar = document.querySelector('.taskbar');
                if (taskbar) taskbar.style.background = activeGradient;

                // 2. Headings and other elements with explicit gradient class or inline style
                const elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    // Prevent modifying the theme selector options themselves
                    if (el.classList.contains('custom-option')) return;

                    const style = el.getAttribute('style');
                    if (!style) return;

                    // Handle standard Aurora (with 135deg)
                    if (style.includes(AURORA_GRADIENT) || style.includes('linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%)')) {
                       // Replace exact string in style attribute to preserve other properties
                       let newStyle = style.replace(/linear-gradient\(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%\)/g, activeGradient);
                       el.setAttribute('style', newStyle);
                    }

                    // Handle standard Aurora (NO angle specified - used in course boxes)
                    if (style.includes(AURORA_GRADIENT_NO_ANGLE) || style.includes('linear-gradient(#3b82f6 0%, #10b981 50%, #8b5cf6 100%)')) {
                        let newStyle = style.replace(/linear-gradient\(#3b82f6 0%, #10b981 50%, #8b5cf6 100%\)/g, activeGradient);
                        el.setAttribute('style', newStyle);
                     }

                    // Handle reversed Aurora (often used in buttons like .side-button)
                    if (style.includes(AURORA_GRADIENT_REVERSED) || style.includes('linear-gradient(135deg, #8b5cf6 0%, #10b981 50%, #3b82f6 100%)')) {
                        let newStyle = style.replace(/linear-gradient\(135deg, #8b5cf6 0%, #10b981 50%, #3b82f6 100%\)/g, activeGradient);
                        el.setAttribute('style', newStyle);
                     }
                    
                    // Fallback for background shorthand with hex codes if exact string doesn't match
                    // This is aggressive but necessary if formatting differs slightly (spaces etc)
                     if (style.includes('background:') && style.includes('#3b82f6') && style.includes('#10b981')) {
                        if (style.includes('gradient')) {
                             // Attempt to replace the gradient part
                             el.style.backgroundImage = activeGradient;
                        }
                    }
                });

                // 3. Handle CSS Classes via Injection
                const css = `
                    /* Text Gradients */
                    .page-title, 
                    .rubric-title, 
                    .company-title,
                    .rubric-hover-dot span {
                        background-image: ${activeGradient} !important;
                        background: ${activeGradient} !important;
                        -webkit-background-clip: text !important;
                        background-clip: text !important;
                        -webkit-text-fill-color: transparent; 
                    }

                    /* Background Gradients */
                    .taskbar,
                    .side-button,
                    .action-button, 
                    .nav-button,
                    .course-box,
                    .cta-button {
                        background: ${activeGradient} !important;
                        background-image: ${activeGradient} !important;
                    }

                    /* Border Gradients (Rubric Box) */
                    .rubric-card {
                        --rubric-border-gradient: ${activeGradient} !important;
                    }
                `;

                 const head = document.head || document.getElementsByTagName('head')[0];
                 const style = document.createElement('style');
                 style.type = 'text/css';
                 style.appendChild(document.createTextNode(css));
                 head.appendChild(style);

            } else {
                 // Reset if needed (though page reload usually handles this naturally)
            }

        } catch (e) {
            console.error("ArisEdu Theme Error:", e);
        }
    }
    
    // Run immediately
    applyGlobalTheme();
    
    // Expose to window for dynamic updates
    window.applyGlobalTheme = applyGlobalTheme;
});
