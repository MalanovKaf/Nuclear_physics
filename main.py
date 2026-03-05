from LabN5 import *
N=[100,1000000]
for i in range (len(N)):
    source = Source_photon(P1=0.2, P2=0.5, P3=0.3, E1=100, E2=200, E3=300, N=N[i])
    source.Energy_diagramma()

