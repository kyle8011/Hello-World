
# My two questions would be:
# 1. what genre of game has the highest ratings?
# 2. What platform has the highest ratings?

# Game_Genres.csv has number, title, date, team, genre, plays
# Game_Scores.csv has console, name, score ** Use this for platform **

main <- function() {
    # Lets answer the first question, what genre of game is rated highest?
    #Read Game_Genres.csv
    genre_data <- read.csv("Data_Analysis/Game_Genres.csv")

    # Get number of Genres
    genres <- get_unique_values("Genres", genre_data)
    cat("There are", length(genres), "Genres \n")
    # Get average ratings
    average_ratings <- get_genre_ratings(genre_data, genres)
    # Plot them
    create_pie_chart(genre_data, genres)
    bar_graph_top_ten(genres, average_ratings)

    # Get Platforms
    platform_data <- read.csv("Data_Analysis/Game_Scores.csv")
    platforms <- get_unique_values("Console", platform_data)
    cat("There are", length(platforms), "Consoles \n")
    # Get average ratings
    average_ratings <- get_console_ratings(platform_data, platforms, FALSE)
    # Plot a bar graph
    #bar_graph_all(platforms, average_ratings,
     #"Video Game Conslole Ratings (No Filter)")

    average_ratings <- get_console_ratings(platform_data, platforms, TRUE)
    print(average_ratings)
    print(platforms)
    bar_graph_all(platforms, average_ratings,
     "Video Game Console Ratings (Filtered)")

    
}

bar_graph_all <- function(names, values, title) {
    # Plot the graph
    barplot(values, names = names, col = rainbow(43),
        cex.names = .6, xlab = "Ratings", ylab = "Consoles", horiz = TRUE,
        las = 1, main = title)
    dev.copy(png, "Data_Analysis/Consolechartfilter.png")
    dev.off()
}

get_console_ratings <- function(dataframe, consoles, unique) {
    # Get the genres from each row and line them up with ratings
    rows <- nrow(dataframe)
    console_ratings <- integer(42)
    console_totals <- integer(42)
    if (!unique) {
        for (x in 1:rows) {
            # Separate out different genres here
            console_row <- dataframe[x, "Console"]
            # Split by commas
            console_row <- unlist(strsplit(console_row, ","))
            # Remove stuff
            console_row <- gsub(" ", "", console_row)
            # Get rating for that row
            rating <- dataframe[x, "Score"]
            # Add them up
            for (console in console_row) {
                # Returns the index for which the console has that name
                index <- which(consoles == console)
                if (!is.na(rating)) {
                    # Adds one to that console rating total
                    console_ratings <- replace(console_ratings,
                                index, console_ratings[index] + rating)
                    # Adds one to that console slot
                    console_totals <- replace(console_totals,
                                index, console_totals[index] + 1)
                }
            }
        }
    } else {
        for (x in 1:rows) {
            # Separate out different genres here
            console_row <- dataframe[x, "Console"]
            # Split by commas
            console_row <- unlist(strsplit(console_row, ","))
            # Get rating for that row
            rating <- dataframe[x, "Score"]
            # Add them up
            if (length(console_row) == 1) {
                index <- which(consoles == console_row)
                # Adds one to that console rating total
                console_ratings <- replace(console_ratings,
                            index, console_ratings[index] + rating)
                # Adds one to that console slot
                console_totals <- replace(console_totals,
                            index, console_totals[index] + 1)
            }
        }
    }
    average_ratings <- console_ratings / console_totals
    return(average_ratings)
}

bar_graph_top_ten <- function(names, values) {
    # Grab the top ten
    # Replace values with less than 3% with other
    for (x in seq_along(values)) {
        if (values[x] < 3.665) {
            names[x] <- "other"
            values[x] <- 0
        }
    }
    # Get genres that were not replaced with other
    top_ten_names <- names[names != "other"]
    # Get percentages that were not replaced with other
    top_ten_ratings <- values[values != 0] * 2
    # Swap values 6 and 7 so it doesn't hit the label
    place_holder <- top_ten_ratings[4]
    top_ten_ratings[4] <- top_ten_ratings[5]
    top_ten_ratings[5] <- place_holder

    place_holder <- top_ten_names[4]
    top_ten_names[4] <- top_ten_names[5]
    top_ten_names[5] <- place_holder

    # Plot the graph
    barplot(top_ten_ratings, names = top_ten_names, col = rainbow(10),
        cex.names = .6, xlab = "Ratings", ylab = "Genres", horiz = TRUE,
        las = 1, main = "Video Game Genre Ratings (Top Ten)")
    dev.copy(png, "Data_Analysis/Genrechart.png")
    dev.off()
}

