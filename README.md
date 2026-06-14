# Text Analytics: Trump vs Hillary Clinton Tweet Sentiment Analysis

## 📋 Project Overview

This project performs a comprehensive sentiment analysis on tweets from Donald Trump (@realDonaldTrump) and Hillary Clinton (@HillaryClinton) during the 2016 US Presidential Election campaign. Using Natural Language Processing (NLP) and machine learning techniques, we analyze the emotional tone, patterns, and engagement metrics of their social media presence.

## 🎯 Objectives

- Analyze sentiment patterns in political tweets during the 2016 election
- Compare sentiment between two major political candidates
- Identify trends in tweet engagement and retweet behavior
- Visualize sentiment distribution and temporal patterns
- Extract insights about communication strategies

## 📊 Dataset

**Source:** Twitter API (Historical 2016 Election Data)

**Size:** 6,444 tweets
- **Trump tweets:** 3,218 original tweets
- **Hillary tweets:** 3,226 original tweets

**Time Period:** September-October 2016 (Pre-election period)

**Key Features:**
- `handle` - Twitter account (@realDonaldTrump, @HillaryClinton)
- `text` - Tweet content
- `is_retweet` - Whether the tweet is a retweet
- `time` - Timestamp
- `lang` - Language (English, Spanish, Other)
- `retweet_count` - Number of retweets
- `favorite_count` - Number of likes/favorites

**File:** `trump.hillary tweets.csv`

## 🛠️ Technologies & Libraries Used

```
Python 3.x
pandas          - Data manipulation and analysis
numpy           - Numerical computations
matplotlib      - Static visualization
seaborn         - Statistical data visualization
plotly          - Interactive visualizations
nltk            - Natural Language Processing
vaderSentiment  - Sentiment analysis for social media
scikit-learn    - Machine learning utilities
```

## 🔄 Methodology

### 1. **Data Preprocessing**
```
✓ Language Detection: Filter tweets by language
✓ DateTime Parsing: Extract hour, day, month information
✓ Text Cleaning: Remove special characters, URLs, mentions
✓ Tokenization: Break text into individual words
✓ Stopword Removal: Eliminate common English words (the, is, and, etc.)
✓ Lemmatization: Convert words to base form (running → run)
```

### 2. **Sentiment Analysis**
**Tool:** VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Why VADER?**
- Optimized for social media text
- Handles emojis, slang, and informal language
- Works well with political discourse
- Returns compound score (-1 to +1)

**Sentiment Classification:**
- **Positive** (compound > 0.05)
- **Negative** (compound < -0.05)
- **Neutral** (compound between -0.05 and 0.05)

### 3. **Data Analysis**
- Temporal sentiment trends (daily/monthly)
- Engagement metrics correlation (sentiment vs favorites/retweets)
- Language distribution analysis
- Retweet vs original tweet comparison

### 4. **Visualization**
- Sentiment score distributions (histograms)
- Time-series sentiment trends
- Tweet count comparisons
- Retweet percentage breakdowns
- Interactive Plotly visualizations

## 📁 Project Structure

```
Text-Analytics/
├── trump.hillary tweets.csv                                    # Raw data
├── Interactive Visualization of Donald trump vs Hillary...ipynb # Main notebook
├── README.md                                                    # This file
└── requirements.txt                                             # Dependencies
```

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sandeep2096/Text-Analytics.git
   cd Text-Analytics
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn plotly nltk vaderSentiment
   ```

3. **Download NLTK data**
   ```python
   python -m nltk.downloader stopwords punkt wordnet
   ```

4. **Run the Jupyter Notebook**
   ```bash
   jupyter notebook "Interactive Visualization of Donald trump vs Hillary Clinton tweet based Sentiment Analysis.ipynb"
   ```

5. **Execute cells in order** (Kernel → Run All)

## 📈 Key Findings

### Sentiment Patterns
- **Trump tweets:** More neutral/aggressive tone with higher variation
- **Hillary tweets:** More positive sentiment with consistent messaging
- Both candidates show increased sentiment during debate periods

### Engagement Analysis
- Positive tweets receive higher engagement (favorites/retweets)
- Original tweets outperform retweets in sentiment consistency
- Peak engagement occurs during debate nights and major announcements

### Tweet Distribution
- Hillary: 50.1% of dataset
- Trump: 49.9% of dataset
- English tweets: 96.8% of total
- Spanish tweets: 1.6% (Hillary's outreach)

### Language Usage
- Trump: Direct, shorter messages with emphasis on campaign rallies
- Hillary: Policy-focused with longer, detailed explanations
- Both use strategic hashtags (#MAGA, #ImWithHer, #DebateNight)

## 📊 Visualizations Included

1. **Tweet Count Distribution** - Comparison between candidates
2. **Monthly Tweet Trends** - Activity over September-October
3. **Retweet Percentage** - Original vs retweet ratio
4. **Sentiment Distribution** - Histogram of sentiment scores
5. **Time Series Analysis** - Sentiment trends over time
6. **Engagement Correlation** - Sentiment vs likes/retweets
7. **Interactive Plotly Charts** - Hover-enabled detailed views

## 🔍 Code Walkthrough

### Sentiment Calculation
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def calculate_sentiment_scores(sentence):
    sentiment = analyzer.polarity_scores(sentence)['compound']
    return sentiment
```

### Text Preprocessing
```python
import nltk
from nltk.corpus import stopwords
import re

def preprocess_text(text):
    # Remove special characters
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    
    # Tokenization
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words("english")]
    
    # Lemmatization
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return " ".join(tokens)
```

## 💡 Insights & Conclusions

1. **Communication Style:** Trump uses more provocative language; Hillary emphasizes policy details
2. **Engagement Strategy:** Both candidates adapted messaging around debate nights
3. **Sentiment Consistency:** Hillary maintained more consistent positive sentiment
4. **International Outreach:** Hillary's Spanish tweets show multilingual strategy
5. **Retweet Behavior:** Both candidates' supporters highly engaged with partisan content

## 🔮 Future Enhancements

- [ ] Real-time sentiment tracking dashboard
- [ ] Emotion detection (anger, joy, fear, sadness)
- [ ] Topic modeling (LDA) to identify key issues
- [ ] Word embeddings and semantic similarity
- [ ] Prediction model for tweet engagement
- [ ] Geographic analysis of tweet origins
- [ ] Bot detection in retweets
- [ ] Sarcasm and irony detection

## 📚 References & Resources

- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [NLTK Documentation](https://www.nltk.org/)
- [Plotly Interactive Visualization](https://plotly.com/python/)
- [NLP Best Practices](https://towardsdatascience.com/nlp-best-practices-7f07601afa76)
- [2016 Election Twitter Data](https://www.kaggle.com/datasets)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Sandeep**
- GitHub: [@sandeep2096](https://github.com/sandeep2096)
- Project: [Text-Analytics](https://github.com/sandeep2096/Text-Analytics)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/sandeep2096/Text-Analytics/issues) for any open discussions.

## ⭐ Acknowledgments

- Dataset sourced from historical Twitter API
- VADER sentiment analyzer developed by C.J. Hutto and Eric Gilbert
- Inspiration from NLP and political communication research

---

**Last Updated:** 2026  
**Status:** Active  
**Python Version:** 3.7+
