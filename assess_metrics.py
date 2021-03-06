import os
from PIL import Image
from torchvision import transforms
import numpy as np
from tqdm import tqdm

import lpips

from pytorch_msssim import MS_SSIM
from assess_metrics.psnr import psnr
from assess_metrics.fsim import FSIMc
from sewar.full_ref import uqi


dataPath = r''
groundTruthPath = r''
assert len(os.listdir(dataPath)) == len(os.listdir(groundTruthPath))

msssim = MS_SSIM(data_range=1.0)
FSIM_loss = FSIMc()
loss_fn_alex = lpips.LPIPS(net='alex', version='0.0').cuda()


transf = transforms.ToTensor()

PSNR = 0.0
MSSSIM = 0.0
FSIM = 0.0
LPIPS = 0.0
UQI = 0.0
if __name__ == "__main__":
    for x_name, y_name in tqdm(zip(os.listdir(dataPath), os.listdir(groundTruthPath))):
        x_tensor = transf(Image.open(os.path.join(dataPath, x_name))).unsqueeze(0).cuda()
        y_tensor = transf(Image.open(os.path.join(groundTruthPath, y_name))).unsqueeze(0).cuda()

        x = np.array(Image.open(os.path.join(dataPath, x_name)))
        y = np.array(Image.open(os.path.join(groundTruthPath, y_name)))
        MSSSIM += msssim(x_tensor, y_tensor)
        PSNR += psnr(x, y)
        FSIM += FSIM_loss(x_tensor, y_tensor)
        LPIPS += loss_fn_alex(x_tensor, y_tensor)
        UQI += uqi(x, y)

    avgMSSSIM = MSSSIM / len(os.listdir(dataPath))
    avgPSNR = PSNR / len(os.listdir(dataPath))
    avgLPIPS = LPIPS / len(os.listdir(dataPath))
    avgFSIM = FSIM / len(os.listdir(dataPath))
    avgUQI = UQI / len(os.listdir(dataPath))
    print("the current comparison is % s" % os.path.basename(dataPath))
    print("avgMSSSIM is % s" % avgMSSSIM)
    print("avgPSNR is % s" % avgPSNR)
    print("avgLPIPS is % s" % avgLPIPS)
    print("avgUQI is % s" % avgUQI)
    print("avgFSIM is % s" % avgFSIM)
