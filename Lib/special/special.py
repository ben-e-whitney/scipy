# 
# Author:  Travis Oliphant, 2002
#

from cephes import *
from Numeric import *
import types
from scipy_base.fastumath import *
from scipy_base import squeeze, isscalar, iscomplex
import specfun
    
class general_function:
    """
 general_function(somefunction)  Genearlized Function class.

  Description:
 
    Define a generalized function which takes nested sequence
    objects or Numeric arrays as inputs and returns a
    Numeric array as output, evaluating the function over successive
    tuples of the input arrays like the python map function except it uses
    the broadcasting rules of Numeric Python.

  Input:

    somefunction -- a Python function or method

  Example:

    def myfunc(a,b):
        if a > b:
            return a-b
        else
            return a+b

    gfunc = general_function(myfunc)

    >>> gfunc([1,2,3,4],2)
    array([3,4,1,2])

    """
    def __init__(self,pyfunc,otypes=None,doc=None):
        if not callable(pyfunc) or type(pyfunc) is types.ClassType:
            raise TypeError, "Object is not a callable Python object."
        self.thefunc = pyfunc
        if doc is None:
            self.__doc__ = pyfunc.__doc__
        else:
            self.__doc__ = doc
        if otypes is None:
            self.otypes=''
        else:
            if isinstance(otypes,types.StringType):
                self.otypes=otypes
            else:
                raise ValueError, "Output types must be a string."

    def __call__(self,*args):
        return squeeze(arraymap(self.thefunc,args,self.otypes))

def sinc(x):
    """Returns sin(pi*x)/(pi*x) at all points of array x.
    """
    w = asarray(x*pi)
    return where(x==0, 1.0, sin(w)/w)


def jnjnp_zeros(nt):
    """Compute nt (<=1400) zeros of the bessel functions Jn and Jn'
    and arange them in order of their magnitudes.

    Outputs (all are arrays of length nt):
    
       zo[l-1] -- Value of the lth zero of of Jn(x) and Jn'(x)
       n[l-1]  -- Order of the Jn(x) or Jn'(x) associated with lth zero
       m[l-1]  -- Serial number of the zeros of Jn(x) or Jn'(x) associated
                    with lth zero.
       t[l-1]  -- 0 if lth zero in zo is zero of Jn(x), 1 if it is a zero
                    of Jn'(x)

    See jn_zeros, jnp_zeros to get separated arrays of zeros.
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt>1400):
        raise ValueError, "Number must be integer <=1400."
    nt = int(nt)
    zo,n,m,t = specfunc.jdzo(nt)
    return zo,n,m,t

def jnyn_zeros(n,nt):
    """Compute nt zeros of the Bessel functions Jn(x), Jn'(x), Yn(x), and
    Yn'(x), respectively. Returns 4 arrays of length nt.

    See jn_zeros, jnp_zeros, yn_zeros, ynp_zeros to get separate arrays.
    """
    if not (isscalar(nt) and isscalar(n)):
        raise ValueError, "Arguments must be scalars."
    if (floor(n)!=n) or (floor(nt)!=nt):
        raise ValueError, "Arguments must be integers."
    if (nt <=0):
        raise ValueError, "nt > 0"
    return specfun.jyzo(n,nt)

def jn_zeros(n,nt):
    """Compute nt zeros of the Bessel function Jn(x).
    """
    return jnyn_zeros(n,nt)[0]
def jnp_zeros(n,nt):
    """Compute nt zeros of the Bessel function Jn'(x).
    """
    return jnyn_zeros(n,nt)[1]
def yn_zeros(n,nt):
    """Compute nt zeros of the Bessel function Yn(x).
    """
    return jnyn_zeros(n,nt)[2]
def ynp_zeros(n,nt):
    """Compute nt zeros of the Bessel function Yn'(x).
    """
    return jnyn_zeros(n,nt)[3]

def y0_zeros(nt,complex=1):
    """Returns nt (complex or real) zeros of Y0(z), z0, and the value
    of Y0'(z0) = -Y1(z0) at each zero.
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt <=0):
        raise ValueError, "Arguments must be scalar positive integer."
    kf = 0
    kc = (complex != 1)
    return specfun.cyzo(nt,kf,kc)
