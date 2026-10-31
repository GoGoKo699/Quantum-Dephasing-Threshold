"""Finite channel and lower-witness diagnostics; analytical proofs are separate."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.special import ive
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply

rng = np.random.default_rng(261031)
def reflection(d):
    z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    q,_ = np.linalg.qr(z)
    signs = np.ones(d)
    signs[:d//2] = -1
    return (q*signs) @ q.conj().T

def ad(u):
    return np.kron(u.conj(),u)

pair_checks=[]
for d in [2,4,8]:
    for t in [0.1,1.,10.,100.]:
        a,b=reflection(d),reflection(d)
        exact=expm(t*((ad(a)+ad(b))/2-np.eye(d*d)))
        cutoff=int(np.ceil(12*np.sqrt(t)+60))
        ident=np.eye(d,dtype=complex)
        mixture=ive(0,t)*ad(ident)
        up=ident.copy(); um=ident.copy()
        mass=float(ive(0,t))
        for m in range(1,cutoff+1):
            up=(a if m%2 else b)@up
            um=(b if m%2 else a)@um
            weight=float(ive(m,t))
            mixture+=weight*(ad(up)+ad(um))
            mass+=2*weight
        error=float(np.linalg.norm(exact-mixture,2))
        assert error<5e-11,(d,t,error)
        pair_checks.append({'dimension':d,'time':t,'superoperator_error':error,'retained_mass':mass,'cutoff':cutoff})

z=np.diag([1.,-1.]); x=np.array([[0.,1.],[1.,0.]])
rho=np.diag([1.,0.]).reshape(-1,order='F')
qubit_checks=[]
for t in [1.,1.5,4.,16.,64.,256.,1024.]:
    theta=1/np.sqrt(t)
    b=np.cos(theta)*z+np.sin(theta)*x
    state=(expm(t*((ad(z)+ad(b))/2-np.eye(4)))@rho).reshape((2,2),order='F')
    predicted_z=np.cos(theta/2)**2*np.exp(-t*(1-np.cos(theta)))+np.sin(theta/2)**2*np.exp(-t*(1+np.cos(theta)))
    error=abs(float(np.trace(state@z).real)-predicted_z)
    assert error<1e-11
    qubit_checks.append({'time':t,'theta':float(theta),'z_signal':float(predicted_z),'zero_measurement_probability_gap':float((1-predicted_z)/2),'oracle_operator_distance':float(np.linalg.norm(b-z,2)),'formula_error':error})

radial_checks=[]
for t in [48.,60.,100.,192.,768.,1536.]:
    m=int(np.floor(t/48)); radius=int(np.ceil(4*t))
    down=np.full(radius,1/3)
    up=np.full(radius,2/3);up[0]=1
    diagonal=np.full(radius+1,-1.);diagonal[-1]=-1/3
    generator=diags([up,diagonal,down],[-1,0,1],shape=(radius+1,radius+1),format='csc')
    start=np.zeros(radius+1);start[0]=1
    probs=expm_multiply(t*generator,start)
    assert abs(probs.sum()-1)<1e-11
    p=float(probs[m:].sum())
    bound=1-256/(25*t)-np.exp(-t*(4*np.log(4)-3))
    assert p>=bound-1e-10
    radial_checks.append({'parity_bits':m,'time':t,'tree_radius':radius,'prob_depth_ge_bits':p,'rigorous_chebyshev_minus_poisson_bound':float(bound),'normalization_error':float(abs(probs.sum()-1))})

radius=6
vertices=[()]
for depth in range(1,radius+1):
    vertices.extend(v+(a,) for v in list(vertices) if len(v)==depth-1 for a in range(3) if not v or a!=v[-1])
index={v:i for i,v in enumerate(vertices)}
structural_checks=0
for mask in range(16):
    bits=[0]+[(mask>>(j-1))&1 for j in range(1,5)]
    def parity(v):
        return sum(bits[1:min(len(v),4)+1])%2
    for v in vertices:
        for a in range(3):
            if v and v[-1]==a:
                w=v[:-1]
            elif len(v)<radius:
                w=v+(a,)
            else:
                w=v
            depth=max(len(v),len(w))
            flip=bits[depth] if v!=w and depth<=4 else 0
            assert (parity(v)^flip)==parity(w)
            if w and w[-1]==a:
                vv=w[:-1]
            elif len(w)<radius:
                vv=w+(a,)
            else:
                vv=w
            assert vv==v
            structural_checks+=1

out={'scope':'Finite identity and witness checks; asymptotic and diamond-norm conclusions require the analytic arguments.','seed':261031,'pair_superoperator_checks':pair_checks,'qubit_lower_bound_checks':qubit_checks,'three_tree_radial_checks':radial_checks,'tree_edge_parity_and_involution_checks':structural_checks,'tree_vertices_for_structural_checks':len(vertices),'max_pair_error':max(r['superoperator_error'] for r in pair_checks),'all_checks_passed':True}
print(json.dumps(out,indent=2))
