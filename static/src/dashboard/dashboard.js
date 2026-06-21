/** @odoo-module **/
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { Component, onWillStart, useRef, useState, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ClinicDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.chartRef = useRef("trendChart");
        this.chart = null;
        this.state = useState({ data: null, loading: true });

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
            await this.loadData();
        });

        useEffect(() => {
            if (this.state.data) {
                this.renderChart();
            }
            return () => this.chart && this.chart.destroy();
        });
    }

    async loadData() {
        this.state.loading = true;
        this.state.data = await this.orm.call("clinic.dashboard", "get_dashboard_data", []);
        this.state.loading = false;
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const trend = this.state.data.week_trend;
        this.chart = new Chart(this.chartRef.el, {
            type: "bar",
            data: {
                labels: trend.map((d) => d.label),
                datasets: [{
                    label: "Appointments",
                    data: trend.map((d) => d.count),
                    backgroundColor: "#714B67",
                }],
            },
            options: {
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
            },
        });
    }

    get stateBadgeClass() {
        return {
            draft: "text-bg-secondary",
            confirmed: "text-bg-info",
            in_progress: "text-bg-warning",
            done: "text-bg-success",
            cancelled: "text-bg-danger",
        };
    }
}

ClinicDashboard.template = "clinic_dashboard.Template";
registry.category("actions").add("clinic_dashboard", ClinicDashboard);