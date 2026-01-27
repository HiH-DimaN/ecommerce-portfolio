'use strict';

const ChartsModule = {
    instances: {},
    
    config: {
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
        fontSize: 12,
        animationDuration: 2000,
        colors: {
            primary: '#1A73E8',
            primaryLight: 'rgba(26, 115, 232, 0.1)',
            success: '#34A853',
            successLight: 'rgba(52, 168, 83, 0.1)',
            error: '#EA4335',
            errorLight: 'rgba(234, 67, 53, 0.1)',
            warning: '#FBBC04',
            warningLight: 'rgba(251, 188, 4, 0.1)',
            gray: '#DADCE0',
            grayLight: '#F8F9FA',
            text: '#202124',
            textSecondary: '#5F6368'
        }
    },

    init() {
        if (typeof Chart === 'undefined') return;
        this.setGlobalDefaults();
        try {
            this.createSalesChart();
            this.createRevenueChart();
            this.createSpeedChart();
        } catch (error) {
            console.error('[Charts] Init error:', error);
        }
    },

    setGlobalDefaults() {
        Chart.defaults.font.family = this.config.fontFamily;
        Chart.defaults.font.size = this.config.fontSize;
        Chart.defaults.color = this.config.colors.textSecondary;
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.plugins.legend.position = 'bottom';
        Chart.defaults.plugins.legend.labels.usePointStyle = true;
        Chart.defaults.plugins.legend.labels.padding = 15;
    },

    createSalesChart() {
        const canvas = document.getElementById('chart-sales');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(26, 115, 232, 0.3)');
        gradient.addColorStop(1, 'rgba(26, 115, 232, 0.01)');

        this.instances.sales = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['ДО', 'Дни 1-7', 'Дни 8-14', 'Дни 15-21', 'Дни 22-30', 'ПОСЛЕ'],
                datasets: [{
                    label: 'Продажи (шт/день)',
                    data: [22, 22, 23, 25, 28, 30],
                    borderColor: this.config.colors.primary,
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5
                }]
            },
            options: {
                scales: {
                    y: { 
                        min: 18, 
                        max: 35,
                        ticks: { callback: (val) => val + ' шт' }
                    }
                }
            }
        });
    },

    createRevenueChart() {
        const canvas = document.getElementById('chart-revenue');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        // Выручка: ДО 2 млн/мес (67к/день), ПОСЛЕ 2.7 млн/мес (90к/день)
        // Дни 1-7: подготовка (без изменений)
        // Дни 8-21: внедрение (10% аудитории, обучение, регламенты) — плавный рост
        // После дня 21: полномасштабный запуск — выход на 2.7 млн
        this.instances.revenue = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['ДО', 'Дни 1-7', 'Дни 8-14', 'Дни 15-21', 'Дни 22-30', 'ПОСЛЕ'],
                datasets: [{
                    label: 'Выручка (тыс. ₽/день)',
                    data: [67, 67, 70, 75, 85, 90],
                    backgroundColor: [
                        this.config.colors.error,
                        this.config.colors.gray,
                        this.config.colors.warning,
                        this.config.colors.warning,
                        'rgba(52, 168, 83, 0.7)',
                        this.config.colors.success
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            afterLabel: (context) => {
                                const phases = ['Базовый уровень', 'Подготовка', 'Запуск 10%', 'Обучение и регламенты', 'Полный запуск', 'Стабильный результат'];
                                return phases[context.dataIndex];
                            }
                        }
                    }
                },
                scales: {
                    y: { 
                        beginAtZero: false,
                        min: 50,
                        max: 100,
                        ticks: { callback: (val) => val + 'к ₽' }
                    }
                }
            }
        });
    },

    createSpeedChart() {
        const canvas = document.getElementById('chart-speed');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        this.instances.speed = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['ПОСЛЕ (30 сек)', 'ДО (30 мин)', 'Экономия'],
                datasets: [{
                    data: [0.5, 30, 30],
                    backgroundColor: [
                        this.config.colors.success,
                        this.config.colors.error,
                        this.config.colors.grayLight
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                cutout: '70%',
                rotation: -90,
                circumference: 180,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => ChartsModule.init(), 200);
});
