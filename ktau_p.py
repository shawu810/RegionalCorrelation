# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 14:44:07 2017

@author: Fei Wu
Reference:
    https://cran.r-project.org/web/packages/NADA/NADA.pdf
    implementation
    https://github.com/rforge/nada/blob/master/pkg/R/ken.R
"""

import numpy as np

from numpy import sum as sum
from numpy import sign as sign
from numpy import abs as abs
from numpy import min as min
from numpy import where as ifelse
from numpy import argsort as order
from numpy import sqrt
import scipy.stats as ss
from rlencode import rlencode
from collections import Counter


def ktau_p(x, xcen, y, ycen):
    xx = x
    cx = xcen
    yy = y
    cy = ycen
    n = len(x)

    
    delx = min(np.diff(np.sort(np.unique(xx)))) / float(1000) if len(np.unique(xx)) > 1 else 0.0
    dely = min(np.diff(np.sort(np.unique(yy)))) / float(1000) if len(np.unique(yy)) > 1 else 0.0
        
    dupx = xx - delx * cx
    diffx = np.subtract.outer(dupx, dupx)
    diffcx = np.subtract.outer(cx, cx)

    xplus = np.add.outer(cx, cx)
    
    dupy = yy - dely * cy
    diffy = np.subtract.outer(dupy, dupy)
    diffcy = np.subtract.outer(cy, cy)
    yplus = np.add.outer(cy, cy)
    
    signyx = sign(diffy * diffx)
    tt = (sum(1.0 - abs(sign(diffx))) - n) / 2.0
    uu = (sum(1.0 - abs(sign(diffy))) - n) / 2.0

    cix = sign(diffcx) * sign(diffx)
    cix = ifelse(cix<=0.0, 0.0, 1.0)
    tt = tt + sum(cix) / 2.0
    signyx = signyx * (1.0 - cix)
    ciy = sign(diffcy) * sign(diffy)
    ciy = ifelse(ciy<=0.0, 0.0, 1.0)
    uu = uu + sum(ciy) / 2.0
    
    
    signyx = signyx * (1 - ciy)
    xplus = ifelse(xplus <= 1.0, 0.0, 1.0)
    yplus = ifelse(yplus <= 1.0, 0.0, 1.0)
    diffx = abs(sign(diffx))
    diffy = abs(sign(diffy))
    tplus = xplus * diffx
    uplus = yplus * diffy
    tt = tt + sum(tplus) / 2.0
    uu = uu + sum(uplus) / 2.0
    ##
    itot = sum(signyx * (1.0 - xplus) * (1.0 - yplus))
    kenS = itot / 2.0
    tau = (itot)/(n * (n - 1))

    J = n * (n - 1) / 2.0
    taub = kenS/(sqrt(J - tt) * sqrt(J - uu))
    
    varS = n * (n - 1.0) * (2 * n + 5.0) / 18.0
    
    intg = np.arange(1, n + 1) # inclusive at n
    dupx = xx - delx * cx
    dupy = yy - dely * cy
    dorder = order(dupx) # python index start at 0
    dxx = dupx[dorder]
    dcx = cx[dorder]
    dorder = order(dupy)
    dyy = dupy[dorder]
    dcy = cy[dorder]
    

    
    tmpx = dxx - intg * (1.0 - dcx) * delx
    tmpy = dyy - intg * (1.0 - dcy) * dely
    
    _, rxlng, _ = rlencode(ss.rankdata(tmpx), 'max')
    nrxlng = Counter(rxlng)
    rxlng = np.array(nrxlng.keys())
    nrxlng = np.array(nrxlng.values())
    x1 = nrxlng * rxlng * (rxlng - 1.0) * (2.0 * rxlng + 5.0)
    x2 = nrxlng * rxlng * (rxlng - 1.0) * (rxlng - 2.0)
    x3 = nrxlng * rxlng * (rxlng - 1.0)
    
    _, rylng, _ = rlencode(ss.rankdata(tmpy), 'max')
    
    nrylng = Counter(rylng)
    rylng = np.array(nrylng.keys())
    nrylng = np.array([nrylng[key] for key in nrylng.keys()])
    y1 = nrylng * rylng * (rylng - 1.0) * (2.0 * rylng + 5.0)
    y2 = nrylng * rylng * (rylng - 1.0) * (rylng - 2.0)
    y3 = nrylng * rylng * (rylng - 1.0)
    delc = (sum(x1) + sum(y1))/18.0 - sum(x2) * sum(y2)/(9.0 * n * 
        (n - 1.0) * (n - 2.0)) - sum(x3) * sum(y3)/(2.0 * n * (n - 
        1))
    
    x4 = nrxlng * (rxlng - 1.0)
    y4 = nrylng * (rylng - 1.0)
    tmpx = intg * dcx - 1.0
    tmpx = ifelse(tmpx < 0.0, 0.0, tmpx)
    nrxlng = sum(tmpx)
    rxlng = 2
    x1 = nrxlng * rxlng * (rxlng - 1.0) * (2.0 * rxlng + 5.0)
    x2 = nrxlng * rxlng * (rxlng - 1.0) * (rxlng - 2.0)
    x3 = nrxlng * rxlng * (rxlng - 1.0)
    tmpy = intg * dcy - 1.0
    tmpy = ifelse(tmpy < 0.0, 0.0, tmpy)
    nrylng = sum(tmpy)
    rylng = 2
    y1 = nrylng * rylng * (rylng - 1) * (2.0 * rylng + 5.0)
    y2 = nrylng * rylng * (rylng - 1) * (rylng - 2.0)
    y3 = nrylng * rylng * (rylng - 1)
    deluc = (sum(x1) + sum(y1))/18.0 - sum(x2) * sum(y2)/(9.0 * 
        n * (n - 1.0) * (n - 2.0)) - sum(x3) * sum(y3)/(2.0 * n * (n - 
        1)) - (sum(x4) + sum(y4))
    
    dxx = dxx - intg * dcx * delx
    dyy = dyy - intg * dcy * dely
    _, rxlng ,_  = rlencode(ss.rankdata(dxx), 'max')
    nrxlng = Counter(rxlng)
    rxlng = np.array(nrxlng.keys())
    nrxlng = np.array(nrxlng.values())
    x1 = nrxlng * rxlng * (rxlng - 1.0) * (2.0 * rxlng + 5.0)
    x2 = nrxlng * rxlng * (rxlng - 1.0) * (rxlng - 2.0)
    x3 = nrxlng * rxlng * (rxlng - 1.0)
    
    _, rylng, _ = rlencode(ss.rankdata(dyy), 'max')
    nrylng = Counter(rylng)
    rylng = np.array(nrylng.keys())
    nrylng = np.array(nrylng.values())
    y1 = nrylng * rylng * (rylng - 1.0) * (2.0 * rylng + 5.0)
    y2 = nrylng * rylng * (rylng - 1.0) * (rylng - 2.0)
    y3 = nrylng * rylng * (rylng - 1.0)
    
    delu = (sum(x1) + sum(y1))/18.0 - sum(x2) * sum(y2)/(9.0 * n * 
        (n - 1.0) * (n - 2.0)) - sum(x3) * sum(y3)/(2.0 * n * (n - 
        1))
    varS = varS - delc - deluc - delu
    p = 2.0 * (1.0 - ss.norm.cdf((abs(kenS - sign(kenS)))/np.sqrt(varS)))

    return tau, p
    
if __name__ == '__main__':
    # testing 
    x = np.array([26., 26.,26.,26.,26.,26.,26.,26.,26.,26.,26.,26.,26., 27])
    xcen = np.array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,0])
    ycen = np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 00.,  0.,  0.,  0.,  0.,0])
    y = np.array([4186.807954,  4123.633722,  4123.633722,  4352.033033,  4288.894417,
       3782.661053,  3782.661053,  4541.73316,   4428.486096,  4508.606898,
       4822.460146,  4777.151726,  3748.969548, 3748.969548])
        
    print ktau_p(x, xcen, y, ycen)
