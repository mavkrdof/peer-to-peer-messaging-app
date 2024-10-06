import toga
import toga.constants

print(toga.constants.AZURE)

colors = [color for color in dir(toga.constants) if color.isalpha()]
print(colors)