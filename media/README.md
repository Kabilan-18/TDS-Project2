
# Media Dataset Analysis

## Dataset Overview
The dataset consists of 2652 entries and 8 columns, including date of media creation, language, type, title, creator, and ratings in terms of overall quality, specific quality, and repeatability.

## Missing Values
The dataset has missing values in the 'date' (99 entries) and 'by' (262 entries) columns, which were addressed by removing records with missing 'date' and 'by' information.

## Analysis Summary
- The average overall rating in the dataset is approximately 3.05, indicating a moderate performance.
- The quality ratings are slightly higher on average at around 3.21.
- Repeatability has a mean of approximately 1.49, suggesting a tendency towards lower repeatability in media.

## Histograms
Histograms were generated for the following metrics:
- **Overall Ratings**: Displays the distribution of overall ratings.
- **Quality Ratings**: Shows how quality ratings are spread across entries.
- **Repeatability Ratings**: Illustrates the frequency of repeatability scores.

## Correlation Analysis
A heatmap was produced to visualize the correlations among overall, quality, and repeatability ratings. Notably, overall and quality ratings exhibit a strong positive correlation (0.83), suggesting that higher overall ratings are associated with better quality ratings. The correlation between overall and repeatability is moderate (0.51), while quality and repeatability have a weaker correlation (0.31).

## Conclusion
The media dataset offers valuable insights into the ratings of various media types. The visualizations and correlations can guide further analyses and inform potential improvements in quality and repeatability.
