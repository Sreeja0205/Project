orders:
id,name,partner_id,date_order,state,amount_untaxed,amount_total,currency_id,create_date,write_date,company_id,user_id,team_id,client_order_ref,ops_order_at,ops_confirmed_at,ops_unmet_demand,ops_closed
14,S00014,"[501, ""Meier Enterprises 17850""]",2025-07-20 12:00:00,sale,125.98,132.28,"[1, ""USD""]",2026-10-07 17:50:27,2026-10-07 17:50:39,"[1, ""AlturaWave""]","[15, ""Maya""]","[6, ""Enterprise Sales""]",ECOM-536365,2025-07-20 12:00:00,2025-07-20 12:00:00,False,False
15,S00015,"[501, ""Meier Enterprises 17850""]",2025-07-20 12:02:17,sale,18.87,19.81,"[1, ""USD""]",2026-10-07 17:50:28,2026-10-07 17:52:32,"[1, ""AlturaWave""]","[17, ""Olivia Martin""]","[6, ""Enterprise Sales""]",ECOM-536366,2025-07-20 12:02:17,2025-07-20 12:02:17,False,True
16,S00016,"[802, ""Priya Vogel""]",2025-07-20 12:09:09,sale,255.07,267.82,"[1, ""USD""]",2026-10-07 17:50:28,2026-10-07 17:52:24,"[1, ""AlturaWave""]","[8, ""Ananya""]","[5, ""Online Sales""]",ECOM-536367,2025-07-20 12:09:09,2025-07-20 12:09:09,False,True
17,S00017,"[802, ""Priya Vogel""]",2025-07-20 12:09:09,sale,66.02,69.32,"[1, ""USD""]",2026-10-07 17:50:28,2026-10-07 17:51:12,"[1, ""AlturaWave""]","[11, ""Sophie Martin""]","[5, ""Online Sales""]",ECOM-536368,2025-07-20 12:09:09,2025-07-20 12:09:09,False,False

order-lines: 
id,order_id,product_id,product_uom_qty,price_unit,discount,price_subtotal,create_date,write_date,qty_delivered,qty_invoiced
1,"[14, ""S00014""]","[3538, ""[85123A] WHITE HANGING HEART T-LIGHT HOLDER""]",6.0,2.55,0.0,15.3,2026-10-07 17:50:27,2026-10-07 17:50:39,6.0,6.0
2,"[14, ""S00014""]","[2796, ""[71053] WHITE METAL LANTERN""]",6.0,3.39,10.0,18.31,2026-10-07 17:50:27,2026-10-07 17:50:39,6.0,6.0
3,"[14, ""S00014""]","[3046, ""[84406B] CREAM CUPID HEARTS COAT HANGER""]",8.0,2.75,10.0,19.8,2026-10-07 17:50:27,2026-10-07 17:50:39,8.0,8.0
4,"[14, ""S00014""]","[2987, ""[84029G] KNITTED UNION FLAG HOT WATER BOTTLE""]",6.0,3.39,15.0,17.29,2026-10-07 17:50:27,2026-10-07 17:50:39,6.0,6.0


invoices:
id,name,partner_id,invoice_origin,invoice_date,state,payment_state,amount_untaxed,amount_total,amount_residual,currency_id,create_date,write_date,move_type,company_id,ops_issued_at,ops_payment_due_at
1,HIP4/2025/07/0001,"[43, ""Serene Spa Supplies""]",P00006,2025-07-14,posted,paid,12.84,13.48,0.0,"[1, ""USD""]",2026-10-07 17:49:31,2026-10-07 17:49:33,in_invoice,"[1, ""AlturaWave""]",2025-07-14 00:00:00,2025-07-14 00:00:00
2,HIP6/2025/07/0001,"[21, ""Adorn Jewellery Ltd.""]",P00018,2025-07-14,posted,paid,13.81,14.5,0.0,"[1, ""USD""]",2026-10-07 17:49:31,2026-10-07 17:49:33,in_invoice,"[1, ""AlturaWave""]",2025-07-14 00:00:00,2025-07-14 00:00:00
3,HIP1/2025/07/0001,"[40, ""Comfort Furnishings Co.""]",P00011,2025-07-14,posted,paid,112.78,118.42,0.0,"[1, ""USD""]",2026-10-07 17:49:31,2026-10-07 17:49:33,in_invoice,"[1, ""AlturaWave""]",2025-07-14 00:00:00,2025-07-14 00:00:00
4,HIP3/2025/07/0001,"[42, ""LittleOne Supplies""]",P00003,2025-07-14,posted,paid,33.92,35.62,0.0,"[1, ""USD""]",2026-10-07 17:49:31,2026-10-07 17:49:33,in_invoice,"[1, ""AlturaWave""]",2025-07-14 00:00:00,2025-07-14 00:00:00

