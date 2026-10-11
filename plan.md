
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
