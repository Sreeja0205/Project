import json

for name in ["kpi_true_net_margin", "kpi_return_cost_index", "kpi_discount_dependency", "customer_segmentation"]:
    print(f"=== {name} ===")
    nb = json.load(open(f"notebooks/gold-to-kpi/{name}.ipynb"))
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            txt = "".join(c["source"])
            if "SparkSession" not in txt:
                print(txt)
