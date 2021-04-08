from dashing import *

class Dashboard():
    def __init__(self, title):
        self.title = title

    def UpdateUI(self, output, bar1, bar2, bar3, bar4, bar5):
        self.ui = VSplit(
            Log(title="Output Log", color=1, border_color=1),

            VSplit(
                HSplit(
                    VGauge(title="PSA", val=95, border_color=1, color=1),
                    VGauge(title="Weather", val=95, border_color=1, color=1),
                    VGauge(title="Welcome", val=95, border_color=1, color=1),
                    VGauge(title="Weekday", val=95, border_color=1, color=1),
                    VGauge(title="Time", val=95, border_color=1, color=1),
                )
            ),
            title=str(self.title),
            color=1
        )
        
        self.log = self.ui.items[0]
        self.log.append(str(output))
        self.ui.items[1].items[0].items[0].value = bar1
        self.ui.items[1].items[0].items[1].value = bar2
        self.ui.items[1].items[0].items[2].value = bar3
        self.ui.items[1].items[0].items[3].value = bar4
        self.ui.items[1].items[0].items[4].value = bar5
        self.ui.display()