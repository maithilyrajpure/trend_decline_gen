// ========================================
// CONFIGURATION
// ========================================
const API_BASE_URL = 'http://localhost:5000';

// Chart.js instances
let lifecycleChart = null;
let factorsChart = null;
let statusSparkline = null;
let platformChart = null;

// Live data update interval
let liveDataInterval = null;

// ========================================
// DOM ELEMENTS
// ========================================
const elements = {
    form: document.getElementById('trendForm'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    loadingState: document.getElementById('loadingState'),
    resultsSection: document.getElementById('resultsSection'),
    
    // Form controls
    advancedToggle: document.getElementById('advancedToggle'),
    advancedOptions: document.getElementById('advancedOptions'),
    minEngagement: document.getElementById('minEngagement'),
    minEngagementValue: document.getElementById('minEngagementValue'),
    confidenceLevel: document.getElementById('confidenceLevel'),
    confidenceLevelValue: document.getElementById('confidenceLevelValue'),
    
    // Status cards
    trendStatus: document.getElementById('trendStatus'),
    confidenceScore: document.getElementById('confidenceScore'),
    predictedTime: document.getElementById('predictedTime'),
    engagementDrop: document.getElementById('engagementDrop'),
    saturationIndex: document.getElementById('saturationIndex'),
    
    // Charts
    lifecycleCanvas: document.getElementById('lifecycleChart'),
    factorsCanvas: document.getElementById('factorsChart'),
    statusSparklineCanvas: document.getElementById('statusSparkline'),
    platformChartCanvas: document.getElementById('platformChart'),
    
    // Insights
    dataInsight: document.getElementById('dataInsight'),
    aiInsight: document.getElementById('aiInsight'),
    
    // Signals
    signalsGrid: document.getElementById('signalsGrid'),
    
    // Live trends
    decliningList: document.getElementById('decliningList'),
    risingList: document.getElementById('risingList')
};

// ========================================
// INITIALIZATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    initializeForm();
    initializeInteractiveElements();
    setDefaultDates();
    initializeLiveTrends();
    initializePlatformChart();
});

function initializeForm() {
    elements.form.addEventListener('submit', handleFormSubmit);
}

function initializeInteractiveElements() {
    // Advanced options toggle
    elements.advancedToggle.addEventListener('click', () => {
        elements.advancedToggle.classList.toggle('active');
        elements.advancedOptions.classList.toggle('active');
    });
    
    // Range sliders
    elements.minEngagement.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        elements.minEngagementValue.textContent = value.toLocaleString();
    });
    
    elements.confidenceLevel.addEventListener('input', (e) => {
        const value = e.target.value;
        elements.confidenceLevelValue.textContent = `${value}%`;
    });
    
    // Add hover effects to all inputs
    const inputs = document.querySelectorAll('.form-input, .form-select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

function setDefaultDates() {
    const today = new Date();
    const twoWeeksAgo = new Date(today);
    twoWeeksAgo.setDate(today.getDate() - 14);
    
    document.getElementById('endDate').valueAsDate = today;
    document.getElementById('startDate').valueAsDate = twoWeeksAgo;
}

// ========================================
// FORM HANDLING
// ========================================
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        keyword: document.getElementById('keyword').value,
        platform: document.getElementById('platform').value,
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value,
        analysis_depth: document.getElementById('analysisDepth').value,
        region: document.getElementById('region').value,
        min_engagement: parseInt(elements.minEngagement.value),
        confidence_level: parseInt(elements.confidenceLevel.value)
    };
    
    await analyzeTrend(formData);
}

// ========================================
// API CALL
// ========================================
async function analyzeTrend(data) {
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/analyze-trend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        updateDashboard(result);
        hideLoading();
        showResults();
        
    } catch (error) {
        console.error('Error analyzing trend:', error);
        hideLoading();
        alert('Failed to analyze trend. Please ensure the backend is running on port 5000.');
    }
}

