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
});
