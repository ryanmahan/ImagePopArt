# ImagePopArt
Takes in an image then creates a "pop art" style of the image

# Color
Works by recursively finding the colors of a lot of similar pixels around it, and the location of those pixels. This data could be used for finding radii of circles to be added, but that functionality was removed because a fixed radius looked better in the end
Uses average color with a fixed radius set by "spacing" variable to draw circles

# Grayscale
Sets the image to a grayscale picture then finds the size a circle should be and sets the radius from 1-(scaleby/2)
Radius of the circle is set by how bright the pixel is, the brighter the pixel the wider the circle.
