# Entity Relationship Diagram (ER)

This document contaions the ER diagram for the Retail Customer Segmentation & Loyalty database. The design models customers, campaigns, purchasing behaviors, and household compositions.

## Entities
- CUSTOMER
- CUSTOMER_PROFILE
- CAMPAIGN
- CUSTOMER_CAMPAIGN (Associative)
- CUSTOMER_CHILD (Weak)

## Relationships
- CUSTOMER to CUSTOMER_PROFILE (1-to-1)
- CUSTOMER to CUSTOMER_CHILD (1-to-many)
- CUSTOMER to CAMPAIGN (many-to-many)

## Revised ER Diagram
<img width="763" height="334" alt="image" src="https://github.com/user-attachments/assets/737548bc-7c38-44a3-bb75-4cc9251bc1c7" />