def y1_zeros(nt,complex=1):
    """Returns nt (complex or real) zeros of Y1(z), z1, and the value
    of Y1'(z1) = Y0(z1) at each zero.
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt <=0):
        raise ValueError, "Arguments must be scalar positive integer."
    kf = 1
    kc = (complex != 1)
    return specfun.cyzo(nt,kf,kc)
def y1p_zeros(nt,complex=1):
    """Returns nt (complex or real) zeros of Y1'(z), z1', and the value
    of Y1(z1') at each zero.
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt <=0):
        raise ValueError, "Arguments must be scalar positive integer."
    kf = 2
    kc = (complex != 1)
    return specfun.cyzo(nt,kf,kc)
    
def jvp(v,z,n=1):
    """Return the nth derivative of Jv(z) with respect to z.
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return jv(v,z)
    else:
        return (jvp(v-1,z,n-1) - jvp(v+1,z,n-1))/2.0

def yvp(v,z,n=1):
    """Return the nth derivative of Yv(z) with respect to z. 
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return yv(v,z)
    else:
        return (yvp(v-1,z,n-1) - yvp(v+1,z,n-1))/2.0

def kvp(v,z,n=1):
    """Return the nth derivative of Kv(z) with respect to z. 
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return kv(v,z)
    else:
        return (kvp(v-1,z,n-1) - kvp(v+1,z,n-1))/2.0

def ivp(v,z,n=1):
    """Return the nth derivative of Iv(z) with respect to z.
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return iv(v,z)
    else:
        return (ivp(v-1,z,n-1) - ivp(v+1,z,n-1))/2.0

def h1vp(v,z,n=1):
    """Return the nth derivative of H1v(z) with respect to z.
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return hankel1(v,z)
    else:
        return (h1vp(v-1,z,n-1) - h1vp(v+1,z,n-1))/2.0

def h2vp(v,z,n=1):
    """Return the nth derivative of H2v(z) with respect to z.
    """
    if not isinstance(n,types.IntType) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if n == 0:
        return hankel2(v,z)
    else:
        return (h2vp(v-1,z,n-1) - h2vp(v+1,z,n-1))/2.0

def sph_jn(n,z):
    """Compute the spherical Bessel function jn(z) and its derivative for
    all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z):
        nm,jn,jnp,yn,ynp = specfun.csphjy(n,z)
    else:
        nm,jn,jnp = specfun.sphj(n,z)        
    return jn, jnp

def sph_yn(n,z):
    """Compute the spherical Bessel function yn(z) and its derivative for
    all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z) or (z<0):
        nm,jn,jnp,yn,ynp = specfun.csphjy(n,z)
    else:
        nm,yn,ynp = specfun.sphy(n,z)
    return yn, ynp

def sph_jnyn(n,z):
    """Compute the spherical Bessel functions, jn(z) and yn(z) and their
    derivatives for all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z) or (z<0):
        nm,jn,jnp,yn,ynp = specfun.csphjy(n,z)
    else:
        nm,yn,ynp = specfun.sphy(n,z)
        nm,jn,jnp = specfun.sphj(n,z)
    return jn,jnp,yn,ynp

def sph_in(n,z):
    """Compute the spherical Bessel function in(z) and its derivative for
    all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z):
        nm,In,Inp,kn,knp = specfun.csphik(n,z)
    else:
        nm,In,Inp = specfun.sphi(n,z)        
    return In, Inp

def sph_kn(n,z):
    """Compute the spherical Bessel function kn(z) and its derivative for
    all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z) or (z<0):
        nm,In,Inp,kn,knp = specfun.csphik(n,z)
    else:
        nm,kn,knp = specfun.sphk(n,z)
    return kn, knp

def sph_inkn(n,z):
    """Compute the spherical Bessel functions, in(z) and kn(z) and their
    derivatives for all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z) or (z<0):
        nm,In,Inp,kn,knp = specfun.csphik(n,z)
    else:
        nm,In,Inp = specfun.sphi(n,z)
        nm,kn,knp = specfun.sphk(n,z)
    return In,Inp,kn,knp

def riccati_jn(n,x):
    """Compute the Ricatti-Bessel function of the first kind and its
    derivative for all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(x)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    nm,jn,jnp = specfun.rctj(n,x)
    return jn,jnp

