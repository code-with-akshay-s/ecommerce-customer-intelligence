import pandas as pd

df = pd.read_csv("data/raw/olist_orders_dataset.csv")

print(df.head())
print(df.columns.tolist())

df.info()

print(df["order_status"].value_counts())

total_orders = len(df)

delivered_orders = (df["order_status"] == "delivered").sum()

delivery_percentage = (delivered_orders/total_orders) * 100

print("Total orders:", total_orders)
print("Delivered orders:", delivered_orders)
print("Delivery percentage:", delivery_percentage)

print(df.isnull().sum())

missing_delievery = df[df["order_delivered_customer_date"].isnull()]

print(missing_delievery["order_status"].value_counts())

delivered_missing = df[
    (df["order_status"] == "delivered") &
    (df["order_delivered_customer_date"].isnull())
]

print(delivered_missing[
    [
        "order_id",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
].to_string(index=False))

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column])

print(df.dtypes)   

df["delivery_days"] = (
    df["order_delivered_customer_date"] - 
    df["order_purchase_timestamp"]
).dt.days

print(df[["order_purchase_timestamp",
          "order_delivered_customer_date",
          "delivery_days"]].head(10))

delivered_orders = df[df["order_status"] == "delivered"]

average_delivery = delivered_orders["delivery_days"].mean()
minimum_delivery = delivered_orders["delivery_days"].min()
maximum_delivery = delivered_orders["delivery_days"].max()


print("Average delivery time:", round(average_delivery, 2), "days")
print("Minimum delivery time:", minimum_delivery, "days")
print("Maximum delivery time:", maximum_delivery, "days")

longest_delivery_order = delivered_orders.loc[
    delivered_orders["delivery_days"].idxmax()
]

print(longest_delivery_order[
    [
        "order_id",
        "order_purchase_timestamp",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "delivery_days"
    ]
])