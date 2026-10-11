To build the "True Margin Segmenter" pipeline, you will need five core tables from your dataset. These tables contain all the necessary fields to calculate gross revenue, extract applied discount percentages, track returned quantities, and group the final metrics by customer.

Here is the exact schema mapping you will need for your Spark Dataframes:

| Table | Required Columns | Data Engineering Purpose |
| --- | --- | --- |
| **`customers`** | `id`, `name` | Acts as the primary dimension table to group final KPIs and label the segments (Core, Opportunistic, Detractors). |
| **`orders`** | `id`, `partner_id` | Serves as the bridge to link transactions to specific customers. **Spark Challenge:** The `partner_id` column contains arrays as strings (e.g., `[501, "Meier Enterprises"]`). You will need to use Spark string parsing/RegEx to extract the clean Customer ID. |
| **`order-lines`** | `order_id`, `product_id`, `product_uom_qty`, `price_unit`, `discount`, `price_subtotal` | The main fact table. You will use `price_subtotal` for actual revenue, and use `(price_unit * product_uom_qty) * (discount / 100)` to calculate the exact dollar amount of **Margin Leakage** lost to discounts. |
| **`move-lines`** | `product_id`, `quantity`, `location_id`, `location_dest_id` | Tracks the physical returns. You will filter this table for reverse movements (e.g., where `location_dest_id` contains your warehouse and `location_id` contains the customer/partner) to aggregate total returned quantities per product/customer. |
| **`products`** | `id`, `list_price` | Required to calculate the true Cost of Goods Sold (COGS). *(Note: If this specific export lacks a standard `cost` column, you can use `list_price` as a proxy baseline to calculate your Net Margin).* |

**How the Pipeline Joins Together:**

1. Clean the `partner_id` in `orders` and join it with `customers` on `id`.
2. Join `order-lines` to `orders` using `order_id` to attach a customer to every line item.
3. Join `products` to `order-lines` via `product_id` to establish the baseline value versus the discounted `price_unit`.
4. Aggregate `move-lines` by `product_id` (filtered for return locations) and join the resulting return volumes back to the customer's purchase history to calculate the **Return Volume Ratio**.
