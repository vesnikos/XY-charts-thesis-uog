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
    f, axarr = plt.subplots(7, 2, sharey=True,)  # Z axis
    for row, cvs in enumerate(dirs):
        d = np.loadtxt(
            fname=os.path.join(CENTER_DATAFOLDER, cvs),
            delimiter=';',
            usecols=(3, 6),  # acc_z, err_z
            skiprows=1,  # skip header
            dtype={
                'names': ('Accuracy Z', 'Error Z'),
                'formats': ('f4', 'f4')
            }
        )

        axarr[row, 0].hist(d['Accuracy Z'], 6)
        axarr[row, 0].set_ylabel('{0} GCP\n{1} Chk'.format(
            os.path.basename(dirs[row]).split('.')[0],
            os.path.basename(dirs[row]).split('.')[1]
        ),
            rotation='horizontal',
            horizontalalignment='right'
        )
        axarr[row, 1].hist(d['Error Z'], 6)

    # finetuning XY

    axarr[0, 0].set_title('Accuracy Z')

    # finetuning XY
    plt.tight_layout()
    axarr[0, 0].set_title('Accuracy Z')
    axarr[0, 1].set_title('Error Z')

    plt.tight_layout()
    f.suptitle(' Z Accuracy/Error Distributions (%s)' % m_name, fontsize=14, fontweight='bold')
    f.subplots_adjust(top=0.90)

    plt.savefig(os.path.join(CHARTFOLDER, m_name + ' Z'))
