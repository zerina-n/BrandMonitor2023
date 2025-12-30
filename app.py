import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import pandas as pd
from textblob import TextBlob

# 1. Setup the App
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

        # 3. AI Analysis (Lightweight Version)
        st.write("Running AI Sentiment Analysis...")
        
        # Define a function to get sentiment using TextBlob
        def analyze_sentiment(text):
            analysis = TextBlob(text)
            if analysis.sentiment.polarity > 0:
                return "POSITIVE", analysis.sentiment.polarity
            else:
                return "NEGATIVE", abs(analysis.sentiment.polarity)

        # Apply the analysis to every row
        df['Sentiment'], df['Confidence'] = zip(*df['text'].map(analyze_sentiment))

        # 4. Filter by Month
        all_months = df['Month'].unique().tolist()
        selected_month = st.select_slider("Select Month", options=all_months)
        filtered_df = df[df['Month'] == selected_month]

        st.write(f"Showing reviews for: **{selected_month}**")
        st.dataframe(filtered_df)

        if not filtered_df.empty:
            # 5. Charts
            st.subheader("Sentiment Distribution")
            sentiment_counts = filtered_df['Sentiment'].value_counts()
            st.bar_chart(sentiment_counts)
            
            # Metric
            st.write("### Model Quality")
            avg_confidence = filtered_df['Confidence'].mean()
            st.metric(label="Average AI Confidence Score", value=f"{avg_confidence:.2%}")
            st.caption("This score represents the polarity strength.")

            # Cloud
            st.subheader("Word Cloud of Reviews")
            text_data = " ".join(filtered_df['text'].tolist())
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
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