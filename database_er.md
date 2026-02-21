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

## ER Diagram
<img width="721" height="324" alt="er_part_b" src="https://github.com/user-attachments/assets/8d126683-89e0-4d1c-84aa-bad421e6b905" />