invoice-lines:
id,move_id,product_id,quantity,price_unit,discount,price_subtotal,sale_line_ids,create_date,write_date,company_id,purchase_line_id
1,"[1, ""HIP4/2025/07/0001""]","[381, ""[21106] CREAM SLICE FLANNEL CHOCOLATE SPOT""]",6.0,2.14,0.0,12.84,[],2026-10-07 17:49:31,2026-10-07 17:49:33,"[1, ""AlturaWave""]","[85, ""CREAM SLICE FLANNEL CHOCOLATE SPOT""]"
2,"[3, ""HIP1/2025/07/0001""]","[2739, ""[47570B] TEA TIME TABLE CLOTH""]",1.0,7.66,0.0,7.66,[],2026-10-07 17:49:31,2026-10-07 17:49:33,"[1, ""AlturaWave""]","[170, ""TEA TIME TABLE CLOTH""]"
3,"[3, ""HIP1/2025/07/0001""]","[2957, ""[82486] WOOD S/3 CABINET ANT WHITE FINISH""]",18.0,5.84,0.0,105.12,[],2026-10-07 17:49:31,2026-10-07 17:49:33,"[1, ""AlturaWave""]","[171, ""WOOD S/3 CABINET ANT WHITE FINISH""]"
4,"[2, ""HIP6/2025/07/0001""]","[608, ""[21429] RED GINGHAM ROSE JEWELLERY BOX""]",8.0,1.36,0.0,10.88,[],2026-10-07 17:49:31,2026-10-07 17:49:33,"[1, ""AlturaWave""]","[480, ""RED GINGHAM ROSE JEWELLERY BOX""]"

move-lines:

id,move_id,picking_id,product_id,quantity,location_id,location_dest_id,write_date
1,"[1, ""PLAN-PO-00001-01/21041: Vendors>Input""]","[1, ""WH/IN/00001""]","[346, ""[21041] RED RETROSPOT OVEN GLOVE DOUBLE""]",3.0,"[1, ""Vendors""]","[6, ""WH/Input""]",2026-10-07 17:49:26
2,"[2, ""PLAN-PO-00001-01/21154: Vendors>Input""]","[1, ""WH/IN/00001""]","[411, ""[21154] RED RETROSPOT OVEN GLOVE""]",200.0,"[1, ""Vendors""]","[6, ""WH/Input""]",2026-10-07 17:49:26
3,"[3, ""PLAN-PO-00001-01/21711: Vendors>Input""]","[1, ""WH/IN/00001""]","[787, ""[21711] FOLDING UMBRELLA WHITE/RED POLKADOT""]",1.0,"[1, ""Vendors""]","[6, ""WH/Input""]",2026-10-07 17:49:26
4,"[4, ""PLAN-PO-00001-01/21739: Vendors>Input""]","[1, ""WH/IN/00001""]","[808, ""[21739] COSY SLIPPER SHOES SMALL GREEN""]",3.0,"[1, ""Vendors""]","[6, ""WH/Input""]",2026-10-07 17:49:26

