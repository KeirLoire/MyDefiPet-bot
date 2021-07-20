import cv2, glob, time, pyautogui, enum, numpy

class Template(enum.Enum):
    COIN="img/templates/coin*.png"
    PLOT="img/templates/plot*.png"
    SHOVEL="img/templates/shovel*.png"
    HARVEST="img/templates/harvest-all*.png"
    CENTER="img/templates/center*.png"
    POTATO="img/templates/potato*.png"
    WHEAT="img/templates/wheat*.png"
    CORN="img/templates/corn*.png"

THRESHOLD = 0.6
DELAY_PER_CLICK = 3
CROP = Template.CORN

def click(p):
    x,y = p
    pyautogui.click(x, y)
    time.sleep(DELAY_PER_CLICK)

def collect_coins():
    coins = detect(Template.COIN)
    for coin in coins:
        click(coin)

def plant_crops():
    plots = detect(Template.PLOT)
    if plots:
        click(plots[0])
        crop = detect(CROP)
        if crop:
            for i in range(4):
                click((crop[0][0] + 50, crop[0][1] + 120))

def go_to_center():
    center = detect(Template.CENTER)
    if center:
        click(center[0])

def harvest_crops():
    shovel = detect(Template.SHOVEL)
    if shovel:
        click((shovel[0][0], shovel[0][1] + 70))
    harvest = detect(Template.HARVEST)
    if harvest: 
        click(harvest[0])

def screenshot():
    file_path = "img/temp.png"
    image = pyautogui.screenshot()
    cv2.imwrite(file_path, cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))
    return file_path

def detect(template):
    results = []
    template_path = template.value
    large_image = cv2.imread(screenshot())

    for file in glob.glob(template_path):
        small_image = cv2.imread(file)
        found = None
        height, width = small_image.shape[:-1]

        result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)

        locations = numpy.where(result >= THRESHOLD)

        mask = numpy.zeros(large_image.shape[:-1], numpy.uint8)

        for coordinate in zip(*locations[::-1]):
            if mask[coordinate[1] + height//2, coordinate[0] + width//2] != 255:
                mask[coordinate[1]:coordinate[1] + height, coordinate[0]:coordinate[0] + width] = 255
                center = (coordinate[0] + width//2, coordinate[1] + height//2)
                results.append(center)
                print(f'Found {template.name.lower()} at {center}...')

    return results

while(True):
    collect_coins()
    harvest_crops()
    plant_crops()
    go_to_center()