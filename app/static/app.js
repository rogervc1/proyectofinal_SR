// Javascript Logic: Laptop Hybrid Recommender Dashboard (Con Monedas USD/PEN/EUR, Comparador 1vs1, Value Badges, Lifestyle Tags y Reportes)

const API_BASE = ""; // Local relative paths

// State variables
let laptopsCatalog = [];
let usersList = [];
let currentRecommendations = [];
let selectedForCompare = [];

// Multi-Currency Configuration
let currentCurrency = "USD";
const currencyRates = {
    USD: { symbol: "$", rate: 1.0, suffix: "USD" },
    PEN: { symbol: "S/", rate: 3.75, suffix: "PEN" },
    EUR: { symbol: "€", rate: 0.92, suffix: "EUR" }
};

function formatPrice(amountInUsd) {
    if (amountInUsd === undefined || amountInUsd === null || isNaN(amountInUsd)) return "-";
    const curr = currencyRates[currentCurrency] || currencyRates.USD;
    const converted = amountInUsd * curr.rate;
    // Redondear para evitar decimales flotantes como 1131.73333333
    const formatted = Math.round(converted).toLocaleString();
    return `${curr.symbol} ${formatted} ${curr.suffix}`;
}

// DOM Elements
const currencySelector = document.getElementById("currency-selector");
const userSelector = document.getElementById("user-selector");
const userProfileDesc = document.getElementById("user-profile-desc");
const usageSelector = document.getElementById("usage-selector");
const budgetInput = document.getElementById("budget-input");
const budgetDisplay = document.getElementById("budget-display");

const wPrice = document.getElementById("w-price");
const wPerf = document.getElementById("w-perf");
const wPortability = document.getElementById("w-portability");
const wScreen = document.getElementById("w-screen");

const wPriceDisplay = document.getElementById("w-price-display");
const wPerfDisplay = document.getElementById("w-perf-display");
const wPortabilityDisplay = document.getElementById("w-portability-display");
const wScreenDisplay = document.getElementById("w-screen-display");

const btnCalculate = document.getElementById("btn-calculate");
const recommendationsContainer = document.getElementById("recommendations-container");
const metaInfoBar = document.getElementById("meta-info-bar");

const metaProfileType = document.getElementById("meta-profile-type");
const metaEnsembleWeights = document.getElementById("meta-ensemble-weights");
const metaPassedItems = document.getElementById("meta-passed-items");

const catalogSearch = document.getElementById("catalog-search");
const catalogTableBody = document.querySelector("#catalog-table tbody");

const metricRmse = document.getElementById("metric-rmse");
const metricCsr = document.getElementById("metric-csr");
const metricPrecision = document.getElementById("metric-precision");

// Compare Elements
const compareBar = document.getElementById("compare-bar");
const compareCount = document.getElementById("compare-count");
const btnClearCompare = document.getElementById("btn-clear-compare");
const btnOpenCompare = document.getElementById("btn-open-compare");
const compareModal = document.getElementById("compare-modal");
const btnCloseModal = document.getElementById("btn-close-modal");
const modalCompareBody = document.getElementById("modal-compare-body");

// Export PDF Element
const btnExportPdf = document.getElementById("btn-export-pdf");

// Initialization
document.addEventListener("DOMContentLoaded", () => {
    initApp();
    setupEventListeners();
});

function initApp() {
    // 1. Fetch catalog
    fetchLaptopsCatalog();
    
    // 2. Fetch users
    fetchUsersList();
    
    // 3. Fetch metrics
    fetchEvaluationMetrics();
}

