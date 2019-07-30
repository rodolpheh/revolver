class Card():

    disponible_width = 18
    disponible_height = 9
    header_height = 2
    footer_height = 1
    border_width = 1

    def __init__(self, frame, month, *argc, **argv):
        self.frame = frame
        self.month = month
        self.width = None
        self.height = None
        self.x_offset = None
        self.y_offset = None
        self.compute_month_dimensions()
        self.compute_offsets()
        # print("{}:\t{} wide,\t{} high,\tX offset: {},\tY offset: {}".format(
        #         self.month, self.width, self.height,
        #         self.x_offset, self.y_offset))
        print(self)

    def __str__(self):
        returned = ""
        month_path = "revolver/resources/months/" + self.month + ".txt"
        frame_path = "revolver/resources/months/" + self.frame + ".txt"
        try:
            with open(month_path, 'r') as month, \
                    open(frame_path, 'r') as frame:
                line_counter = 0
                month_content = month.readlines()
                month_index = 0
                for frame_line in frame.readlines():
                    line_counter += 1
                    if line_counter <= self.header_height + 1:
                        returned += frame_line
                        continue
                    if line_counter > self.header_height + self.height + 1:
                        returned += frame_line
                        continue
                    month_line = month_content[month_index]
                    month_line = (
                        month_line[:-1] 
                        if month_line[-1] == '\n'
                        else month_line)
                    x_padding = (
                        self.disponible_width
                        - len(month_line) - self.x_offset)
                    returned += frame_line.replace(
                        "XXXXXXXXXXXXXXXXXX",
                        "{3:>{0}}{1}{3:>{2}}".format(
                            self.x_offset,
                            month_line,
                            x_padding,
                            ' '
                        )
                    )
                    month_index += 1
        except FileNotFoundError as fError:
            print(fError)
        return returned

    def compute_month_dimensions(self):
        try:
            with open("revolver/resources/months/" + self.month + ".txt", 'r') \
                    as month:
                self.width = 0
                self.height = 0
                for line in month.readlines():
                    self.width = max(self.width, len(line))
                    self.height += 1
        except FileNotFoundError as fError:
            print(fError)

    def compute_offsets(self):
        try:
            self.x_offset = (self.disponible_width - self.width) // 2
            self.y_offset = (self.disponible_height - self.height) // 2
        except TypeError as tError:
            print(tError)


if __name__ == "__main__":
    from convertdate.french_republican import MOIS
    for mois in MOIS:
        Card("Frame", mois)
