import core.utils as utils
import core.actions as actions
import time


device = utils.connectToBluestacks()

actions.openScoutCamp(device)

positions = actions.getAvailableScouts()

actions.sendScout(device, positions[0])