function setupEventListeners() {
    // Currency Selector Listener
    if (currencySelector) {
        currencySelector.addEventListener("change", (e) => {
            currentCurrency = e.target.value;
            updateBudgetDisplay();
            if (currentRecommendations.length > 0) {
                renderRecommendations({ recommendations: currentRecommendations, meta: currentRecommendationsMeta });
            }
            if (laptopsCatalog.length > 0) {
                renderCatalog(laptopsCatalog);
            }
        });
    }

    // Sliders value updates
    budgetInput.addEventListener("input", updateBudgetDisplay);
    
    wPrice.addEventListener("input", (e) => updateMautLabel(wPrice, wPriceDisplay));
    wPerf.addEventListener("input", (e) => updateMautLabel(wPerf, wPerfDisplay));
    wPortability.addEventListener("input", (e) => updateMautLabel(wPortability, wPortabilityDisplay));
    wScreen.addEventListener("input", (e) => updateMautLabel(wScreen, wScreenDisplay));
    
    // User selector change -> Updates description and adjusts defaults
    userSelector.addEventListener("change", handleUserChange);
    
    // Tabs switching
    const tabButtons = document.querySelectorAll(".tab-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            const targetTab = btn.getAttribute("data-tab");
            document.querySelectorAll(".tab-content").forEach(tc => tc.classList.remove("active"));
            document.getElementById(targetTab).classList.add("active");
        });
    });
    
    // Recommendation trigger
    btnCalculate.addEventListener("click", getRecommendations);
    
    // Catalogue search
    catalogSearch.addEventListener("input", filterCatalog);

    // Compare Bar Listeners
    btnClearCompare.addEventListener("click", clearCompare);
    btnOpenCompare.addEventListener("click", openCompareModal);
    btnCloseModal.addEventListener("click", () => compareModal.style.display = "none");
    
    // Export PDF
    if (btnExportPdf) {
        btnExportPdf.addEventListener("click", () => window.print());
    }

    // Close modal on click outside
    window.addEventListener("click", (e) => {
        if (e.target === compareModal) {
            compareModal.style.display = "none";
        }
    });
}

function updateBudgetDisplay() {
    const valInUsd = parseFloat(budgetInput.value);
    budgetDisplay.textContent = formatPrice(valInUsd);
}

function updateMautLabel(slider, display) {
    display.textContent = `${slider.value}%`;
}

function handleUserChange() {
    const val = userSelector.value;
    if (val === "NEW_USER") {
        userProfileDesc.innerHTML = `<i class="fa-solid fa-user-plus"></i> <strong>Usuario Nuevo (Cold Start):</strong> Sin historial de valoraciones en la plataforma. Se aplican pesos de regla (60% MAUT, 30% Contenido, 10% SVD).`;
    } else {
        const userObj = usersList.find(u => u.user_id === val);
        const profile = userObj ? userObj.profile_name : "Estudiante / Oficina";
        const desc = userObj ? userObj.profile_description : "Perfil de usuario estándar.";
        userProfileDesc.innerHTML = `<i class="fa-solid fa-user-check"></i> <strong>Usuario ${val} (${profile}):</strong> ${desc} Ponderación activa: 50% SVD Colaborativo, 30% MAUT, 20% Contenido.`;
        
        // Auto-adaptar el caso de uso por UX
        if (profile.includes("Gamer")) {
            usageSelector.value = "Arquitectura / Render 3D";
            wPerf.value = 50; wPrice.value = 10; wPortability.value = 10; wScreen.value = 30;
        } else if (profile.includes("IA") || profile.includes("Datos")) {
            usageSelector.value = "Deep Learning";
            wPerf.value = 60; wPrice.value = 10; wPortability.value = 10; wScreen.value = 20;
        } else {
            usageSelector.value = "Uso de Oficina / Estudiante";
            wPrice.value = 40; wPortability.value = 30; wPerf.value = 15; wScreen.value = 15;
        }
        // Actualizar displays
        updateMautLabel(wPrice, wPriceDisplay);
        updateMautLabel(wPerf, wPerfDisplay);
        updateMautLabel(wPortability, wPortabilityDisplay);
        updateMautLabel(wScreen, wScreenDisplay);
    }
}

// API Calls
async function fetchLaptopsCatalog() {
    try {
        const response = await fetch(`${API_BASE}/api/laptops`);
        if (!response.ok) throw new Error("Error fetching laptops catalog");
        laptopsCatalog = await response.json();
        renderCatalog(laptopsCatalog);
        document.getElementById("stat-laptops").textContent = `${laptopsCatalog.length} Laptops`;
        document.getElementById("catalog-count").textContent = laptopsCatalog.length;
    } catch (error) {
        console.error(error);
    }
}

async function fetchUsersList() {
    try {
        const response = await fetch(`${API_BASE}/api/users`);
        if (!response.ok) throw new Error("Error fetching users list");
        usersList = await response.json();
        
        userSelector.innerHTML = '<option value="NEW_USER" selected>Usuario Nuevo (Cold Start)</option>';
        
        usersList.forEach(u => {
            const opt = document.createElement("option");
            opt.value = u.user_id;
            opt.textContent = `Usuario ${u.user_id} - ${u.profile_name}`;
            userSelector.appendChild(opt);
        });
    } catch (error) {
        console.error(error);
    }
}

