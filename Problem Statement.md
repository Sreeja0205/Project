This project solves the "revenue illusion," where businesses mistakenly treat high-spending customers as VIPs, even when those customers demand heavy discounts and frequently return items, ultimately costing the company money. By processing historical sales, invoicing, and inventory returns, the data pipeline calculates the actual, bottom-line profit every customer generates. This allows the business to stop wasting promotional budgets on unprofitable shoppers and start rewarding the customers who actually drive financial growth.

### Customer Segments

1. **Core Profit Drivers:** Customers who consistently generate positive net margins. They typically buy at full price, exhibit high loyalty, and have near-zero return rates. 
2. **Opportunistic Buyers:** The middle tier. They shop primarily during seasonal sales or when offered standard promotions, maintaining average order values and standard return rates that keep them moderately profitable.
3. **Margin Detractors:** The "discount abusers." They generate high top-line revenue but rely exclusively on deep discounts and have high return rates, resulting in zero or negative net profit after operational costs are factored in.

### Stakeholders and Corresponding KPIs

**Finance & Operations Leadership**
This group needs visibility into cash flow and the hidden costs of supply chain movements.

- **True Net Margin:** Total revenue per customer minus the cost of goods sold, applied discounts, and the operational cost of processing their returns.
- **Return Cost Index:** The direct financial loss incurred from reverse logistics (handling, inspecting, and restocking returned inventory from Margin Detractors).

**Sales & Account Management**
Sales teams use the Streamlit dashboard to know exactly which segment a customer belongs to during a live transaction, dictating whether they are authorized to offer a discount.

- **Discount-to-Profit Ratio:** The actual net profit generated for every dollar given away in sales negotiations.
- **Core Retention Rate:** The percentage of Core Profit Drivers successfully retained quarter-over-quarter, proving the team is focusing on the right accounts.

**Marketing & Promotions**
Marketing uses these segments to exclude Margin Detractors from targeted email blasts and reallocate that budget toward acquiring and keeping high-value clients.

- **Promo Efficiency Score:** Measures whether promotional campaigns are successfully moving Opportunistic Buyers into the Core Profit Driver category, or simply subsidizing the habits of Margin Detractors.

---

- **True Net Profit Trend (Visualized by Time):** A line chart tracking daily or weekly net profit (gross sales minus discounts and return costs). This shows whether overall business profitability is actually growing over time, rather than just top-line sales.
- **Gross Revenue vs. Net Margin (Visualized by Segment):** A grouped bar chart comparing total sales dollars against actual profit dollars across the three customer segments (Core, Opportunistic, Detractors). This starkly illustrates the "revenue illusion" by showing how the Detractor segment might have high sales but near-zero or negative profit.
- **Total Margin Leakage (Visualized by Time):** An area chart showing the daily dollar amount actively lost to applied discounts and reverse logistics (return processing). This highlights the real-time financial bleed the business is experiencing.
- **Discount Dependency Ratio (Visualized by Metric/Scatter Plot):** A scatter plot mapping customer lifetime spend (Y-axis) against their average discount percentage (X-axis). This visually clusters the "Margin Detractors" into a high-spend/high-discount corner, separate from the "Core Profit Drivers."
- **Return Volume Rate (Visualized by Product Category or Time):** A heatmap or bar chart showing the percentage of items returned. Displaying this by product category helps identify if specific items are driving the high return rates among the opportunistic and detractor segments.
