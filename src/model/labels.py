class Labels:
    labels_list: list[str]

    def __init__(self):
        self.labels_list = []

    def add_label(self, new_label):
        self.labels_list.append(new_label)

    def add_labels(self, new_labels_list):
        self.labels_list.append(new_labels_list)