async function fetchEvaluationMetrics() {
    try {
        const response = await fetch(`${API_BASE}/api/metrics`);
        if (!response.ok) throw new Error("Error fetching metrics");
        const data = await response.json();
        
        metricRmse.textContent = data.svd_rmse.toFixed(4);
        metricCsr.textContent = `${(data.csr_hybrid * 100).toFixed(1)}%`;
        metricPrecision.textContent = `${(data.precision_hybrid * 100).toFixed(2)}%`;
        
        document.getElementById("stat-ratings").textContent = `1,999 Ratings`;
    } catch (error) {
        console.error(error);
    }
}

let currentRecommendationsMeta = null;

async function getRecommendations() {
    recommendationsContainer.innerHTML = `
        <div class="loading-state">
            <i class="fa-solid fa-spinner"></i>
            <p>Calculando matrices latentes, filtros en cascada y ensamble dinámico...</p>
        </div>
    `;
    metaInfoBar.style.display = "none";
    
    const userVal = userSelector.value;
    const isNew = userVal === "NEW_USER";
    const budgetVal = parseFloat(budgetInput.value);
    const usageVal = usageSelector.value;
    
    const checkedTags = Array.from(document.querySelectorAll(".tag-input:checked")).map(cb => cb.value);

    const payload = {
        user_id: isNew ? "U999" : userVal,
        usage_type: usageVal,
        budget: budgetVal,
        maut_weights: {
            price: parseFloat(wPrice.value),
            perf: parseFloat(wPerf.value),
            portability: parseFloat(wPortability.value),
            screen: parseFloat(wScreen.value)
        },
        is_cold_start: isNew ? true : false,
        lifestyle_tags: checkedTags
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error("Error calculating recommendations");
        const data = await response.json();
        
        currentRecommendations = data.recommendations;
        currentRecommendationsMeta = data.meta;
        renderRecommendations(data);
    } catch (error) {
        recommendationsContainer.innerHTML = `
            <div class="empty-state font-danger">
                <i class="fa-solid fa-circle-exclamation"></i>
                <p>Ocurrió un error al calcular las recomendaciones: ${error.message}</p>
            </div>
        `;
    }
}

