from dashing import *

class Dashboard():
    def __init__(self, title):
        self.title = title

    def UpdateUI(self, output, bar1, bar2, bar3, bar4, bar5):
        self.ui = VSplit(
            Log(title="Terminal Output", color=2, border_color=2),

            VSplit(
                HSplit(
                    VGauge(val=95, border_color=2, color=2),
                    VGauge(val=95, border_color=2, color=2),
                    VGauge(val=95, border_color=2, color=2),
                    VGauge(val=95, border_color=2, color=2),
                    VGauge(val=95, border_color=2, color=2),
                )
            ),
            title=str(self.title),
            color=2
        )
        
        self.log = self.ui.items[0]
        self.log.append(str(output))
        self.ui.items[1].items[0].items[0].value = bar1
        self.ui.items[1].items[0].items[1].value = bar2
        self.ui.items[1].items[0].items[2].value = bar3
        self.ui.items[1].items[0].items[3].value = bar4
        self.ui.items[1].items[0].items[4].value = bar5
        self.ui.display()