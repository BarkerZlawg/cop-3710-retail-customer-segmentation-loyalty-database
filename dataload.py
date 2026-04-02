import oracledb as odb
import pandas as pd

connect = odb.connect(user = 'retail_user', password = 'password', dsn = 'localhost:1521/XEPDB1')
cursor = connect.cursor()

#CUSTOMER INIT
def clean_number(val):
    if pd.isna(val):
        return None
    return float(val)

df = pd.read_csv("customer.csv")
df = df.where(pd.notnull(df), None)

numeric_cols = ['Income', 'Kidhome', 'Teenhome', 'Recency', 'ComplainFlag', 'Year_Birth']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO CUSTOMER VALUES (
        :1,:2,:3,:4,
        TO_DATE(:5, 'DD-MM-YYYY'),
        :6,:7,:8,:9,:10
    )
""", (
    int(row['CustomerID']),
    row['EducationCode'],
    row['MaritalStatusCode'],
    clean_number(row['Year_Birth']),
    row['Dt_Customer'],
    clean_number(row['Income']),
    clean_number(row['Kidhome']),
    clean_number(row['Teenhome']),
    clean_number(row['Recency']),
    clean_number(row['ComplainFlag'])
))

#PROFILE_CUSTOMER INIT
df = pd.read_csv("profile_customer.csv")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO CUSTOMER_PROFILE VALUES (
            :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12
        )
    """, tuple(row))

#CUSTOMER_CHILD INIT
df = pd.read_csv("customer.csv")

child_rows = []
for _, row in df.iterrows():
    cid = row['CustomerID']

    if row['Kidhome'] > 0:
        child_rows.append((cid, 1, 'Kid', None, None))

    if row['Teenhome'] > 0:
        child_rows.append((cid, 2, 'Teen', None, None))

for row in child_rows:
    cursor.execute("""
        INSERT INTO CUSTOMER_CHILD VALUES (
            :1,:2,:3,:4,:5
        )
    """, row)

#CAMPAIGN INIT
cursor.execute("""
    INSERT INTO CAMPAIGN VALUES (1, 'Campaign A', SYSDATE, SYSDATE+30, 5, 20)
""")

cursor.execute("""
    INSERT INTO CAMPAIGN VALUES (2, 'Campaign B', SYSDATE, SYSDATE+30, 10, 30)
""")

cursor.execute("""
    INSERT INTO CAMPAIGN VALUES (3, 'Campaign C', SYSDATE, SYSDATE+30, 8, 25)
""")

#CUSTOMER_CAMPAIGN INIT
df = pd.read_csv("customer.csv")

for _, row in df.iterrows():
    cid = int(row['CustomerID'])

    # Example mapping (you can expand this)
    if row.get('AcceptedCmp1', 0) == 1:
        cursor.execute("""
            INSERT INTO CUSTOMER_CAMPAIGN VALUES (
                :1, 1, 'Y', SYSDATE, 'Email'
            )
        """, (cid,))

    if row.get('AcceptedCmp2', 0) == 1:
        cursor.execute("""
            INSERT INTO CUSTOMER_CAMPAIGN VALUES (
                :1, 2, 'Y', SYSDATE, 'Phone'
            )
        """, (cid,))

connect.commit()
cursor.close()
connect.close()