// ========================================
// UI STATE MANAGEMENT
// ========================================
function showLoading() {
    elements.loadingState.classList.remove('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.analyzeBtn.disabled = true;
}

function hideLoading() {
    elements.loadingState.classList.add('hidden');
    elements.analyzeBtn.disabled = false;
}

function showResults() {
    elements.resultsSection.classList.remove('hidden');
    
    setTimeout(() => {
        elements.resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }, 100);
}

// ========================================
// DASHBOARD UPDATE
// ========================================
function updateDashboard(data) {
    updateStatusCards(data);
    updateCharts(data);
    updateInsights(data);
    updateSignals(data);
}

function updateStatusCards(data) {
    // Trend status with animation
    elements.trendStatus.textContent = data.trend_status;
    elements.trendStatus.style.color = getStatusColor(data.trend_status);
    elements.trendStatus.style.animation = 'fadeIn 0.5s ease';
    
    // Confidence score
    const confidencePct = (data.confidence_score * 100).toFixed(0);
    elements.confidenceScore.textContent = `${confidencePct}%`;
    
    // Predicted time
    elements.predictedTime.textContent = data.predicted_decline_time;
    
    // Engagement drop
    elements.engagementDrop.textContent = `-${data.decline_signals.engagement_drop_pct}%`;
    
    // Saturation index
    const saturation = (data.decline_signals.content_saturation_score * 100).toFixed(0);
    elements.saturationIndex.textContent = `${saturation}/100`;
    
    // Update sparkline
    updateStatusSparkline(data.lifecycle);
}

function updateCharts(data) {
    updateLifecycleChart(data.lifecycle);
    updateFactorsChart(data.feature_importance);
}

function updateInsights(data) {
    elements.dataInsight.textContent = data.explainable_reasoning;
    elements.aiInsight.textContent = data.genai_insight;
    
    // Add typing effect
    typeWriter(elements.dataInsight, data.explainable_reasoning, 20);
    setTimeout(() => {
        typeWriter(elements.aiInsight, data.genai_insight, 20);
    }, 500);
}

function updateSignals(data) {
    const signals = data.decline_signals;
    const signalsHTML = `
        <div class="signal-item">
            <div class="signal-label">Engagement Drop</div>
            <div class="signal-value">${signals.engagement_drop_pct}%</div>
            <div class="signal-bar">
                <div class="signal-bar-fill" style="width: 0%" data-width="${Math.min(signals.engagement_drop_pct, 100)}%"></div>
            </div>
        </div>
        
        <div class="signal-item">
            <div class="signal-label">Sentiment Score</div>
            <div class="signal-value">${signals.sentiment_score}</div>
            <div class="signal-bar">
                <div class="signal-bar-fill" style="width: 0%" data-width="${Math.abs(signals.sentiment_score) * 100}%"></div>
            </div>
        </div>
        
        <div class="signal-item">
            <div class="signal-label">Influencer Activity</div>
            <div class="signal-value">${(signals.influencer_activity_ratio * 100).toFixed(0)}%</div>
            <div class="signal-bar">
                <div class="signal-bar-fill" style="width: 0%" data-width="${signals.influencer_activity_ratio * 100}%"></div>
            </div>
        </div>
        
        <div class="signal-item">
            <div class="signal-label">Content Saturation</div>
            <div class="signal-value">${(signals.content_saturation_score * 100).toFixed(0)}%</div>
            <div class="signal-bar">
                <div class="signal-bar-fill" style="width: 0%" data-width="${signals.content_saturation_score * 100}%"></div>
            </div>
        </div>
    `;
    
    elements.signalsGrid.innerHTML = signalsHTML;
    
    // Animate bars with delay
    setTimeout(() => {
        document.querySelectorAll('.signal-bar-fill').forEach((bar, index) => {
            setTimeout(() => {
                bar.style.width = bar.getAttribute('data-width');
            }, index * 100);
        });
    }, 200);
}

// ========================================
// CHART CREATION
// ========================================
function updateLifecycleChart(lifecycle) {
    if (lifecycleChart) {
        lifecycleChart.destroy();
    }
    
    const ctx = elements.lifecycleCanvas.getContext('2d');
    
    lifecycleChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: lifecycle.dates,
            datasets: [
                {
                    label: 'Engagement',
                    data: lifecycle.engagement,
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#00d4ff',
                    pointBorderColor: '#0a0e14',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#00d4ff',
                    pointHoverBorderWidth: 3
                },
                {
                    label: 'Post Frequency',
                    data: lifecycle.post_frequency,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#0a0e14',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#6366f1',
                    pointHoverBorderWidth: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#8b95a5',
                        font: {
                            family: 'DM Mono',
                            size: 12
                        },
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: '#151a25',
                    titleColor: '#e6edf3',
                    bodyColor: '#8b95a5',
                    borderColor: '#232935',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    titleFont: {
                        family: 'DM Mono',
                        size: 13
                    },
                    bodyFont: {
                        family: 'DM Mono',
                        size: 12
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#232935',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#596673',
                        font: {
                            family: 'DM Mono',
                            size: 11
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#596673',
                        font: {
                            family: 'DM Mono',
                            size: 11
                        }
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

function updateFactorsChart(features) {
    if (factorsChart) {
        factorsChart.destroy();
    }
    
    const ctx = elements.factorsCanvas.getContext('2d');
    
    const labels = Object.keys(features);
    const values = Object.values(features);
    
    factorsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Importance',
                data: values,
                backgroundColor: [
                    'rgba(0, 212, 255, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    '#00d4ff',
                    '#6366f1',
                    '#f59e0b',
                    '#ef4444'
                ],
                borderWidth: 2,
                borderRadius: 6,
                hoverBackgroundColor: [
                    'rgba(0, 212, 255, 1)',
                    'rgba(99, 102, 241, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#151a25',
                    titleColor: '#e6edf3',
                    bodyColor: '#8b95a5',
                    borderColor: '#232935',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: {
                        family: 'DM Mono',
                        size: 13
                    },
                    bodyFont: {
                        family: 'DM Mono',
                        size: 12
                    },
                    callbacks: {
                        label: function(context) {
                            const value = (context.parsed.y * 100).toFixed(0);
                            return `Importance: ${value}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    grid: {
                        color: '#232935',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#596673',
                        font: {
                            family: 'DM Mono',
                            size: 11
                        },
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#596673',
                        font: {
                            family: 'DM Mono',
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

function updateStatusSparkline(lifecycle) {
    if (statusSparkline) {
        statusSparkline.destroy();
    }
    
    const ctx = elements.statusSparklineCanvas.getContext('2d');
    
    statusSparkline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: lifecycle.dates,
            datasets: [{
                data: lifecycle.engagement,
                borderColor: '#00d4ff',
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                y: { display: false },
                x: { display: false }
            }
        }
    });
}

// ========================================
// LIVE TRENDING DATA
// ========================================
function initializeLiveTrends() {
    updateLiveTrends();
    
    // Update every 30 seconds
    liveDataInterval = setInterval(updateLiveTrends, 30000);
}

function updateLiveTrends() {
    // Generate mock declining trends
    const decliningTrends = generateMockTrends('declining');
    renderTrendList(decliningTrends, elements.decliningList, 'negative');
    
    // Generate mock rising trends
    const risingTrends = generateMockTrends('rising');
    renderTrendList(risingTrends, elements.risingList, 'positive');
}

function generateMockTrends(type) {
    const hashtags = [
        '#AIArt', '#TechNews', '#Fitness2024', '#CryptoUpdate', '#FoodieLife',
        '#TravelGoals', '#StartupLife', '#Gaming', '#Fashion', '#Mindfulness',
        '#Sustainability', '#RemoteWork', '#WebDev', '#Photography', '#Music'
    ];
    
    const platforms = ['Instagram', 'TikTok', 'Twitter/X', 'LinkedIn'];
    
    const trends = [];
    for (let i = 0; i < 5; i++) {
        const randomHashtag = hashtags[Math.floor(Math.random() * hashtags.length)];
        const randomPlatform = platforms[Math.floor(Math.random() * platforms.length)];
        const change = type === 'declining' 
            ? -(Math.random() * 40 + 10).toFixed(1)
            : (Math.random() * 60 + 20).toFixed(1);
        const engagement = Math.floor(Math.random() * 500000 + 50000);
        
        trends.push({
            name: randomHashtag,
            platform: randomPlatform,
            change: change,
            engagement: engagement
        });
    }
    
    return trends;
}

function renderTrendList(trends, container, changeType) {
    const html = trends.map(trend => `
        <div class="trend-item">
            <div class="trend-info">
                <div class="trend-name">${trend.name}</div>
                <div class="trend-platform">${trend.platform}</div>
            </div>
            <div class="trend-stats">
                <div class="trend-change ${changeType}">
                    ${trend.change > 0 ? '+' : ''}${trend.change}%
                </div>
                <div class="trend-engagement">${formatNumber(trend.engagement)}</div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
    
    // Add click handlers
    container.querySelectorAll('.trend-item').forEach((item, index) => {
        item.addEventListener('click', () => {
            const trend = trends[index];
            document.getElementById('keyword').value = trend.name;
            document.getElementById('platform').value = trend.platform;
            item.style.transform = 'scale(0.95)';
            setTimeout(() => {
                item.style.transform = '';
            }, 200);
        });
    });
}

function initializePlatformChart() {
    const ctx = elements.platformChartCanvas.getContext('2d');
    
    platformChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Instagram', 'TikTok', 'Twitter/X', 'LinkedIn', 'YouTube'],
            datasets: [{
                data: [30, 25, 20, 15, 10],
                backgroundColor: [
                    'rgba(0, 212, 255, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(34, 197, 94, 0.8)'
                ],
                borderColor: [
                    '#00d4ff',
                    '#6366f1',
                    '#f59e0b',
                    '#ef4444',
                    '#22c55e'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#8b95a5',
                        font: {
                            family: 'DM Mono',
                            size: 10
                        },
                        padding: 10
                    }
                },
                tooltip: {
                    backgroundColor: '#151a25',
                    titleColor: '#e6edf3',
                    bodyColor: '#8b95a5',
                    borderColor: '#232935',
                    borderWidth: 1,
                    padding: 10,
                    titleFont: {
                        family: 'DM Mono',
                        size: 12
                    },
                    bodyFont: {
                        family: 'DM Mono',
                        size: 11
                    }
                }
            }
        }
    });
}

// ========================================
// UTILITIES
// ========================================
function getStatusColor(status) {
    const colors = {
        'Critical Decline': '#ef4444',
        'Early Decline': '#f59e0b',
        'Plateauing': '#f59e0b',
        'Growing': '#22c55e'
    };
    
    return colors[status] || '#8b95a5';
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function typeWriter(element, text, speed = 50) {
    element.textContent = '';
    let i = 0;
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (liveDataInterval) {
        clearInterval(liveDataInterval);
    }
});