// Rendering Recommendations
function renderRecommendations(data) {
    const recs = data.recommendations;
    const meta = data.meta;
    
    metaInfoBar.style.display = "flex";
    metaProfileType.textContent = meta.profile_type;
    metaEnsembleWeights.textContent = `α (MAUT)=${meta.weights.alpha_maut.toFixed(2)} | β (SVD)=${meta.weights.beta_svd.toFixed(2)} | γ (Contenido)=${meta.weights.gamma_content.toFixed(2)}`;
    metaPassedItems.textContent = `${meta.items_passed_rules} / ${meta.total_items_catalog} Laptops`;
    
    if (recs.length === 0) {
        recommendationsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-ban"></i>
                <p>Ningún equipo del catálogo cumple con los filtros estrictos de hardware, presupuesto o etiquetas configuradas. Relaja los parámetros en el panel lateral.</p>
            </div>
        `;
        return;
    }
    
    recommendationsContainer.innerHTML = "";
    
    recs.forEach((laptop, index) => {
        const card = document.createElement("div");
        card.className = "laptop-card";
        
        let badgeHtml = "";
        if (index === 0) {
            badgeHtml = `<div class="card-badge">Mejor Match</div>`;
        } else if (index < 3) {
            badgeHtml = `<div class="card-badge" style="background: var(--color-secondary)">Top Recomendado</div>`;
        }
        
        const laptopBrand = laptop.brand || (laptop.name ? laptop.name.split(' ')[0] : 'Laptop');
        const laptopModel = laptop.model || laptop.name || `${laptopBrand} Ultrabook`;
        const fallbackQuery = encodeURIComponent(`laptop ${laptopBrand} ${laptopModel}`);
        
        const amazonUrl = (laptop.amazon_url && laptop.amazon_url !== 'undefined' && laptop.amazon_url !== 'null' && laptop.amazon_url !== '') 
            ? laptop.amazon_url 
            : `https://www.amazon.com/s?k=${fallbackQuery}`;
            
        const buyUrl = (laptop.buy_url && laptop.buy_url !== 'undefined' && laptop.buy_url !== 'null' && laptop.buy_url !== '') 
            ? laptop.buy_url 
            : amazonUrl;
            
        const bestStore = (laptop.best_store && laptop.best_store !== 'undefined' && laptop.best_store !== 'null' && laptop.best_store !== '') 
            ? laptop.best_store 
            : 'Amazon.com';

        let valBadgeClass = "badge-fair-price";
        if (laptop.value_tag === "Top Calidad/Precio") valBadgeClass = "badge-top-value";
        else if (laptop.value_tag === "Gama Premium") valBadgeClass = "badge-premium";
        
        const mautPerc = Math.round((laptop.u_knowledge || 0) * 100);
        const svdPerc = Math.round((laptop.svd_score_norm || 0) * 100);
        const contentPerc = Math.round((laptop.s_content || 0) * 100);
        const hybridPerc = Math.round((laptop.hybrid_score || 0) * 100);
        
        const isChecked = selectedForCompare.some(item => item.id === laptop.id);
        
        card.innerHTML = `
            ${badgeHtml}
            
            <label class="card-compare-check">
                <input type="checkbox" class="compare-chk" data-id="${laptop.id}" ${isChecked ? 'checked' : ''}>
                <span>Comparar</span>
            </label>

            <div class="card-header-info" style="margin-top: 15px;">
                <span class="brand-lbl">${laptopBrand}</span>
                <h3 class="laptop-name" title="${laptopModel}">${laptopModel}</h3>
                <div class="laptop-price">${formatPrice(laptop.price)}</div>
                <span class="value-badge ${valBadgeClass}">${laptop.value_tag || 'Precio Justo'}</span>
            </div>
            
            <div class="card-specs">
                <div class="spec-item"><i class="fa-solid fa-microchip"></i> <span>CPU Cores: ${laptop.cpu_cores || '-'}</span></div>
                <div class="spec-item"><i class="fa-solid fa-memory"></i> <span>RAM: ${laptop.ram || '-'} GB</span></div>
                <div class="spec-item"><i class="fa-solid fa-video"></i> <span>VRAM: ${laptop.gpu_vram > 0 ? laptop.gpu_vram + ' GB' : 'Integrada'}</span></div>
                <div class="spec-item"><i class="fa-solid fa-shield-halved"></i> <span>CUDA: ${laptop.cuda_support ? 'Sí' : 'No'}</span></div>
                <div class="spec-item"><i class="fa-solid fa-weight-hanging"></i> <span>Peso: ${laptop.weight || '-'} kg</span></div>
                <div class="spec-item"><i class="fa-solid fa-expand"></i> <span>Screen: ${laptop.screen_size || '-'}</span></div>
            </div>
            
            <div class="card-score-breakdown">
                <div class="breakdown-title">Análisis de Relevancia Híbrida</div>
                
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>MAUT (Conocimiento)</span>
                        <span>${mautPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-maut" style="width: ${mautPerc}%"></div>
                    </div>
                </div>
                
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>SVD (Predicción Rating: ${laptop.svd_rating_pred ? laptop.svd_rating_pred.toFixed(1) : '3.0'} / 5.0)</span>
                        <span>${svdPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-svd" style="width: ${svdPerc}%"></div>
                    </div>
                </div>
                
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>Content Similarity</span>
                        <span>${contentPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-content" style="width: ${contentPerc}%"></div>
                    </div>
                </div>
                
                <div class="total-score-box">
                    <span>Puntaje Híbrido Final:</span>
                    <span class="total-score-val">${hybridPerc}%</span>
                </div>
            </div>

            <div class="card-store-bar">
                <div class="store-actions">
                    <a href="${amazonUrl}" target="_blank" rel="noopener noreferrer" class="buy-link-amazon" title="Ver oferta en Amazon.com">
                        <i class="fa-brands fa-amazon"></i> Amazon
                    </a>
                    ${bestStore !== 'Amazon.com' ? `<a href="${buyUrl}" target="_blank" rel="noopener noreferrer" class="buy-link-store" title="Ver oferta en ${bestStore}"><i class="fa-solid fa-store"></i> ${bestStore}</a>` : ''}
                </div>
                <div class="store-name">
                    <button class="btn-trend-modal" data-id="${laptop.id}" title="Ver gráfica interactiva de tendencia de precios">
                        <i class="fa-solid fa-chart-line font-green"></i> Gráfica de Precios
                    </button>
                </div>
            </div>
        `;
        recommendationsContainer.appendChild(card);
    });

    document.querySelectorAll(".compare-chk").forEach(chk => {
        chk.addEventListener("change", handleCompareCheck);
    });
    
    document.querySelectorAll(".btn-trend-modal").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const id = parseInt(e.currentTarget.getAttribute("data-id"));
            const laptop = currentRecommendations.find(l => l.id === id) || laptopsCatalog.find(l => l.id === id);
            if (laptop) openPriceChartModal(laptop);
        });
    });
}

