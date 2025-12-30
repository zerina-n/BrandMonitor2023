import matplotlib.pyplot as plt
from wordcloud import WordCloud
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
        # Load the data
        df = pd.read_json("reviews.json")
        
        # Create a real Date column to sort by month
        df['date'] = pd.to_datetime(df['date'])
        df['Month'] = df['date'].dt.month_name()

        # 3. AI Analysis (Run on ALL data first)
        # We process the text to get label (POSITIVE/NEGATIVE) and score (Confidence)
        st.write("Running AI Sentiment Analysis...")
        
        # Apply the model to every review text
        results = sentiment_pipeline(df['text'].tolist())
        
        # Save results back into the Table
        df['Sentiment'] = [r['label'] for r in results]
        df['Confidence'] = [r['score'] for r in results]

        # 4. Filter by Month (Interactive)
        all_months = df['Month'].unique().tolist()
        selected_month = st.select_slider("Select Month", options=all_months)
        
        # Filter the table based on the slider
        filtered_df = df[df['Month'] == selected_month]

        # Show the Data Table
        st.write(f"Showing reviews for: **{selected_month}**")
        st.dataframe(filtered_df)

        if not filtered_df.empty:
            # 5. The Bar Chart (Visualization)
            st.subheader("Sentiment Distribution")
            sentiment_counts = filtered_df['Sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
            
            # --- ADVANCED REQUIREMENT: Average Confidence ---
            st.write("### Model Quality")
            
            # Calculate the average score
            avg_confidence = filtered_df['Confidence'].mean()
            
            # Display it as a big metric
            st.metric(label="Average AI Confidence Score", value=f"{avg_confidence:.2%}")
            st.caption("This score represents how sure the AI is about its predictions on average.")

            # --- BONUS: WORD CLOUD ---
            st.subheader("Word Cloud of Reviews")
            
            # Combine all review text into one big string
            text_data = " ".join(filtered_df['text'].tolist())
            
            # Create the cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
            
            # Display it using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
        else:
            st.info("No reviews found for this month.")

    except FileNotFoundError:
        st.error("Error: 'reviews.json' file not found. Please run the scraper first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

elif page == "Products":
    st.write("Product Analysis Page (Under Construction)")

elif page == "Testimonials":
    st.write("Customer Testimonials Page (Under Construction)")