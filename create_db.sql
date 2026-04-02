CREATE TABLE CUSTOMER (
    CustomerID NUMBER PRIMARY KEY,
    EducationCode VARCHAR2(20),
    MaritalStatusCode VARCHAR2(20),
    Year_Birth NUMBER,
    Dt_Customer DATE NOT NULL,
    Income NUMBER,
    Kidhome NUMBER,
    Teenhome NUMBER,
    Recency NUMBER,
    ComplainFlag NUMBER
);

CREATE TABLE CUSTOMER_PROFILE (
    CustomerID NUMBER PRIMARY KEY,
    MntWines NUMBER,
    MntFruits NUMBER,
    MntMeatProducts NUMBER,
    MntFishProducts NUMBER,
    MntSweetProducts NUMBER,
    MntGoldProds NUMBER,
    NumDealsPurchases NUMBER,
    NumWebPurchases NUMBER,
    NumCatalogPurchases NUMBER,
    NumStorePurchases NUMBER,
    NumWebVisitsMonth NUMBER,

    CONSTRAINT FK_PROFILE_CUSTOMER FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID)
);

CREATE TABLE CUSTOMER_CHILD (
    CustomerID NUMBER NOT NULL,
    ChildSeq NUMBER NOT NULL,
    ChildType VARCHAR(20),
    BirthYear NUMBER,
    Notes VARCHAR2(200),

    CONSTRAINT PK_CHILD PRIMARY KEY (CustomerID, ChildSeq),
    CONSTRAINT FK_CHILD_CUSTOMER FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID)
);

CREATE TABLE CAMPAIGN (
    CampaignID NUMBER PRIMARY KEY,
    CampaignName VARCHAR2(100),
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    CostPerContact NUMBER,
    RevenuePerResponse NUMBER
);

CREATE TABLE CUSTOMER_CAMPAIGN (
    CustomerID NUMBER NOT NULL,
    CampaignID NUMBER NOT NULL,
    AcceptedFlag VARCHAR2(20),
    ResponseDate DATE NOT NULL,
    ContactChannel VARCHAR2(20),

    CONSTRAINT FK_CUSTOMER FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID),
    CONSTRAINT FK_CAMPAIGN FOREIGN KEY (CampaignID) REFERENCES CAMPAIGN(CampaignID)
);
