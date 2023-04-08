import core.utils as utils
import time

# Look for Scout Camp on the city and open its interface
def openScoutCamp(device):
    screenshot = utils.takeScreenshot()

    x, y = utils.findPattern(screenshot, 'images/scout.png')
   
    utils.click(device, [x, y])

# Return the buttons position of each available scouts (ready to be sent)
def getAvailableScouts():
    screenshot = utils.takeScreenshot()

    positions = utils.findMultiplePatterns(screenshot, 'images/explore.png')

    return positions

# Send a scout to explore the nearest fog square
def sendScout(device, position):
    utils.click(device, position)

    # Find the "Explore" button and click on it
    screenshot = utils.takeScreenshot()
    x, y = utils.findPattern(screenshot, 'images/explore.png')
    utils.click(device, [x, y])

    # Find the "March" button, click on it to send the scout
    screenshot = utils.takeScreenshot()
    x, y = utils.findPattern(screenshot, 'images/marche.png')
    utils.click(device, [x, y])
    
    # Return to city view
    utils.click(device, [100, 1000])