function handleCompareCheck(e) {
    const laptopId = parseInt(e.target.getAttribute("data-id"));
    const laptopObj = currentRecommendations.find(l => l.id === laptopId);

    if (e.target.checked) {
        if (selectedForCompare.length >= 2) {
            alert("Solo puedes seleccionar hasta 2 laptops para la comparativa cara a cara (1vs1).");
            e.target.checked = false;
            return;
        }
        if (laptopObj && !selectedForCompare.some(l => l.id === laptopId)) {
            selectedForCompare.push(laptopObj);
        }
    } else {
        selectedForCompare = selectedForCompare.filter(l => l.id !== laptopId);
    }

    updateCompareBar();
}

function updateCompareBar() {
    if (selectedForCompare.length > 0) {
        compareBar.style.display = "flex";
        compareCount.textContent = selectedForCompare.length;
    } else {
        compareBar.style.display = "none";
    }
}

function clearCompare() {
    selectedForCompare = [];
    document.querySelectorAll(".compare-chk").forEach(chk => chk.checked = false);
    updateCompareBar();
}

function openCompareModal() {
    if (selectedForCompare.length < 2) {
        alert("Por favor selecciona 2 laptops para realizar la comparativa 1vs1.");
        return;
    }

    const l1 = selectedForCompare[0];
    const l2 = selectedForCompare[1];

    const l1Score = Math.round(l1.hybrid_score * 100);
    const l2Score = Math.round(l2.hybrid_score * 100);

    const l1Win = l1Score >= l2Score;
    const l2Win = l2Score > l1Score;

    let verdict = "";
    if (l1Win) {
        verdict = `<strong>Veredicto del recomendador:</strong> <strong>${l1.model}</strong> obtiene el puntaje híbrido más alto (${l1Score}% vs ${l2Score}%). `;
        if (l1.ram > l2.ram) verdict += `Ofrece más memoria RAM (${l1.ram}GB vs ${l2.ram}GB). `;
        if (l1.cpu_cores > l2.cpu_cores) verdict += `Posee más núcleos CPU (${l1.cpu_cores} vs ${l2.cpu_cores}). `;
        if (l1.weight < l2.weight) verdict += `Es más liviana (${l1.weight}kg vs ${l2.weight}kg). `;
    } else {
        verdict = `<strong>Veredicto del recomendador:</strong> <strong>${l2.model}</strong> supera en relevancia general (${l2Score}% vs ${l1Score}%). `;
        if (l2.ram > l1.ram) verdict += `Ofrece más memoria RAM (${l2.ram}GB vs ${l1.ram}GB). `;
        if (l2.cpu_cores > l1.cpu_cores) verdict += `Posee más núcleos CPU (${l2.cpu_cores} vs ${l1.cpu_cores}). `;
        if (l2.weight < l1.weight) verdict += `Es más ligera (${l2.weight}kg vs ${l1.weight}kg). `;
    }

    modalCompareBody.innerHTML = `
        <div class="compare-grid">
            <div class="compare-laptop-card ${l1Win ? 'compare-winner' : ''}">
                ${l1Win ? '<span class="value-badge badge-top-value" style="margin-bottom:8px;">Ganador 1vs1</span>' : ''}
                <h3 style="font-family:var(--font-heading); font-size:1.2rem;">${l1.model}</h3>
                <div class="laptop-price" style="margin-bottom:6px;">${formatPrice(l1.price)}</div>
                <small style="color:var(--color-success); display:block; margin-bottom:12px;">${l1.price_trend_tag || ''}</small>

                <table class="catalog-table" style="font-size:0.8rem;">
                    <tr><th>Puntaje Híbrido</th><td class="${l1Score >= l2Score ? 'win-spec' : ''}"><strong>${l1Score}%</strong></td></tr>
                    <tr><th>CPU Cores</th><td class="${l1.cpu_cores >= l2.cpu_cores ? 'win-spec' : ''}">${l1.cpu_cores} núcleos</td></tr>
                    <tr><th>RAM</th><td class="${l1.ram >= l2.ram ? 'win-spec' : ''}">${l1.ram} GB</td></tr>
                    <tr><th>GPU VRAM</th><td class="${l1.gpu_vram >= l2.gpu_vram ? 'win-spec' : ''}">${l1.gpu_vram > 0 ? l1.gpu_vram + ' GB' : 'Integrada'}</td></tr>
                    <tr><th>Peso</th><td class="${l1.weight <= l2.weight ? 'win-spec' : ''}">${l1.weight} kg</td></tr>
                    <tr><th>Mínimo Histórico</th><td class="font-green">${formatPrice(l1.historical_low || l1.price)}</td></tr>
                    <tr><th>Promedio Histórico</th><td>${formatPrice(l1.historical_avg || l1.price)}</td></tr>
                    <tr><th>Oferta Amazon</th><td><a href="${l1.amazon_url}" target="_blank" rel="noopener noreferrer" class="buy-link-amazon"><i class="fa-brands fa-amazon"></i> Ir a Amazon</a></td></tr>
                </table>
            </div>

            <div class="compare-laptop-card ${l2Win ? 'compare-winner' : ''}">
                ${l2Win ? '<span class="value-badge badge-top-value" style="margin-bottom:8px;">Ganador 1vs1</span>' : ''}
                <h3 style="font-family:var(--font-heading); font-size:1.2rem;">${l2.model}</h3>
                <div class="laptop-price" style="margin-bottom:6px;">${formatPrice(l2.price)}</div>
                <small style="color:var(--color-success); display:block; margin-bottom:12px;">${l2.price_trend_tag || ''}</small>

                <table class="catalog-table" style="font-size:0.8rem;">
                    <tr><th>Puntaje Híbrido</th><td class="${l2Score >= l1Score ? 'win-spec' : ''}"><strong>${l2Score}%</strong></td></tr>
                    <tr><th>CPU Cores</th><td class="${l2.cpu_cores >= l1.cpu_cores ? 'win-spec' : ''}">${l2.cpu_cores} núcleos</td></tr>
                    <tr><th>RAM</th><td class="${l2.ram >= l1.ram ? 'win-spec' : ''}">${l2.ram} GB</td></tr>
                    <tr><th>GPU VRAM</th><td class="${l2.gpu_vram >= l1.gpu_vram ? 'win-spec' : ''}">${l2.gpu_vram > 0 ? l2.gpu_vram + ' GB' : 'Integrada'}</td></tr>
                    <tr><th>Peso</th><td class="${l2.weight <= l1.weight ? 'win-spec' : ''}">${l2.weight} kg</td></tr>
                    <tr><th>Mínimo Histórico</th><td class="font-green">${formatPrice(l2.historical_low || l2.price)}</td></tr>
                    <tr><th>Promedio Histórico</th><td>${formatPrice(l2.historical_avg || l2.price)}</td></tr>
                    <tr><th>Oferta Amazon</th><td><a href="${l2.amazon_url}" target="_blank" rel="noopener noreferrer" class="buy-link-amazon"><i class="fa-brands fa-amazon"></i> Ir a Amazon</a></td></tr>
                </table>
            </div>
        </div>

        <div class="compare-verdict-box">
            <i class="fa-solid fa-circle-check font-green"></i> ${verdict}
        </div>
    `;

    compareModal.style.display = "flex";
}

