import pandas as pd
import os
import matplotlib 
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import re
from collections import defaultdict

denovo_dir = "../processed_data/translation/nejm/train_denovo/test/"
finetune_dir = "../processed_data/translation/nejm/finetune/test/"
out_dir = "../processed_data/translation/nejm/plot_bleu/"
os.makedirs(out_dir, exist_ok=True)


data = ["wmt18", "nejm.4000", "nejm.8000", "nejm.16000", \
	"nejm.32000", "nejm.64000", "nejm.93303"]
direction = ["zh2en", "en2zh"]
container = defaultdict(list)
for h, in_dir in [("de novo", denovo_dir), ("finetune", finetune_dir)]:
	for i,d in enumerate(data):
		for j in direction:
			fn = f"{in_dir}/{d}.{j}.tc.bleu"
			try:
				with open(fn, "r") as f:
					line = f.readlines()[0].strip()
					bleu = re.search("BLEU = [0-9\.]+", line).group(0).split("=")[1].strip()
					bleu = float(bleu)
					container["bleu"].append(bleu)

				container["data_ord"].append(i)
				container["data"].append(d)
				container["direction"].append(j)
				container["train"].append(h)
			except:
				print(f"{fn} does not exist.")

bleu = pd.DataFrame(container)
plt.ion()
fig, ax = plt.subplots(1, 1)
g = sns.lineplot(x="data_ord", y="bleu", hue="direction", data=bleu, legend="brief", style="train", markers=["o","o"], dashes=[(2,1),""])
fig.set_size_inches(5,4)
fig.tight_layout()
g.legend_.texts[0].set_position((-40,0))
g.legend_.texts[0].set_text("Direction")
g.legend_.texts[3].set_position((-40,0))
g.legend_.texts[3].set_text("Training")
ax.set_xlabel("Sentence Pairs")
ax.set_ylabel("BLEU")
ax.set_xticklabels(["","Baseline", "4000", "8000", "16000", "32000", "64000", "Full"])
ax.legend()
plt.savefig(f"{out_dir}/bleu.pdf")
plt.close()

test = pd.DataFrame({"x": range(10), "y": range(1,11)})
sns.lineplot(x="x", y="y", data=test, legend="full")