from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
# At the top of your utils file, add:
from qiskit.quantum_info import Statevector
import numpy as np
import math as m
from qiskit_aer import QasmSimulator


S_simulator = Aer.get_backend('statevector_simulator')
M_simulator = Aer.get_backend('qasm_simulator')


def Binary(N, total, LSB):
    '''
    Input: N (integer), total (integer), LSB (string)
    Returns the base-2 binary equivalent of N according to left or right least significant bit notation
    '''
    qubits = int(m.log(total, 2))
    b_num = np.zeros(qubits)
    
    for i in np.arange(qubits):
        if N / (2 ** (qubits - i - 1)) >= 1:
            if LSB == 'R':
                b_num[i] = 1
            if LSB == 'L':
                b_num[int(qubits - (i + 1))] = 1
            
            N = N - 2 ** (qubits - i - 1)
    
    B = []
    
    for j in np.arange(len(b_num)):
        B.append(int(b_num[j]))
    
    return B

# credit qcml lab
def Wavefunction(obj, **kwargs):
    '''
    Prints a tidier version of the array statevector corresponding to the wavefunction of a QuantumCircuit object
    Keyword Arguments:          precision (integer) - the decimal precision for amplitudes
                                column (Bool) - prints each state in a vertical column
                                systems (array of integers) - separates the qubits into different states
                                show_systems (array of Bools) - indicates which qubit systems to print
    '''
    if type(obj) == QuantumCircuit:
        statevec = Statevector(obj).data # fixed the statevector object to use
    if type(obj) == np.ndarray:
        statevec = obj
    
    sys = False
    NL = False
    dec = 5
    
    if 'precision' in kwargs:
        dec = int(kwargs['precision'])
    if 'column' in kwargs:
        NL = kwargs['column']
    if 'systems' in kwargs:
        systems = kwargs['systems']
        sys = True
        last_sys = int(len(systems) - 1)
        show_systems = []
        
        for s_chk in np.arange(len(systems)):
            if type(systems[s_chk]) != int:
                raise Exception('systems must be an array of all integers')
        
        if 'show_systems' in kwargs:
            show_systems = kwargs['show_systems']
            if len(systems) != len(show_systems):
                raise Exception('systems and show_systems need to be arrays of equal length')
            
            for ls in np.arange(len(show_systems)):
                if show_systems[ls] not in [True, False]:
                    raise Exception('show_systems must be an array of Truth Values')
                if show_systems[ls] == True:
                    last_sys = int(ls)
        else:
            for ss in np.arange(len(systems)):
                show_systems.append(True)
    
    wavefunction = ''
    qubits = int(m.log(len(statevec), 2))
    
    for i in range(int(len(statevec))):
        value = round(statevec[i].real, dec) + round(statevec[i].imag, dec) * 1j
        if (value.real != 0) or (value.imag != 0):
            state = list(Binary(int(i), int(2**qubits), 'L'))
            state_str = ''
            
            if sys == True:
                k = 0
                for s in np.arange(len(systems)):
                    if show_systems[s] == True:
                        if int(s) != last_sys:
                            state.insert(int(k + systems[s]), '>|')
                            k = int(k + systems[s] + 1)
                        else:
                            k = int(k + systems[s])
                    else:
                        for s2 in np.arange(systems[s]):
                            del state[int(k)]
            
            for j in np.arange(len(state)):
                if type(state[j]) != str:
                    state_str =  str(int(state[j]))  + state_str 
                else:
                    state_str =   state[j] +state_str
            
            if (value.real != 0) and (value.imag != 0):
                if value.imag > 0:
                    wavefunction = wavefunction + str(value.real) + '+' + str(value.imag) + 'j |' + state_str + '> '
                else:
                    wavefunction = wavefunction + str(value.real) + '' + str(value.imag) + 'j |' + state_str + '> '
            
            if (value.real != 0) and (value.imag == 0):
                wavefunction = wavefunction + str(value.real) + ' |' + state_str + '> '
            
            if (value.real == 0) and (value.imag != 0):
                wavefunction = wavefunction + str(value.imag) + 'j |' + state_str + '> '
            
            if NL:
                wavefunction = wavefunction + '\n'
    
    print(wavefunction)