// Render Catalog
function renderCatalog(laptops) {
    catalogTableBody.innerHTML = "";
    
    laptops.forEach(l => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>#${l.id}</strong></td>
            <td>
                <strong>${l.brand}</strong> ${l.model ? l.model.replace(l.brand + ' ', '') : ''}
                <div class="helper-text" style="font-size:0.65rem;">CPU: ${l.cpu} | GPU: ${l.gpu}</div>
            </td>
            <td><strong class="font-blue">${formatPrice(l.price)}</strong></td>
            <td>${l.cpu_cores} núcleos</td>
            <td>${l.ram} GB</td>
            <td>${l.gpu_vram > 0 ? l.gpu_vram + ' GB VRAM' : 'Integrada'}</td>
            <td>${l.cuda_support ? '<span class="font-green"><i class="fa-solid fa-circle-check"></i> Sí</span>' : '<span class="text-muted">No</span>'}</td>
            <td>${l.weight} kg</td>
            <td>${l.screen_size}" (${l.screen_resolution})</td>
        `;
        catalogTableBody.appendChild(tr);
    });
}

function filterCatalog() {
    const query = catalogSearch.value.toLowerCase();
    const filtered = laptopsCatalog.filter(l => {
        return (l.brand && l.brand.toLowerCase().includes(query)) || 
               (l.model && l.model.toLowerCase().includes(query)) || 
               (l.cpu && l.cpu.toLowerCase().includes(query));
    });
    renderCatalog(filtered);
}

// Chart.js Price Trend Modal Logic
let priceChartInstance = null;
const priceModal = document.getElementById("price-modal");
const btnClosePriceModal = document.getElementById("btn-close-price-modal");

if (btnClosePriceModal) {
    btnClosePriceModal.addEventListener("click", () => {
        if (priceModal) priceModal.style.display = "none";
    });
}

function openPriceChartModal(laptop) {
    if (!priceModal) return;
    
    document.getElementById("price-modal-title").textContent = `Histórico de Precios: ${laptop.model || laptop.name}`;
    
    let seriesUsd = [laptop.price * 1.1, laptop.price * 1.05, laptop.price * 1.02, laptop.price * 1.0, laptop.price * 0.98, laptop.price];
    if (laptop.price_history_json) {
        try {
            seriesUsd = typeof laptop.price_history_json === 'string' ? JSON.parse(laptop.price_history_json) : laptop.price_history_json;
        } catch (e) {
            console.error(e);
        }
    }
    
    const curr = currencyRates[currentCurrency] || currencyRates.USD;
    const seriesConverted = seriesUsd.map(val => Math.round(val * curr.rate));

    const minVal = Math.min(...seriesUsd);
    const maxVal = Math.max(...seriesUsd);
    const avgVal = Math.round(seriesUsd.reduce((a, b) => a + b, 0) / seriesUsd.length);
    
    document.getElementById("price-modal-metrics").innerHTML = `
        <div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 15px;">
            <div class="metric-card card-glass" style="padding:12px;">
                <span class="meta-lbl">Precio Actual</span>
                <span class="val-display font-blue" style="font-size:1.2rem;">${formatPrice(laptop.price)}</span>
            </div>
            <div class="metric-card card-glass" style="padding:12px;">
                <span class="meta-lbl">Mínimo Histórico</span>
                <span class="val-display font-green" style="font-size:1.2rem;">${formatPrice(minVal)}</span>
            </div>
            <div class="metric-card card-glass" style="padding:12px;">
                <span class="meta-lbl">Máximo Histórico</span>
                <span class="val-display font-purple" style="font-size:1.2rem;">${formatPrice(maxVal)}</span>
            </div>
            <div class="metric-card card-glass" style="padding:12px;">
                <span class="meta-lbl">Promedio 6 Meses</span>
                <span class="val-display" style="font-size:1.2rem; color:var(--text-primary);">${formatPrice(avgVal)}</span>
            </div>
        </div>
    `;

    priceModal.style.display = "flex";

    const ctx = document.getElementById("priceTrendCanvas").getContext("2d");
    if (priceChartInstance) {
        priceChartInstance.destroy();
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.35)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

    priceChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto'],
            datasets: [{
                label: `Precio (${curr.suffix})`,
                data: seriesConverted,
                borderColor: '#10b981',
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.35,
                pointBackgroundColor: '#34d399',
                pointBorderColor: '#ffffff',
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f3f4f6', font: { family: 'Outfit', size: 12 } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` Precio: ${curr.symbol} ${context.parsed.y.toLocaleString()} ${curr.suffix}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#9ca3af',
                        callback: function(value) { return curr.symbol + ' ' + value.toLocaleString(); }
                    }
                }
            }
        }
    });
}
