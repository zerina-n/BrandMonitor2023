import streamlit as st
import pandas as pd
from transformers import pipeline

# 1. Load the AI Model (Cache it so it doesn't reload every time)
@st.cache_resource
def load_sentiment_model():
    # This downloads the model the first time you run it
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

sentiment_pipeline = load_sentiment_model()

st.title("Brand Monitor 2023")

# 2. Sidebar Navigation
page = st.sidebar.radio("Go to", ["Reviews", "Products", "Testimonials"])

if page == "Reviews":
    st.header("Customer Reviews")
    
    try:
        df = pd.read_json("reviews.json")
        df['date'] = pd.to_datetime(df['date'])
        
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        
        selected_month = st.select_slider("Select a Month in 2023", options=months)
        
        # Filter by month
        filtered_df = df[df['date'].dt.month_name() == selected_month]
        
        st.write(f"Showing reviews for: **{selected_month}**")
        
        if not filtered_df.empty:
            # --- AI ANALYSIS SECTION ---
            st.write("🤖 **Running Sentiment Analysis...**")
            
            # 1. Get the list of text from the filtered reviews
            reviews_text = filtered_df['text'].tolist()
            
            # 2. Feed them into the AI
            results = sentiment_pipeline(reviews_text)
            
            # 3. Add the results back to the table
            filtered_df['Sentiment'] = [result['label'] for result in results]
            filtered_df['Confidence'] = [result['score'] for result in results]
            
            # 4. Show the Table with new AI columns
            st.dataframe(filtered_df)
            
          # 5. The Bar Chart (Visualization)
            st.subheader("Sentiment Distribution")
            sentiment_counts = filtered_df['Sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
            
            # --- ADVANCED REQUIREMENT: Average Confidence ---
            # Calculate the average score
            avg_confidence = filtered_df['Confidence'].mean()
            
            # Display it as a big metric
            st.write("### Model Quality")
            st.metric(label="Average AI Confidence Score", value=f"{avg_confidence:.2%}")
            st.caption("This score represents how sure the AI is about its predictions on average.")
            
        else:
            st.info("No reviews found for this month.")
            
    except ValueError:
        st.error("Could not load reviews.json.")

elif page == "Products":
    st.header("Product List")
    st.write("Products placeholder.")

elif page == "Testimonials":
    st.header("Customer Testimonials")
    st.write("Testimonials placeholder.")