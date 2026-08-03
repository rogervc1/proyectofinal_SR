// Javascript Logic: Laptop Hybrid Recommender Dashboard

const API_BASE = ""; // Local relative paths

// State variables
let laptopsCatalog = [];
let usersList = [];

// DOM Elements
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
    // Sliders value updates
    budgetInput.addEventListener("input", (e) => {
        budgetDisplay.textContent = `${e.target.value} USD`;
    });
    
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
}

function updateMautLabel(slider, display) {
    display.textContent = `${slider.value}%`;
}

function handleUserChange() {
    const val = userSelector.value;
    if (val === "NEW_USER") {
        userProfileDesc.innerHTML = `<i class="fa-solid fa-sparkles"></i> El sistema aplicará pesos de <strong>Cold Start</strong> (60% MAUT, 30% Contenido, 10% SVD). Se apoya en reglas de negocio.`;
    } else {
        const userObj = usersList.find(u => u.user_id === val);
        const profile = userObj ? userObj.profile_name : "Usuario Recurrente";
        userProfileDesc.innerHTML = `<i class="fa-solid fa-clock-rotate-left"></i> Historial detectado. Perfil: <strong>${profile}</strong>. Ponderación dinámica activa (50% SVD colaborativo, 30% MAUT, 20% Contenido).`;
        
        // Auto-adaptar el caso de uso por UX
        if (profile.includes("Gamer")) {
            usageSelector.value = "Arquitectura / Render 3D";
            // Aumentar rendimiento y pantalla en MAUT
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
        
        // Populate select (solo 1 usuario representativo por perfil)
        let seenProfiles = new Set();
        usersList.forEach(u => {
            if (!seenProfiles.has(u.profile_name)) {
                seenProfiles.add(u.profile_name);
                const opt = document.createElement("option");
                opt.value = u.user_id;
                opt.textContent = `Perfil: ${u.profile_name} (Historial SVD)`;
                userSelector.appendChild(opt);
            }
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
        
        // Render values
        metricRmse.textContent = data.svd_rmse.toFixed(4);
        metricCsr.textContent = `${(data.csr_hybrid * 100).toFixed(1)}%`;
        metricPrecision.textContent = `${(data.precision_hybrid * 100).toFixed(2)}%`;
        
        document.getElementById("stat-ratings").textContent = `2,688 Ratings`;
    } catch (error) {
        console.error(error);
    }
}

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
    
    const payload = {
        user_id: isNew ? "U999" : userVal, // ID comodín si es nuevo
        usage_type: usageVal,
        budget: budgetVal,
        maut_weights: {
            price: parseFloat(wPrice.value),
            perf: parseFloat(wPerf.value),
            portability: parseFloat(wPortability.value),
            screen: parseFloat(wScreen.value)
        },
        is_cold_start: isNew ? true : false
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error("Error calculating recommendations");
        const data = await response.json();
        
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

// Rendering
function renderRecommendations(data) {
    const recs = data.recommendations;
    const meta = data.meta;
    
    // Update Meta Bar
    metaInfoBar.style.display = "flex";
    metaProfileType.textContent = meta.profile_type;
    metaEnsembleWeights.textContent = `α (MAUT)=${meta.weights.alpha_maut.toFixed(2)} | β (SVD)=${meta.weights.beta_svd.toFixed(2)} | γ (Contenido)=${meta.weights.gamma_content.toFixed(2)}`;
    metaPassedItems.textContent = `${meta.items_passed_rules} / ${meta.total_items_catalog} Laptops`;
    
    if (recs.length === 0) {
        recommendationsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-ban"></i>
                <p>Ningún equipo del catálogo cumple con los filtros estrictos de hardware o presupuesto configurados. Relaja los parámetros en el panel lateral.</p>
            </div>
        `;
        return;
    }
    
    recommendationsContainer.innerHTML = "";
    
    recs.forEach((laptop, index) => {
        const card = document.createElement("div");
        card.className = "laptop-card";
        
        // Badge text
        let badgeHtml = "";
        if (index === 0) {
            badgeHtml = `<div class="card-badge">Mejor Match</div>`;
        } else if (index < 3) {
            badgeHtml = `<div class="card-badge" style="background: var(--color-secondary)">Top Recomendado</div>`;
        }
        
        const mautPerc = Math.round(laptop.u_knowledge * 100);
        const svdPerc = Math.round(laptop.svd_score_norm * 100);
        const contentPerc = Math.round(laptop.s_content * 100);
        const hybridPerc = Math.round(laptop.hybrid_score * 100);
        
        card.innerHTML = `
            ${badgeHtml}
            <div class="card-header-info">
                <span class="brand-lbl">${laptop.brand}</span>
                <h3 class="laptop-name" title="${laptop.model}">${laptop.model}</h3>
                <div class="laptop-price">${laptop.price.toLocaleString()} USD</div>
            </div>
            
            <div class="card-specs">
                <div class="spec-item"><i class="fa-solid fa-microchip"></i> <span>CPU Cores: ${laptop.cpu_cores}</span></div>
                <div class="spec-item"><i class="fa-solid fa-memory"></i> <span>RAM: ${laptop.ram} GB</span></div>
                <div class="spec-item"><i class="fa-solid fa-video"></i> <span>VRAM: ${laptop.gpu_vram > 0 ? laptop.gpu_vram + ' GB' : 'Integrada'}</span></div>
                <div class="spec-item"><i class="fa-solid fa-shield-halved"></i> <span>CUDA: ${laptop.cuda_support ? 'Sí' : 'No'}</span></div>
                <div class="spec-item"><i class="fa-solid fa-weight-hanging"></i> <span>Peso: ${laptop.weight} kg</span></div>
                <div class="spec-item"><i class="fa-solid fa-expand"></i> <span>Screen: ${laptop.screen_size}"</span></div>
            </div>
            
            <div class="card-score-breakdown">
                <div class="breakdown-title">Análisis de Relevancia</div>
                
                <!-- MAUT utility -->
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>MAUT (Conocimiento)</span>
                        <span>${mautPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-maut" style="width: ${mautPerc}%"></div>
                    </div>
                </div>
                
                <!-- SVD rating -->
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>SVD (Predicción Rating: ${laptop.svd_rating_pred.toFixed(1)}★)</span>
                        <span>${svdPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-svd" style="width: ${svdPerc}%"></div>
                    </div>
                </div>
                
                <!-- Content similarity -->
                <div class="score-bar-group">
                    <div class="score-bar-lbl">
                        <span>Content Similarity</span>
                        <span>${contentPerc}%</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill fill-content" style="width: ${contentPerc}%"></div>
                    </div>
                </div>
                
                <!-- Total score -->
                <div class="total-score-box">
                    <span>Puntaje Híbrido Final:</span>
                    <span class="total-score-val">${hybridPerc}%</span>
                </div>
            </div>
        `;
        recommendationsContainer.appendChild(card);
    });
}

function renderCatalog(laptops) {
    catalogTableBody.innerHTML = "";
    
    laptops.forEach(l => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>#${l.id}</strong></td>
            <td>
                <strong>${l.brand}</strong> ${l.model.replace(l.brand + ' ', '')}
                <div class="helper-text" style="font-size:0.65rem;">CPU: ${l.cpu} | GPU: ${l.gpu}</div>
            </td>
            <td><strong class="font-blue">${l.price} USD</strong></td>
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
        return l.brand.toLowerCase().includes(query) || 
               l.model.toLowerCase().includes(query) || 
               l.cpu.toLowerCase().includes(query);
    });
    renderCatalog(filtered);
}
