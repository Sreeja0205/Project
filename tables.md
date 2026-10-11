## 1. Source-to-Target Mapping (S2T)

This mapping tracks exactly how raw data from your Bronze landing zone is transformed in the Silver layer and loaded into the Gold Fact and Dimension tables to calculate the True Margin KPIs.

| Business Requirement | Source (Bronze) | Target (Gold) | Target Field | Silver Transformation Logic |
| :--- | :--- | :--- | :--- | :--- |
| **Customer ID** | `orders.partner_id` / `invoices.partner_id` | All Fact & Dim Tables | `customer_id` | Extract numeric ID using Regex from string array (e.g., `[501, "Meier Enterprises"]` → `501`). |
| **Customer Name** | `customers.name` | `dim_customer` | `customer_name` | String standardisation (Title Case, trim whitespace). |
| **Product Cost** | `products.list_price` | `dim_product` | `unit_cost_baseline` | Cast as Decimal. Serves as COGS proxy for profit calculation. |
| **Ordered Qty** | `order-lines.product_uom_qty` | `fact_sales` | `quantity_ordered` | Cast as Integer; handle nulls as 0. |
| **Applied Discount** | `order-lines.discount` | `fact_sales` | `discount_percent` | Cast as Decimal. |
| **Discount Leakage** | Derived from `order-lines` | `fact_sales` | `discount_amount` | `(price_unit * quantity_ordered) * (discount_percent / 100)`. |
| **Billed Revenue** | `invoice-lines.price_subtotal` | `fact_revenue` | `realized_revenue` | Cast as Decimal. Filter out canceled/unpaid invoices. |
| **Return Volume** | `move-lines.quantity` | `fact_returns` | `quantity_returned` | Filter for reverse logistics (`location_dest_id` = internal warehouse). |
| **Transaction Date** | `orders.date_order` | `dim_date` | `date_key` | Convert timestamp to `YYYYMMDD` integer key format. |

---

## 2. Dimension Schemas (The Context)

Dimensions provide the slicing, filtering, and grouping context for your Streamlit dashboard.

**`dim_customer`**
Provides the grouping for the final customer segmentation.

* **`customer_key`** (Primary Key, Surrogate)
* **`customer_id`** (Business Key, extracted from source arrays)
* **`customer_name`** (String)
* **`customer_type`** (Derived from `is_company`: 'B2B' or 'B2C')
* **`segment`** (String: 'Core Profit Driver', 'Opportunistic Buyer', 'Margin Detractor' - *Updated continuously based on Fact table aggregations*)

**`dim_product`**
Provides the cost baseline and category groupings to analyze return rates.

* **`product_key`** (Primary Key, Surrogate)
* **`product_id`** (Business Key)
* **`product_name`** (String)
* **`category_id`** (Integer)
* **`unit_cost_baseline`** (Decimal, sourced from `list_price`)

**`dim_date`**
Standard calendar dimension for time-series analysis (e.g., True Net Profit Trend).

* **`date_key`** (Primary Key, Integer e.g., 20261007)
* **`full_date`** (Date)
* **`year`** (Integer)
* **`month`** (Integer)
* **`quarter`** (Integer)

---

## 3. Fact Schemas (The Action)

Following the framework's rule to keep business processes separate, we split the transactional data into three distinct Fact tables. This ensures the grain remains pure and prevents data duplication (fan-out) when joining sales intent to actual billing and returns.

**`fact_sales` (The Intent & Discount Process)**

* **Grain:** One row equals one product quoted on a single sales order line.
* **`sales_key`** (Primary Key)
* **`order_id`** (Foreign Key)
* **`customer_key`** (Foreign Key to `dim_customer`)
* **`product_key`** (Foreign Key to `dim_product`)
* **`date_key`** (Foreign Key to `dim_date`)
* **`quantity_ordered`** (Integer)
* **`unit_price`** (Decimal)
* **`discount_percent`** (Decimal)
* **`discount_amount_leakage`** (Decimal - *Calculated Measure for KPI*)

**`fact_revenue` (The Billing & Profit Process)**

* **Grain:** One row equals one product billed on a finalized, paid invoice line.
* **`revenue_key`** (Primary Key)
* **`invoice_id`** (Foreign Key)
* **`customer_key`** (Foreign Key to `dim_customer`)
* **`product_key`** (Foreign Key to `dim_product`)
* **`date_key`** (Foreign Key to `dim_date`)
* **`quantity_billed`** (Integer)
* **`realized_revenue`** (Decimal, sourced from `price_subtotal` - *Measure for KPI*)
* **`gross_profit`** (Decimal: `realized_revenue - (quantity_billed * dim_product.unit_cost_baseline)`)

**`fact_returns` (The Reverse Logistics Process)**

* **Grain:** One row equals one product physically received back into the warehouse from a customer.
* **`return_key`** (Primary Key)
* **`customer_key`** (Foreign Key to `dim_customer`)
* **`product_key`** (Foreign Key to `dim_product`)
* **`date_key`** (Foreign Key to `dim_date`)
* **`quantity_returned`** (Integer)
* **`return_cost_impact`** (Decimal: e.g., `quantity_returned * fixed_handling_fee` - *Measure for KPI*)