operation-types(complete - table):
id,name,code,warehouse_id,write_date
1,Receipts,incoming,"[1, ""My Company""]",2026-10-07 17:47:05
2,Delivery Orders,outgoing,"[1, ""My Company""]",2026-10-07 17:47:05
3,Pick,internal,"[1, ""My Company""]",2026-10-07 17:47:05
4,Pack,internal,"[1, ""My Company""]",2026-10-07 17:47:05
5,Quality Control,internal,"[1, ""My Company""]",2026-10-07 17:47:05
6,Storage,internal,"[1, ""My Company""]",2026-10-07 17:47:05
7,Internal Transfers,internal,"[1, ""My Company""]",2026-10-07 17:47:05
8,Cross Dock,internal,"[1, ""My Company""]",2026-10-07 17:47:05

products:
id,default_code,name,categ_id,uom_id,list_price,create_date,write_date,active,qty_available,virtual_available,product_tmpl_id
1,Delivery_007,Standard delivery,"[4, ""Deliveries""]","[1, ""Units""]",0.0,2026-10-07 17:46:06,2026-10-07 17:46:06,True,0.0,0.0,"[1, ""[Delivery_007] Standard delivery""]"
2,10002,INFLATABLE POLITICAL GLOBE,"[19, ""Novelty & Gadgets""]","[1, ""Units""]",0.85,2026-10-07 17:46:25,2026-10-07 17:46:25,True,74.0,164.0,"[2, ""[10002] INFLATABLE POLITICAL GLOBE""]"
3,10080,GROOVY CACTUS INFLATABLE,"[19, ""Novelty & Gadgets""]","[1, ""Units""]",0.39,2026-10-07 17:46:25,2026-10-07 17:46:25,True,0.0,0.0,"[3, ""[10080] GROOVY CACTUS INFLATABLE""]"
4,10120,DOGGY RUBBER,"[22, ""Stationery & Craft""]","[1, ""Units""]",0.21,2026-10-07 17:46:25,2026-10-07 17:46:25,True,3.0,16.0,"[4, ""[10120] DOGGY RUBBER""]"

customers:
id,ref,name,type,parent_id,commercial_partner_id,company_id,category_id,customer_rank,supplier_rank,is_company,street,street2,city,zip,state_id,country_id,email,phone,active,create_date,write_date,ops_registered_at,ops_registration_basis,x_seed_profile,x_seed_bulk_buyer,x_seed_store_candidate,user_ids,team_ids,leader_team_ids
6,CUST-GUEST-CANCEL,Unidentified Source Cancellation Customer,contact,False,"[6, ""Unidentified Source Cancellation Customer""]",False,[],1,0,False,False,False,False,False,False,False,False,False,True,2026-10-07 17:46:25,2026-10-07 17:46:25,False,False,False,False,False,[],[],[]
58,CUST-13256,Omar Khan,contact,False,"[58, ""Omar Khan""]",False,[],1,0,False,False,False,Manchester,,"[2136, ""England (GB)""]","[231, ""United Kingdom""]",omar.khan13256@example.com,+44-20-8170388,True,2026-10-07 17:47:15,2026-10-07 17:47:15,False,unknown_no_source_order,individual_training,False,False,[],[],[]
59,CUST-17846,Hugo Silva,contact,False,"[59, ""Hugo Silva""]",False,[],1,0,False,False,False,Leeds,,"[2136, ""England (GB)""]","[231, ""United Kingdom""]",hugo.silva17846@example.com,+44-20-9890641,True,2026-10-07 17:47:15,2026-10-07 17:47:15,False,unknown_no_source_order,individual_training,False,False,[],[],[]
60,CUST-PROSPECT-118289,Sam Hayes,contact,False,"[60, ""Sam Hayes""]",False,[],1,0,False,False,False,Manama,,"[2151, ""Manama (BH)""]","[23, ""Bahrain""]",prospect118289@example.com,,True,2026-10-07 17:47:15,2026-10-07 17:47:15,2025-04-21 01:40:08,synthetic_weekly_nonbuying_customer,individual_training,False,False,[],[],[]


