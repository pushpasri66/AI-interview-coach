/**
 * AI Interview Coach - Chart.js Multimodal Analytics Visualizations
 */

document.addEventListener("DOMContentLoaded", () => {
    initAnalyticsCharts();
});

function initAnalyticsCharts() {
    // 1. Line Chart: Performance Progress Over Time
    const lineCtx = document.getElementById("progressLineChart");
    if (lineCtx) {
        new Chart(lineCtx, {
            type: "line",
            data: {
                labels: ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5"],
                datasets: [{
                    label: "Overall Performance Score",
                    data: [68, 74, 80, 84, 88],
                    borderColor: "#6366f1",
                    backgroundColor: "rgba(99, 102, 241, 0.15)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: "#818cf8"
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { min: 40, max: 100, grid: { color: "rgba(255,255,255,0.05)" } },
                    x: { grid: { color: "rgba(255,255,255,0.05)" } }
                }
            }
        });
    }

    // 2. Radar Chart: Multimodal Competencies
    const radarCtx = document.getElementById("competencyRadarChart");
    if (radarCtx) {
        new Chart(radarCtx, {
            type: "radar",
            data: {
                labels: ["Technical Depth", "HR & Behavioral", "Coding Sandbox", "Voice Quality", "Confidence", "Eye Contact"],
                datasets: [{
                    label: "Candidate Competency Profile",
                    data: [82, 88, 78, 82, 84, 90],
                    backgroundColor: "rgba(168, 85, 247, 0.25)",
                    borderColor: "#a855f7",
                    borderWidth: 2,
                    pointBackgroundColor: "#c084fc"
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: { min: 0, max: 100, grid: { color: "rgba(255,255,255,0.08)" } }
                }
            }
        });
    }

    // 3. Bar Chart: Technical Domain Proficiency
    const barCtx = document.getElementById("proficiencyBarChart");
    if (barCtx) {
        new Chart(barCtx, {
            type: "bar",
            data: {
                labels: ["Python", "SQL", "AI / ML", "Data Structures", "DBMS"],
                datasets: [{
                    label: "Proficiency Level %",
                    data: [88, 85, 80, 75, 82],
                    backgroundColor: ["#6366f1", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { min: 0, max: 100, grid: { color: "rgba(255,255,255,0.05)" } },
                    x: { grid: { color: "rgba(255,255,255,0.05)" } }
                }
            }
        });
    }

    // 4. Pie Chart: Evaluation Breakdown Distribution
    const pieCtx = document.getElementById("distributionPieChart");
    if (pieCtx) {
        new Chart(pieCtx, {
            type: "doughnut",
            data: {
                labels: ["Technical Correctness", "Relevance", "Communication", "Emotion / Composure"],
                datasets: [{
                    data: [40, 30, 20, 10],
                    backgroundColor: ["#6366f1", "#34d399", "#fbbf24", "#f43f5e"]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
}