def riccati_yn(n,x):
    """Compute the Ricatti-Bessel function of the second kind and its
    derivative for all orders up to and including n.
    """
    if not (isscalar(n) and isscalar(x)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    nm,jn,jnp = specfun.rcty(n,x)
    return jn,jnp

def _sph_harmonic(m,n,theta,phi):
    """inputs of (m,n,theta,phi) returns spherical harmonic of order
    m,n (m<=n) and argument theta and phi:  Y^m_n(theta,phi)
    """
    x = cos(phi)
    m,n = int(m), int(n)
    Pmn,Pmnd = lpmn(m,n,x)
    val = Pmn[m,n]
    val *= sqrt((2*m+1)/4.0/pi)
    val *= exp(0.5*gammaln(n-m+1)-gammaln(n+m+1))
    val *= exp(1j*m*theta)
    return val

sph_harm = general_function(_sph_harmonic,'D')

def erfinv(y):
    return ndtri((y+1)/2.0)/sqrt(2)

def erfcinv(y):
    return ndtri((2-y)/2.0)/sqrt(2)

def erf_zeros(nt):
    """Compute nt complex zeros of the error function erf(z).
    """
    if (floor(nt)!=nt) or (nt<=0) or not isscalar(nt):
        raise ValueError, "Argument must be positive scalar integer."
    return specfun.cerzo(nt)

def fresnelc_zeros(nt):
    """Compute nt complex zeros of the cosine fresnel integral C(z).
    """
    if (floor(nt)!=nt) or (nt<=0) or not isscalar(nt):
        raise ValueError, "Argument must be positive scalar integer."
    return specfun.fcszo(1,nt)

def fresnels_zeros(nt):
    """Compute nt complex zeros of the sine fresnel integral S(z).
    """
    if (floor(nt)!=nt) or (nt<=0) or not isscalar(nt):
        raise ValueError, "Argument must be positive scalar integer."
    return specfun.fcszo(2,nt)

def fresnel_zeros(nt):
    """Compute nt complex zeros of the sine and cosine fresnel integrals
    S(z) and C(z).
    """
    if (floor(nt)!=nt) or (nt<=0) or not isscalar(nt):
        raise ValueError, "Argument must be positive scalar integer."
    return specfun.fcszo(2,nt), specfun.fcszo(1,nt)

def gammaincinv(a,y):
    """returns the inverse of the incomplete gamma integral in that it
    finds x such that gammainc(a,x)=y
    """
    return gammainccinv(a,1-y)

def hyp0f1(v,z):
    """Confluent hypergeometric limit function 0F1.
    Limit as q->infinity of 1F1(q;a;z/q)
    """
    z = asarray(z)
    if z.typecode() in ['F', 'D']:
        arg = 2*sqrt(abs(z))
        num = where(z>=0, iv(v-1,arg), jv(v-1,arg))
        den = abs(z)**((v-1.0)/2)
    else:
        num = iv(v-1,2*sqrt(z))
        den = z**((v-1.0)/2.0)
    num *= gamma(v)
    return where(z==0,1.0,num/ asarray(den))

def assoc_laguerre(x,n,k=0.0):
    gam = gamma
    fac = gam(k+1+n)/gam(k+1)/gam(n+1)
    return fac*hyp1f1(-n,k+1,x)

digamma = psi

def polygamma(n, x):
    """Polygamma function which is the nth derivative of the digamma (psi)
    function."""
    n, x = asarray(n), asarray(x)
    cond = (n==0)
    fac2 = (-1.0)**(n+1) * gamma(n+1.0) * zeta(n+1,x)
    if sometrue(cond):
        return where(cond, psi(x), fac2)
    return fac2

def mathieu_even_coef(m,q):
    """Compute expansion coefficients for even mathieu functions and
    modified mathieu functions.
    """
    if not (isscalar(m) and isscalar(q)):
        raise ValueError, "m and q must be scalars."
    if (q < 0):
        raise ValueError, "q >=0"
    if (m != floor(m)) or (m<0):
        raise ValueError, "m must be an integer >=0."

    if (q <= 1):
        qm = 7.5+56.1*sqrt(q)-134.7*q+90.7*sqrt(q)*q
    else:
        qm=17.0+3.1*sqrt(q)-.126*q+.0037*sqrt(q)*q
    km = int(qm+0.5*m)
    if km > 251:
        print "Warning, too many predicted coefficients."
    kd = 1
    m = int(floor(m))
    if m % 2:
        kd = 2

    a = mathieu_a(m,q)
    fc = specfun.fcoef(kd,m,q,a)
    return fc[:km]

def mathieu_odd_coef(m,q):
    """Compute expansion coefficients for even mathieu functions and
    modified mathieu functions.
    """
    if not (isscalar(m) and isscalar(q)):
        raise ValueError, "m and q must be scalars."
    if (q < 0):
        raise ValueError, "q >=0"
    if (m != floor(m)) or (m<=0):
        raise ValueError, "m must be an integer > 0"

    if (q <= 1):
        qm = 7.5+56.1*sqrt(q)-134.7*q+90.7*sqrt(q)*q
    else:
        qm=17.0+3.1*sqrt(q)-.126*q+.0037*sqrt(q)*q
    km = int(qm+0.5*m)
    if km > 251:
        print "Warning, too many predicted coefficients."
    kd = 4
    m = int(floor(m))
    if m % 2:
        kd = 3

    b = mathieu_b(m,q)
    fc = specfunc.fcoef(kd,m,q,b)
    return fc[:km]


def lpmn(m,n,z):
    """Associated Legendre functions of the second kind, Pmn(z) and its
    derivative, Pmn'(z) of order m and degree n.  Returns two
    arrays of size (m+1,n+1) containing Pmn(z) and Pmn'(z) for
    all orders from 0..m and degrees from 0..n.

    z can be complex.
    """
    if not isscalar(m) or (m<0):
        raise ValueError, "m must be a non-negative integer."    
    if not isscalar(n) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if not isscalar(z):
        raise ValueError, "z must be scalar."
    if iscomplex(z):
        p,pd = specfun.clpmn(m,n,z)
    else:        
        p,pd = specfun.lpmn(m,n,z)
    return p,pd


def lqmn(m,n,z):
    """Associated Legendre functions of the second kind, Qmn(z) and its
    derivative, Qmn'(z) of order m and degree n.  Returns two
    arrays of size (m+1,n+1) containing Qmn(z) and Qmn'(z) for
    all orders from 0..m and degrees from 0..n.

    z can be complex.
    """
    if not isscalar(m) or (m<0):
        raise ValueError, "m must be a non-negative integer."    
    if not isscalar(n) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if not isscalar(z):
        raise ValueError, "z must be scalar."
    if iscomplex(z):
        q,qd = specfun.clqmn(m,n,z)
    else:        
        q,qd = specfun.lqmn(m,n,z)
    return q,qd


def bernoulli(n):
    """Return an array of the Bernoulli numbers B0..Bn
    """
    if not isscalar(n) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    n = int(n)
    return specfun.bernob(n)

def euler(n):
    """Return an array of the Euler numbers E0..En
    """
    if not isscalar(n) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    n = int(n)
    return specfun.eulerb(n)
    
def lpn(n,z):
    """Compute sequence of Legendre functions of the first kind (polynomials),
    Pn(z) and derivatives for all degrees from 0 to n (inclusive).
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z):
        pn,pd = specfun.clpn(n,z)
    else:
        pn,pd = specfun.lpn(n,z)
    return pn,pd
    
def lqn(n,z):
    """Compute sequence of Legendre functions of the second kind,
    Qn(z) and derivatives for all degrees from 0 to n (inclusive).
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (n!= floor(n)) or (n<0):
        raise ValueError, "n must be a non-negative integer."
    if iscomplex(z):
        qn,qd = specfun.clqn(n,z)
    else:
        qn,qd = specfun.lqnb(n,z)
    return qn,qd

def ai_zeros(nt):
    """Compute the zeros of Airy Functions Ai(x) and Ai'(x), a and a'
    respectively, and the associated values of Ai(a') and Ai'(a).

    Outputs:

      a[l-1]   -- the lth zero of Ai(x)
      ap[l-1]  -- the lth zero of Ai'(x)
      ai[l-1]  -- Ai(ap[l-1])
      aip[l-1] -- Ai'(a[l-1])
    """
    kf = 1
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be a positive integer scalar."
    return specfun.airyzo(nt,kf)
    
def bi_zeros(nt):
    """Compute the zeros of Airy Functions Bi(x) and Bi'(x), b and b'
    respectively, and the associated values of Ai(b') and Ai'(b).

    Outputs:

      b[l-1]   -- the lth zero of Bi(x)
      bp[l-1]  -- the lth zero of Bi'(x)
      bi[l-1]  -- Bi(bp[l-1])
      bip[l-1] -- Bi'(b[l-1])
    """
    kf = 2
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be a positive integer scalar."
    return specfun.airyzo(nt,kf)

def lmbda(v,x):
    """Compute sequence of lambda functions with arbitrary order v
    and their derivatives.  Lv0(x)..Lv(x) are computed with v0=v-int(v).
    """
    if not (isscalar(v) and isscalar(x)):
        raise ValueError, "arguments must be scalars."
    if (v<0):
        raise ValueError, "argument must be > 0."
    if (v!=floor(v)):
        vm, vl, dl = specfun.lamv(v,x)
    else:
        vm, vl, dl = specfun.lamn(v,x)
    return vl, dl

def pbdv_seq(v,x):
    """Compute sequence of parabolic cylinder functions Dv(x) and
    their derivatives for Dv0(x)..Dv(x) with v0=v-int(v).
    """
    if not (isscalar(v) and isscalar(x)):
        raise ValueError, "arguments must be scalars."
    dv,dp,pdf,pdd = specfun.pbdv(v,x)
    return dv,dp

def pbvv_seq(v,x):
    """Compute sequence of parabolic cylinder functions Dv(x) and
    their derivatives for Dv0(x)..Dv(x) with v0=v-int(v).
    """
    if not (isscalar(v) and isscalar(x)):
        raise ValueError, "arguments must be scalars."
    dv,dp,pdf,pdd = specfun.pbvv(v,x)
    return dv,dp

def pbdn_seq(n,z):
    """Compute sequence of parabolic cylinder functions Dn(z) and
    their derivatives for D0(z)..Dn(z).
    """
    if not (isscalar(n) and isscalar(z)):
        raise ValueError, "arguments must be scalars."
    if (floor(n)!=n):
        raise ValueError, "n must be an integer."    
    cpb,cpd = specfun.cpbdn(n,z)
    return cpb,cpd

def ber_zeros(nt):
    """Compute nt zeros of the kelvin function ber x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,1)

def bei_zeros(nt):
    """Compute nt zeros of the kelvin function bei x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,2)

