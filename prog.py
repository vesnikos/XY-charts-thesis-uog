import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# export at A4 dimensions
plt.rc('figure', figsize=(11.69, 8.27))

BASEDIR = os.path.dirname(__file__)
DATAFOLDER = os.path.join(BASEDIR, 'data')
CHARTFOLDER = os.path.join(BASEDIR, 'charts')
CENTER_DATAFOLDER = os.path.join(DATAFOLDER, 'center')
RANDOM_DATAFOLDER = os.path.join(DATAFOLDER, 'random')
EDGE_DATAFOLDER = os.path.join(DATAFOLDER, 'edge')

for m in [CENTER_DATAFOLDER, RANDOM_DATAFOLDER, EDGE_DATAFOLDER]:
    m_name = os.path.basename(m).capitalize()
    dirs = []
    for f in glob.glob(os.path.join(m, '*.csv')):
        dirs.append(f)
    # Sort by name
    dirs = sorted(dirs,
                  key=lambda item: int(os.path.basename(item).partition('.')[0])
                  )

    # 7 by 3 axes, returned as a 2-d array
    f, axarr = plt.subplots(7, 3, sharey=True)
    for row, cvs in enumerate(dirs):
        d = np.loadtxt(
            fname=os.path.join(CENTER_DATAFOLDER, cvs),
            delimiter=';',
            usecols=(2, 4, 5),  # acc_xy, err_x, err_y
            skiprows=1,  # skip header
            dtype={
                'names': ('Accuracy XY', 'Error X', 'Error Y'),
                'formats': ('f4', 'f4', 'f4')
            }
        )

        axarr[row, 0].hist(d['Accuracy XY'], 6)
        axarr[row, 0].set_ylabel('{0} GCP\n{1} Chk'.format(
            os.path.basename(dirs[row]).split('.')[0],
            os.path.basename(dirs[row]).split('.')[1]
        ),
            rotation='horizontal',
            horizontalalignment='right'
        )
        axarr[row, 1].hist(d['Error X'], 6)
        axarr[row, 2].hist(d['Error Y'], 6)

    # finetuning
    plt.tight_layout()
    axarr[0, 0].set_title('Accuracy XY')
    axarr[0, 1].set_title('Error X')
    axarr[0, 2].set_title('Error Y')

    f.suptitle(' XY Accuracy/Error Distributions (%s)' % m_name, fontsize=14, fontweight='bold')
    f.subplots_adjust(top=0.90)

    plt.savefig(os.path.join(CHARTFOLDER, m_name))
