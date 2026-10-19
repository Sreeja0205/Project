files = [
    "runners/gold/run_fact_sales.py",
    "runners/gold/run_fact_invoice.py",
    "runners/kpis/run_kpi_true_net_margin.py",
    "runners/kpis/run_kpi_return_cost_index.py",
    "runners/kpis/run_customer_segmentation.py",
    "streamlit/app.py"
]

for f in files:
    print(f"\n================ {f} ================")
    with open(f) as fp:
        print(fp.read())
