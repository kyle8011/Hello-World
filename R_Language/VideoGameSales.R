#Read from videogame sales from 1980 to 2020
dataframe <- read.csv("R_Language/vgsales.csv")

# Get the number of rows
rows <- nrow(dataframe)

# Function to add up all entries in a column
add_column <- function(column_name) {
    total_sales <- 0
    for (sale in dataframe[1:rows, c(column_name)]) {
        total_sales <- total_sales + sale
    }
    return(total_sales)
}
# Test out the function
na_sales <- add_column("NA_Sales")
print("Total NA Sales (millions)")
print(na_sales)


# Get number of games made by Nintendo
nintendo <- 0L
for (game in dataframe[1:rows, c("Publisher")]) {
    if (game == "Nintendo") {
        nintendo <- nintendo + 1
    }
}
print("Number of games made by nintendo")
print(nintendo)


# Find the year range
low_year <- 3000L
high_year <- 0L
for (year in dataframe[1:rows, c("Year")]) {
    if (year != "N/A") {
        if (as.integer(year) <= low_year) {
            low_year <- as.integer(year)
        }
        if (as.integer(year) >= high_year) {
            high_year <- as.integer(year)
        }
    }
}
# Print using concantenation given that the boolean value = TRUE
print_years <- FALSE
if (print_years)
    cat("Year range: ", low_year, "-", high_year, "\n")


# A function that returns a list of the total unique values
total_unique_values <- function(organize_by) {
    value_list <- list()
    values <- 0
    for (value in dataframe[1:rows, c(organize_by)]) {
        if (value %in% value_list) {
            return
            } else {
            value_list <- append(value_list, value)
            values <- values + 1
        }
    }
    return(value_list)
}

# Get number of platforms
platforms <- total_unique_values("Platform")
cat("There are", length(platforms), "Platforms \n")

# Get number of companies
companies <- total_unique_values("Publisher")
cat("There are", length(companies), "Companies \n")

# Get number of Genres
genres <- total_unique_values("Genre")
cat("There are", length(genres), "Genres \n")

# Making graphs

# Pie Chart

# Creata a vector for holding the genre totals
genre_totals <- integer(12)
for (x in 1:rows) {
    # Returns the index for which the genre has that name
    index <- which(genres == dataframe[x, "Genre"])
    # Adds one to that genre slot
    genre_totals <- replace(genre_totals, index, genre_totals[index] + 1)
}
# Get percentages of each game genre
sum <- sum(genre_totals)
percentage <- round(genre_totals / sum * 100)
lbl <- paste(genres, percentage, "%")
# Plot a pie chart with each genre
pie(genre_totals, labels = lbl, col = rainbow(12),
    main = "Game Genres (1980 - 2020)")
dev.copy(png, "R_Language/piechart.png")
dev.off()

# Bar Graph

# Get each total
eu_sales <- add_column("EU_Sales")
jp_sales <- add_column("JP_Sales")
other_sales <- add_column("Other_Sales")
# Put them into vectors
sales <- c(na_sales, eu_sales, jp_sales, other_sales)
names <- c("North Americe", "Europe", "Japan", "Other")
# Plot the graph
barplot(sales, names.arg = names, col = rainbow(4),
    xlab = "Countries", ylab = "Games Sold (millions)",
    main = "Video Games Sold around the World (1980 - 2020)")
dev.copy(png, "R_Language/barchart.png")
dev.off()