# A function that returns a list of the total unique values
get_unique_values <- function(organize_by, dataframe) {
    value_list <- list()
    rows <- nrow(dataframe)
    for (values in dataframe[1:rows, c(organize_by)]) {
        values <- unlist(strsplit(values, ","))
        # Remove brackets, commas, quotation marks
        values <- gsub("\\[|\\]|\\'|\\ ", "", values)
        for (value in values) {
            if (value %in% value_list) {
                return
            } else {
                if (value != "")
                value_list <- append(value_list, value)
            }
        }
    }
    return(value_list)
}

get_genre_ratings <- function(dataframe, genres) {
    # Get the genres from each row and line them up with ratings
    rows <- nrow(dataframe)
    genre_ratings <- integer(23)
    genre_totals <- integer(23)
    for (x in 1:rows) {
        # Separate out different genres here
        genre_row <- dataframe[x, "Genres"]
        # Split by commas
        genre_row <- unlist(strsplit(genre_row, ","))
        # Remove stuff
        genre_row <- gsub("\\[|\\]|\\'|\\ ", "", genre_row)
        # Get rating for that row
        rating <- dataframe[x, "Rating"]
        # Add them up
        for (genre in genre_row) {
            # Returns the index for which the genre has that name
            index <- which(genres == genre)
            if (!is.na(rating)) {
                # Adds one to that genre rating total
                genre_ratings <- replace(genre_ratings,
                            index, genre_ratings[index] + rating)
                # Adds one to that genre slot
                genre_totals <- replace(genre_totals,
                            index, genre_totals[index] + 1)
            }
        }
    }
    average_ratings <- genre_ratings / genre_totals
    return(average_ratings)
}

# Pie Chart
create_pie_chart <- function(dataframe, genres) {
    rows <- nrow(dataframe)
    # Creata a vector for holding the genre totals
    genre_totals <- integer(23)
    for (x in 1:rows) {
        # Separate out different genres here
        genre_row <- dataframe[x, "Genres"]
        # Split by commas
        genre_row <- unlist(strsplit(genre_row, ","))
        # Remove stuff
        genre_row <- gsub("\\[|\\]|\\'|\\ ", "", genre_row)
        # Add them up
        for (genre in genre_row) {
            # Returns the index for which the genre has that name
            index <- which(genres == genre)
            # Adds one to that genre slot
            genre_totals <- replace(genre_totals,
                            index, genre_totals[index] + 1)
        }
    }
    # Get percentages of each game genre
    sum <- sum(genre_totals)
    percentage <- round(genre_totals / sum * 100)
    other_total <- 0
    # Replace values with less than 3% with other
    for (x in seq_along(percentage)) {
        if (percentage[x] < 3) {
            other_total <- other_total + percentage[x]
            genres[x] <- "other"
            percentage[x] <- 0
        }
    }
    # Get genres that were not replaced with other
    genres_other <- genres[genres != "other"]
    genres_other <- append(genres_other, "other")
    # Get percentages that were not replaces with other
    percentage_other <- percentage[percentage != 0]
    percentage_other <- append(percentage_other, other_total)
    # Create the labels
    lbl <- paste(genres_other, percentage_other, "%")
    # Plot a pie chart with each genre
    pie(percentage_other, labels = lbl, col = rainbow(23),
      main = "Game Genres")
    # Save the plot
    dev.copy(png, "Data_Analysis/piechart.png")
    dev.off()
}

# Function to add up all entries in a column
add_column <- function(column_name, dataframe) {
    total_sales <- 0
    rows <- nrow(dataframe)
    for (sale in dataframe[1:rows, c(column_name)]) {
        total_sales <- total_sales + sale
    }
    return(total_sales)
}

main()