def ker_zeros(nt):
    """Compute nt zeros of the kelvin function ker x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,3)

def kei_zeros(nt):
    """Compute nt zeros of the kelvin function kei x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,4)

def berp_zeros(nt):
    """Compute nt zeros of the kelvin function ber' x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,5)

def beip_zeros(nt):
    """Compute nt zeros of the kelvin function bei' x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,6)

def kerp_zeros(nt):
    """Compute nt zeros of the kelvin function ker' x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,7)

def keip_zeros(nt):
    """Compute nt zeros of the kelvin function kei' x
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,8)

def kelvin_zeros(nt):
    """Compute nt zeros of all the kelvin functions returned in a
    length 8 tuple of arrays of length nt.
    The tuple containse the arrays of zeros of
    (ber, bei, ker, kei, ber', bei', ker', kei')
    """
    if not isscalar(nt) or (floor(nt)!=nt) or (nt<=0):
        raise ValueError, "nt must be positive integer scalar."
    return specfun.klvnzo(nt,1), \
           specfun.klvnzo(nt,2), \
           specfun.klvnzo(nt,3), \
           specfun.klvnzo(nt,4), \
           specfun.klvnzo(nt,5), \
           specfun.klvnzo(nt,6), \
           specfun.klvnzo(nt,7), \
           specfun.klvnzo(nt,8)
    
