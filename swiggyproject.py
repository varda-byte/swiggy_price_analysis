import pandas as pd

df = pd.read_csv('swiggy_file.csv')

# 1. Fix column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# 2. Extract price number from "₹250 for two" → 125
df['price_per_person'] = df['average_price'].str.extract(r'₹(\d+)').astype(float) / 2

# 3. Fix rating — replace NEW with NaN, convert to float
df['rating'] = df['rating'].replace('NEW', pd.NA)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 4. Drop missing cuisines and area
df = df.dropna(subset=['cuisine', 'area'])

# 5. Clean pure_veg column
df['pure_veg'] = df['pure_veg'].str.strip()

# 6. Check result
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Top 10 most expensive cuisines
cuisine_price = df.groupby('cuisine')['price_per_person'].mean().sort_values(ascending=False).head(10)
print("Top 10 Expensive Cuisines:\n", cuisine_price)

# 2. Top 10 most expensive cities
city_price = df.groupby('location')['price_per_person'].mean().sort_values(ascending=False).head(10)
print("\nTop 10 Expensive Cities:\n", city_price)

# 3. Does higher rating = higher price?
df_rated = df.dropna(subset=['rating'])
print("\nCorrelation (rating vs price):", df_rated['rating'].corr(df_rated['price_per_person']).round(3))
import pandas as pd
import matplotlib.pyplot as plt

# Load and clean
df = pd.read_csv('swiggy_file.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['price_per_person'] = df['average_price'].str.extract(r'₹(\d+)').astype(float) / 2
df['rating'] = pd.to_numeric(df['rating'].replace('NEW', pd.NA), errors='coerce')
df = df.dropna(subset=['cuisine', 'area'])

# Analysis
cuisine_price = df.groupby('cuisine')['price_per_person'].mean().sort_values(ascending=False).head(10)
city_price = df.groupby('location')['price_per_person'].mean().sort_values(ascending=False).head(10)
df_rated = df.dropna(subset=['rating'])

# Charts
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

cuisine_price.plot(kind='barh', ax=axes[0], color='steelblue')
axes[0].set_title('Top 10 Expensive Cuisines')
axes[0].set_xlabel('Avg Price per Person (₹)')

city_price_clean = city_price[city_price < 1000]
city_price_clean.plot(kind='barh', ax=axes[1], color='coral')
axes[1].set_title('Top 10 Expensive Cities')
axes[1].set_xlabel('Avg Price per Person (₹)')

axes[2].scatter(df_rated['rating'], df_rated['price_per_person'], alpha=0.1, color='purple')
axes[2].set_title('Rating vs Price (corr = 0.063)')
axes[2].set_xlabel('Rating')
axes[2].set_ylabel('Price per Person (₹)')

plt.tight_layout()
plt.savefig('swiggy_analysis.png', dpi=150)
plt.show()