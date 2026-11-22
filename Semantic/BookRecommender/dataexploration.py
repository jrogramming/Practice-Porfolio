import seaborn as sns
import pandas as pd
import kagglehub
import matplotlib.pyplot as plt

# Download dataset
#path = kagglehub.dataset_download("dylanjcastillo/7k-books-with-metadata")
path = r"C:\Users\trang\.cache\kagglehub\datasets\dylanjcastillo\7k-books-with-metadata\versions\3"
#print("Path to dataset files:", path)

books = pd.read_csv(f"{path}/books.csv")
#books


# EDA

# Missing Values
ax = plt.axes()
sns.heatmap(books.isna().transpose(), cbar = False, ax = ax)
plt.xlabel("Columns")
plt.ylabel("Missing Values")
plt.show()

# We want to get rid of these books, check for biases
# Heatmap
books["missing_desc"] = np.where(books["description"].isna(), 1, 0)