def pro_cv_seq(m,n,c):
    """Compute a sequence of characteristic values for the prolate
    spheroidal wave functions for mode m and n'=m..n and spheroidal
    parameter c.
    """
    if not (isscalar(m) and isscalar(n) and isscalar(c)):
        raise ValueError, "Arguments must be scalars."
    if (n!=floor(n)) or (m!=floor(m)):
        raise ValueError, "Modes must be integers."
    if (n-m > 199):
        raise ValueError, "Difference between n and m is too large."
    maxL = n-m+1
    return specfun.segv(m,n,c,1)[1][:maxL]
    
def obl_cv_seq(m,n,c):
    """Compute a sequence of characteristic values for the oblate
    spheroidal wave functions for mode m and n'=m..n and spheroidal
    parameter c.
    """
    if not (isscalar(m) and isscalar(n) and isscalar(c)):
        raise ValueError, "Arguments must be scalars."
    if (n!=floor(n)) or (m!=floor(m)):
        raise ValueError, "Modes must be integers."
    if (n-m > 199):
        raise ValueError, "Difference between n and m is too large."
    maxL = n-m+1
    return specfun.segv(m,n,c,-1)[1][:maxL]

################## test functions #########################
    
def test(level=1):
    from scipy_test.testing import module_test
    module_test(__name__,__file__,level=level)

def test_suite(level=1):
    from scipy_test.testing import module_test_suite
    return module_test_suite(__name__,__file__,level=level)