'''
Do not worry about the length of this code block.
You dont need to understand this code.
It is only to help you view the wavefunction in a better way
'''

#credit qcml7 lab 
def WavefunctionToptoBottom( obj, *args, **kwargs):
  '''
  Displays the wavefunction of the quantum system
  '''
  if(type(obj) == QuantumCircuit ):
    statevec = S_simulator.run(obj, shots=1 ).result().get_statevector() 
  if(type(obj) == np.ndarray):
    statevec = obj
  sys = False
  NL = False
  dec = 5
  if 'precision' in kwargs:
    dec = int(kwargs['precision'] )  
  if 'column' in kwargs:  
    NL = kwargs['column']
  if 'systems' in kwargs:
    systems=kwargs['systems']
    sys = True
    last_sys= int(len(systems)-1)
    show_systems = []
    for s_chk in np.arange(len(systems)): 
      if( type(systems [s_chk])!=int ):
        raise Exception('systems must be an array of all integers')
    if 'show_systems' in kwargs: 
      show_systems = kwargs['show_systems']
      if(len(systems)!=len (show_systems) ):
        raise Exception('systems and show_systems need to be arrays of equal length')
      for ls in np.arange(len(show_systems)): 
        if((show_systems [ ls]!=True) and (show_systems [ ls] !=False)): 
          raise Exception('show_systems must be an array of Truth Values') 
        if(show_systems [ ls] ==True): 
          last_sys= int(ls)

    else:
      for ss in np.arange(len(systems)): 
        show_systems.append(True)
  wavefunction = ''
  qubits = int(m.log(len(np.asarray(statevec)),2)) 
  for i in np.arange( int(len(np.asarray(statevec))) ): 
    value = round(statevec[int(i)].real, dec) + round(statevec[int(i)].imag, dec) * 1j
    if( (value.real!=0) or (value.imag!=0)): 
      state= list(Binary(int(i), int(2**qubits),'L'))
      state_str = ''
      if( sys == True ):    #Systems and Show Systems
        k = 0 
        for s in np.arange(len(systems)):
          if(show_systems [s]==True):
            if(int(s)!=last_sys):
              state.insert(int(k+systems [s]), '>|' ) 
              k = int(k+systems[s]+1)
            else:
              k = int(k+systems[s])
          else:
            for s2 in np.arange(systems [s]): 
              del state[int(k)]
      for j in np.arange(len(state)):
        if(type(state[j])!=str):
          state_str = state_str+str(int(state[j]))
        else:
          state_str = state_str+state[j]
      if ((value.real!=0) and (value.imag!=0)):
        if( value.imag> 0):
          wavefunction = wavefunction + str(value.real) + '+' + str(value.imag) + 'j |' + state_str + '>   '
        else:
          wavefunction = wavefunction + str(value.real) +'' + str(value.imag) + 'j |' + state_str + '>    '
      if( (value.real!=0) and (value.imag==0)): 
        wavefunction = wavefunction +str(value.real)+' |'+state_str +'>     '
      if((value.real==0) and (value.imag!=0)): 
        wavefunction = wavefunction +str(value.imag)+'j |'+state_str+ '>     '
      if (NL):
        wavefunction = wavefunction + '\n'
  print(wavefunction)




# now implement a generic QFT method for n qubits

def QFT(num_qubits):
    qreg = QuantumRegister(num_qubits)
    qc = QuantumCircuit(qreg)

    for i in range(num_qubits):
        qc.h(qreg[i])
        for j in range(i+1, num_qubits):
            qc.cp(2*m.pi/2**(j-i+1), qreg[j], qreg[i])
        qc.barrier()

    return qc


def QFT_dag(num_qubits):
    qreg = QuantumRegister(num_qubits)
    qc = QuantumCircuit(qreg)

    for i in range(num_qubits-1, -1, -1):
        for j in range(num_qubits-1, i, -1):
            qc.cp(-2*m.pi/2**(j-i+1), qreg[j], qreg[i])
        qc.h(qreg[i])
        qc.barrier()

    return qc