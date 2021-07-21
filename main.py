import cv2, glob, time, pyautogui, enum, numpy

class Template(enum.Enum):
    COIN="img/templates/coin*.png"
    PLOT="img/templates/plot*.png"
    SHOVEL="img/templates/shovel*.png"
    HARVEST="img/templates/harvest_all*.png"
    OK="img/templates/ok*.png"
    CENTER="img/templates/center*.png"
    POTATO="img/templates/potato*.png"
    WHEAT="img/templates/wheat*.png"
    CORN="img/templates/corn*.png"

THRESHOLD = 0.6
DELAY_PER_CLICK = 0.5
CROP = Template.CORN
PLOT_COUNT = 5

def click(p):
    x,y = p
    pyautogui.click(x, y)
    time.sleep(DELAY_PER_CLICK)

def collect_coins():
    coins = detect(Template.COIN)
    for coin in coins:
        click(coin)

def handle_message():
    message = detect(Template.OK)
    if message:
        click(message[0])

def plant_crops():
    plots = detect(Template.PLOT)
    if plots:
        click(plots[0])
        time.sleep(2)
        crop = detect(CROP)
        if crop:
            for i in range(PLOT_COUNT):
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

def detect(template):
    template_path = template.value
    large_image = pyautogui.screenshot()
    large_image = cv2.cvtColor(numpy.array(large_image), cv2.COLOR_RGB2BGR)

    # Get matched objects
    matches = []
    for file in glob.glob(template_path):
        small_image = cv2.imread(file)
        height, width = small_image.shape[:-1]

        result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)

        locations = numpy.where(result >= THRESHOLD)

        matches += zip(*locations[::-1])

    # Combine overlapping matched objects
    results = []
    mask = numpy.zeros(large_image.shape[:-1], numpy.uint8)

    for match in matches:
        if mask[match[1] + height//2, match[0] + width//2] != 255:
                mask[match[1]:match[1] + height, match[0]:match[0] + width] = 255
                center = (match[0] + width//2, match[1] + height//2)
                results.append(center)
                print(f'Found {template.name.lower()} at {center}.')

    return results

while(True):
    collect_coins()
    harvest_crops()
    plant_crops()
    go_to_center()
    handle_message()