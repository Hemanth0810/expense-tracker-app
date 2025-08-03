// Dashboard Chart Configuration
document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('expenseChart');
    
    if (chartCanvas) {
        // Fetch chart data
        fetch('/api/chart-data')
            .then(response => response.json())
            .then(data => {
                if (data.categories.length > 0) {
                    createExpenseChart(data);
                }
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    }
});

function createExpenseChart(data) {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    
    // Color palette for categories
    const colors = [
        '#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b',
        '#ef4444', '#ec4899', '#84cc16', '#f97316', '#6b7280'
    ];
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.categories,
            datasets: [{
                data: data.amounts,
                backgroundColor: colors.slice(0, data.categories.length),
                borderColor: '#2d2d2d',
                borderWidth: 3,
                hoverBorderWidth: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12,
                            family: "'Segoe UI', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: '#2d2d2d',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: $${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '60%',
            animation: {
                animateRotate: true,
                duration: 1000
            }
        }
    });
}
