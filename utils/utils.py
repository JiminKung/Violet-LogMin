import textwrap

def centered_display(root):
    screen_width, screen_height = root.maxsize()
    center_x = (screen_width - root.window_width) / 2
    center_y = (screen_height - root.window_height) / 2
    size = "%dx%d+%d+%d" % (root.window_width, root.window_height, center_x, center_y)
    root.geometry(size)


def format_date(datetime):
    year = datetime.year
    month = datetime.month
    day = datetime.day

    return "{}-{}-{}".format(year, month, day)


def wrap(content, length=5000):
    return "\n".join(textwrap.wrap(content, length))