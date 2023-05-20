# R datatypes include: logical, numerical, integer, complex, character, raw
# Use at least 5 of these

# Integer (more precise than float)
int <- 123L
print(int)
print(class(int))

# Logical
bool <- TRUE
print(bool)
print(class(bool))

# Numerical (includes floating and integer)
num <- -5.3
print(num)
print(class(num))

# Complex
complex <- 3 + 5i
print(complex)
print(class(complex))
print("Converting from cartesian to polar")
cat("r =", Mod(complex), ", theta (radians) =", Arg(complex), "\n")


# Character
char <- "Fruit"
print(char)
print(class(char))

# Raw
raw <- charToRaw("Fruit")
print(raw)
print(class(raw))


# Reading from a CSV file
read_csv <- read.csv("R_Language/test_csv.csv")
# Prints column named "Number"
print(read_csv[c("Number")])
# Prints second and third entry of column "Name"
print(read_csv[2:3, c("Name")])
# Prints second row
print(read_csv[2, ])
# Prints data column
print(read_csv[3])
# Get number of rows
number_rows <- nrow(read_csv)
print(number_rows)
# Get number of columns
number_columns <- length(read_csv)
print(number_columns)

# Add up data
total_data <- 0
for (x in read_csv[1:number_rows, 3]) {
    total_data <- total_data + x
    print(total_data)
}

# Display output to the screen in the form of a plot
barplot(read_csv$data, col = "blue", width = c(2, 1, 3, 2, 1),
    main = "Test Bar Graph", xlab = "number", ylab = "data",
    names.arg = c(1, 2, 3, 4, 5))
