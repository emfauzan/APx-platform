import pandas as pd
import matplotlib.pyplot as plt


def plot():
    df = pd.read_csv("RMS Level 2ch.csv", skiprows=[0,1,2], sep=";", usecols = ['Hz','dBSPL','Hz1','dBSPL1'])
    x1 = df["Hz"]
    y1 = df["dBSPL"]
    x2 = df["Hz1"]
    y2 = df["dBSPL1"]
    fig, ax = plt.subplots()
    line1 = ax.plot(x1, y1, label="Ch1")
    line2 = ax.plot(x2, y2, label="Ch2")
    leg = ax.legend(fancybox=True)
        
    lines = [line1,line2]
    lined = {}
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(True)
        lined[legline] = origline
            
    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()
        
        #plt.semilogx(self.x, self.y)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("RMS Level (dBSPL)")
        
    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()
    
plot()
