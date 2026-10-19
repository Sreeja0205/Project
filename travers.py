import json

for path in [
    "notebooks/gold-to-kpi/kpi_true_net_margin.ipynb",
    "notebooks/gold-to-kpi/kpi_return_cost_index.ipynb",
    "notebooks/gold-to-kpi/kpi_discount_dependency.ipynb",
    "notebooks/silver-to-gold/fact_sales.ipynb",
    "notebooks/silver-to-gold/fact_invoice.ipynb"
]:
    print(f"\n================ {path} ================")
    nb = json.load(open(path))
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            # Skip the first 18 lines of SparkSession config so it fits on screen!
            lines = c["source"]
            print("".join(lines[18:] if len(lines) > 18 else lines))
