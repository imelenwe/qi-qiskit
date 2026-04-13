Environment Setup: new-env
Starting point: old-env conda env with a broken qiskit installation caused by a package conflict.

Root cause: qiskit-terra 0.45.1 (the legacy pre-1.0 name for qiskit) had been installed alongside qiskit 1.4.3, overwriting its files. This caused qiskit.__version__ to report 0.45.1 and broke imports that qiskit-ibm-runtime depended on.

Steps taken:

Create new env by cloning old-env
Removed qiskit-terra (legacy conflict package, nothing depended on it)

pip uninstall qiskit-terra
Force-reinstalled qiskit 1.4.3 to restore files overwritten by qiskit-terra

pip install qiskit==1.4.3 --force-reinstall --no-deps
Upgraded qiskit-ibm-runtime from 0.23.0 → 0.40.0

0.23.0 connected to auth.quantum-computing.ibm.com (IBM's old service, now shut down)
0.40.0 is the minimum version supporting the new ibm_quantum_platform channel (quantum.ibm.com)

pip install qiskit-ibm-runtime==0.40.0
Final package versions in qcml-ibmqc:

Package	Version
qiskit	1.4.3
qiskit-aer	0.14.2
qiskit-ibm-runtime	0.40.0
