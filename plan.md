
### The 7 Core Tables

| Table | Required Columns | Data Engineering Purpose |
| --- | --- | --- |
| **`customers`** | `id`, `name` | The primary dimension table. Used to group all financial and return metrics to individual users and label their final segment (Core, Opportunistic, or Detractor). |
| **`orders`** | `id`, `partner_id`, `date_order` | Tracks the top-level sales event. **Spark Challenge:** You must parse the `partner_id` array string (e.g., `[501, "Meier Enterprises"]`) into a clean integer to join with the `customers` table. |
| **`order-lines`** | `id`, `order_id`, `product_id`, `discount`, `product_uom_qty` | The sales fact table. Crucial for extracting the exact `discount` percentage applied at the moment of sale to calculate the **Discount Dependency Ratio** and **Margin Leakage**. |
| **`invoices`** | `id`, `partner_id`, `move_type` | The financial header table. Filters out unpaid/canceled orders and identifies refunds via the `move_type` column (e.g., standard invoice vs. credit note). |
| **`invoice-lines`** | `id`, `move_id`, `product_id`, `price_subtotal`, `sale_line_ids` | The financial fact table. Provides the true, realized gross revenue (`price_subtotal`) actually billed to the customer, rather than just what was ordered. |
| **`move-lines`** | `product_id`, `quantity`, `location_id`, `location_dest_id` | The inventory fact table. Filtered for reverse logistics (where `location_dest_id` is your warehouse) to track the physical quantity of returned items and calculate the **Return Cost Index**. |
| **`products`** | `id`, `list_price`, `categ_id` | The product dimension table. Connects to line items to provide the baseline unit cost (used to calculate **True Net Margin**) and category groupings for the **Return Volume Rate** visual. |

---

### Pipeline Joins (Medallion Architecture Logic)

**1. Clean and Standardize (Silver Layer)**

* Extract the raw Customer ID from the `partner_id` string arrays in both the `orders` and `invoices` tables using Spark regex/string manipulation.
* Filter `invoices` to only include posted/paid records, separating standard sales from refunds (`move_type`).
* Filter `move-lines` to isolate return events by selecting rows where the destination location (`location_dest_id`) is your internal warehouse and the source is external.

**2. Build the Sales & Revenue Core (Gold Layer)**

* Join **`orders`** to **`customers`** on `id = partner_id`.
* Join **`order-lines`** to **`orders`** on `order_id = id` to attach a customer to every discounted item.
* Join **`invoice-lines`** to **`invoices`** on `move_id = id` to calculate actual billed revenue per customer.
* **The Bridge Join:** Join **`invoice-lines`** to **`order-lines`** using the `sale_line_ids` array. This perfectly links the financial revenue collected to the original discount offered by the sales rep.

**3. Attach Costs & Physical Returns (Gold Layer)**

* Join **`products`** to your combined line-item table on `product_id` to establish the baseline cost of goods sold (COGS) for every transaction.
* Aggregate your filtered **`move-lines`** (returns) by `product_id` and join them against the customer's purchase history to quantify the physical return volume.

**4. Final KPI Aggregation**

* Group the entire flattened dataset by Customer `id`.
* Calculate **True Net Margin**: `SUM(invoice_lines.price_subtotal) - SUM(products.list_price * invoice_lines.quantity) - SUM(Return Processing Costs from move-lines)`.
* Apply SQL `CASE WHEN` logic to categorize each customer ID into **Core Profit Drivers**, **Opportunistic Buyers**, or **Margin Detractors** based on their aggregated margin, discount frequency, and return volume. Feed this final table directly into Streamlit.




---



1. Business Needs Drive the Pipeline
A data pipeline is useless if it doesn't answer specific questions. Before touching a database or writing a line of code, you must define:

Stakeholders & Questions: Who is using this? (e.g., Sales Managers asking, "Which customers are actually profitable after discounts and returns?").

KPIs & Formulas: The exact math behind the metrics (e.g., True Net Margin = Gross Sales - Discounts - Cost of Goods - Return Costs).

Slicing (Dimensions): How do they want to view the KPI? (e.g., Filtering by Customer Segment, by Product Category, or by Month).

2. Fact vs. Dimension Modeling
This is the blueprint for how you structure your data. You must categorize your tables into two types:

Fact Tables (The Action): These hold the measurable, transactional events that change constantly. In your project, order-lines (sales) and move-lines (returns) are facts.

Dimension Tables (The Context): These hold the descriptive attributes you use to filter or group the facts. Your customers and products tables are dimensions.

The "Grain": This is the most crucial rule in data modeling. You must define what one single row in your fact table represents. For your project, the grain is: One specific product purchased by one customer in a single transaction line.

3. The Medallion Architecture
This dictates how data physically moves, cleans itself, and transforms using Spark:

Landing/Bronze: Raw, untouched data exactly as it arrived from the source systems (your initial CSVs). It acts as a historical archive.

Silver: The cleanup zone. This is where you drop nulls, parse the messy partner_id strings into clean integers, standardise formats, and enforce data quality.

Gold: The business-ready zone. This is where you join your Facts and Dimensions together into highly aggregated, optimized tables (e.g., gold_customer_profitability) specifically designed to feed your metrics.

4. Serving the Results
The final step is connecting a visualization tool (like Streamlit) to your Gold layer.

Visual Selection: Match the chart type strictly to the KPI's intent. Use line charts for profit trends over time, and scatter plots to show the relationship between discount dependency and lifetime spend.

Zero-Computation Rule: Dashboards should not perform heavy math. All the complex joins and profit calculations must be fully completed in the Gold layer so the Streamlit dashboard loads instantly.
