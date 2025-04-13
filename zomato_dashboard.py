import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    #df = pd.read_csv('zomato.csv')
    df = pd.read_csv(r'C:\Users\chava\Desktop\Zomato Project\zomato.csv')
    df.drop_duplicates(inplace=True)
    df = df.dropna(subset=['rate', 'location', 'cuisines', 'rest_type', 'approx_cost(for two people)'])
    df['rate'] = df['rate'].astype(str).apply(lambda x: x.split('/')[0].strip())
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df['cost'] = df['approx_cost(for two people)'].astype(str).str.replace(',', '')
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    df.dropna(subset=['rate', 'cost'], inplace=True)
    return df

df = load_data()

# Title
st.title("Zomato Restaurant Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
rest_type_filter = st.sidebar.multiselect(
    "Select Restaurant Types", 
    df['rest_type'].unique(), 
    default=df['rest_type'].unique()[:5]
)
online_order_filter = st.sidebar.selectbox(
    "Online Ordering Available", 
    options=["Yes", "No", "Both"], 
    index=2
)

# Apply filters
filtered_df = df[df['rest_type'].isin(rest_type_filter)]
if online_order_filter != "Both":
    filtered_df = filtered_df[filtered_df['online_order'] == online_order_filter]

st.subheader("Top 10 Cuisines")
top_cuisines = filtered_df['cuisines'].value_counts().nlargest(10)
st.bar_chart(top_cuisines)

st.subheader("Average Rating by Restaurant Type")
avg_rating = filtered_df.groupby('rest_type')['rate'].mean().sort_values(ascending=False).head(10)
st.bar_chart(avg_rating)

st.subheader("Cost for Two vs Rating")
fig, ax = plt.subplots()
sns.scatterplot(x='cost', y='rate', data=filtered_df, alpha=0.5, ax=ax)
st.pyplot(fig)

st.subheader("Average Rating by Online Order Availability")
if 'online_order' in filtered_df.columns:
    order_rating = filtered_df.groupby('online_order')['rate'].mean()
    st.bar_chart(order_rating)

# Footer
st.markdown("---")
st.caption("Made with Streamlit | Data Source: Kaggle Zomato Dataset")
