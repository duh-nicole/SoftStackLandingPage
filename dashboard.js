const SUPABASE_URL = 'https://ltwdlbjniihlmctzcmcv.supabase.co';
const SUPABASE_KEY = 'sb_publishable_IUA8fTizYLqccuDujYTUpg_qEsB39og';

// Initialize the Supabase Client safely
const {createClient} = window.supabase;
const db = createClient(SUPABASE_URL, SUPABASE_KEY);

function escapeHTML(str) {
    if (str === null || str === undefined) return '';
    if (typeof str !== 'string') str = String(str);
    return str.replace(/[&<>'"]/g,
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}

// Modal Focus & Accessibility State
const modal = document.getElementById('inspectionModal');
const closeModalBtn = document.getElementById('closeModalBtn');
let previouslyFocusedElement = null;

function getFocusableElements(container) {
    return Array.from(
        container.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
    );
}

function handleModalFocusTrap(e) {
    if (e.key !== 'Tab') return;

    const focusables = getFocusableElements(modal);
    if (focusables.length === 0) return;

    const firstFocusable = focusables[0];
    const lastFocusable = focusables[focusables.length - 1];

    if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
        }
    } else {
        if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
        }
    }
}

function closeModal() {
    modal.style.display = 'none';
    modal.removeAttribute('aria-modal');
    modal.removeAttribute('role');

    window.removeEventListener('keydown', handleModalFocusTrap);

    // Return focus to the table row or button that triggered the modal
    if (previouslyFocusedElement && typeof previouslyFocusedElement.focus === 'function') {
        previouslyFocusedElement.focus();
    }
}

closeModalBtn.addEventListener('click', closeModal);

window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'flex') closeModal();
});

function openInspectionModal(item) {
    previouslyFocusedElement = document.activeElement;

    const name = item.client?.name || item.name || 'Anonymous';
    const company = item.client?.company || item.company;
    const companyText = company ? ` (${company})` : '';

    document.getElementById('modalClientTitle').textContent = `${name}${companyText} // Project Profile`;
    document.getElementById('modalTimeline').textContent = item.timeline || 'Unspecified';
    document.getElementById('modalVibe').textContent = `${item.creative_energy || 3} / 5 Vibe`;
    document.getElementById('modalSource').textContent = item.discovery_source || 'Direct Discovery / Unknown';
    document.getElementById('modalSummary').textContent = item.business_summary || 'No overview provided.';

    let antiFeaturesText = 'None noted!';
    if (Array.isArray(item.anti_features)) {
        antiFeaturesText = item.anti_features.join(', ');
    } else if (typeof item.anti_features === 'string') {
        antiFeaturesText = item.anti_features;
    }
    document.getElementById('modalAntiFeatures').textContent = antiFeaturesText;

    // Handle accessibility & compliance accommodations
    const complianceServices = item.compliance_services || item.access_accommodations || item.accessibility_requirements || 'No specific accommodations flagged.';
    document.getElementById('modalAccess').textContent = complianceServices;

    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.style.display = 'flex';

    // Trap focus inside modal
    window.addEventListener('keydown', handleModalFocusTrap);
    // Set focus to the close button
    closeModalBtn.setAttribute('tabindex', '0');
    closeModalBtn.setAttribute('aria-label', 'Close inspection modal');
    closeModalBtn.focus();
}

async function fetchPipelineData() {
    const rowsContainer = document.getElementById('pipelineRows');
    const totalCounter = document.getElementById('totalBriefs');

    try {
        // Fetch directly from your Supabase table
        const {data: briefs, error} = await db
            .from('public.project_briefs')
            .select('*');

        if (error) throw error;

        totalCounter.textContent = briefs.length;

        let totalValue = 0;
        briefs.forEach(item => {
            const budget = item.budget_range || '';
            if (budget.includes('$1k')) totalValue += 1000;
            else if (budget.includes('$5k')) totalValue += 5000;
            else if (budget.includes('$10k')) totalValue += 10000;
        });
        document.getElementById('pipelineValue').textContent = `$${totalValue.toLocaleString()}`;
        rowsContainer.innerHTML = '';

        if (!briefs || briefs.length === 0) {
            rowsContainer.innerHTML =
                `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No active project briefs found in the database.</td></tr>`;
            return;
        }

        briefs.forEach(item => {
            const row = document.createElement('tr');
            row.style.cursor = 'pointer';
            row.setAttribute('tabindex', '0');
            row.setAttribute('role', 'button');
            row.setAttribute('aria-label', `Inspect details for ${item.client?.name || item.name || 'Anonymous'}`);

            row.addEventListener('click', () => openInspectionModal(item));
            row.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    openInspectionModal(item);
                }
            });

            const clientName = item.client?.name || item.name || 'Anonymous';
            const clientCompany = item.client?.company || item.company;

            const safeName = escapeHTML(clientName);
            const safeCompany = clientCompany ?
                ` <span style="color: var(--text-muted); font-size: 0.85rem; display:block;">${escapeHTML(clientCompany)}</span>` : '';
            const clientInfo = safeName + safeCompany;

            const safeGoal = escapeHTML(item.primary_goal || 'Unspecified goal');
            const safeBudget = escapeHTML(item.budget_range || 'TBD');
            const safeTimeline = escapeHTML(item.timeline || 'TBD');

            let featureTagsHTML = '';
            const features = item.required_features || item.features;
            if (Array.isArray(features)) {
                featureTagsHTML = features.map(feat => `<span class="feature-tag">${escapeHTML(feat.replace(/_/g, ' '))}</span>`).join('');
            } else if (typeof features === 'string') {
                featureTagsHTML = features.split(',').map(feat => `<span class="feature-tag">${escapeHTML(feat.trim().replace(/_/g, ' '))}</span>`).join('');
            }

            if (item.has_accessibility_priority || item.accessibility_priority) {
                featureTagsHTML += `<span class="a11y-badge">♿ WCAG Priority</span>`;
            }

            row.innerHTML = `
                <td><strong>${clientInfo}</strong></td>
                <td>${safeGoal}</td>
                <td><div style="max-width: 320px; display: flex; flex-wrap: wrap;">${featureTagsHTML || '<span style="color: var(--text-muted); font-size: 0.85rem;">None</span>'}</div></td>
                <td><span style="color: var(--text-main); font-weight: 600;">${safeBudget}</span></td>
                <td>${safeTimeline}</td>
                <td><span class="badge">${escapeHTML(item.status || 'Received')}</span></td>
            `;
            rowsContainer.appendChild(row);
        });

    } catch (error) {
        console.error("Dashboard Sync Error:", error);
        rowsContainer.innerHTML =
            `<tr><td colspan="6" style="text-align: center; color: var(--primary-accent);">Pipeline sync failed. Check browser console for details.</td></tr>`;
    }
}

document.addEventListener('DOMContentLoaded', fetchPipelineData);
document.getElementById('refreshBtn').addEventListener('click', fetchPipelineData);
