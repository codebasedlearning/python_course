# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This snippet discusses the internal representation of integers. """

# pylint: disable=too-few-public-methods
import ctypes
import sys
import sysconfig


# There is currently an internal change or development in Python regarding the
# execution of parallel code (keyword GIL), and without going into detail here,
# this also changes the internal data structures. So there are two ways to
# represent an integer internally.

def detect_python_gil_status():
    """ Detects GIL status, i.e. do we have a Free-Threading (`t` variant w.o. GIL) and is it active? """
    gil_removed = sysconfig.get_config_vars().get("Py_GIL_DISABLED") == 1
    gil_active = not hasattr(sys, '_is_gil_enabled') or sys._is_gil_enabled()   # pylint: disable=protected-access
    return gil_removed, gil_active

GIL_REMOVED, _ = detect_python_gil_status()


# PyLongObject (in CPython) represents the internal structure of a Python integer.
# This may change in future Python versions.

if not GIL_REMOVED:
    class PyLongObject(ctypes.Structure):
        """ PyLongObject for CPython with GIL """
        _fields_ = [
            ("ob_refcnt", ctypes.c_ssize_t),                    # Reference count
            ("ob_type", ctypes.c_void_p),                       # Pointer to PyTypeObject
            ("ob_size", ctypes.c_ssize_t),                      # Number of digits (negative for negative numbers)
            # ("ob_digit", ctypes.c_uint32 * n)                 # n digits (stored in base 2^30)
        ]
else:
    class PyVarObject(ctypes.Structure):
        """ PyVarObject for CPython with GIL removed """
        _fields_ = [
            ('ob_tid', ctypes.c_void_p),                        # owning Thread id
            ('__padding', ctypes.c_uint16),
            ('ob_mutex', ctypes.c_uint8),
            ('ob_gc_bits', ctypes.c_uint8),
            ('ob_ref_local', ctypes.c_uint32),
            ("ob_ref_shared", ctypes.c_ssize_t),
            ("ob_type", ctypes.c_void_p)
        ]
    class PyLongObject(ctypes.Structure):
        """ PyLongObject for CPython with GIL removed """
        _fields_ = [
            ('ob_base', PyVarObject),
            ('lv_tag', ctypes.c_void_p)                         # bits 0,1 contains sign, from bit 3 it has the size
            # ("ob_digit", ctypes.c_uint32 * n)
        ]


def get_long_info(num):
    """ extracts info from PyLongObject """
    addr = id(num)                                              # memory address of object
    obj = PyLongObject.from_address(addr)                       # build object from address

    digits_len = abs(obj.ob_size) if not GIL_REMOVED else abs(obj.lv_tag >> 3) # lv_tag >> NON_SIZE_BITS
    digits_array = [] if digits_len == 0 else list(
        (ctypes.c_uint32 * digits_len).from_address(
            addr + ctypes.sizeof(PyLongObject)
        ))
    # one_more_ref = num  # comment in to increase the reference count
    reference_count = obj.ob_refcnt if not GIL_REMOVED else obj.ob_base.ob_ref_local
    return digits_len, digits_array, reference_count


def show_int_internals():
    """ shows the integer 'digits' and reference counts """
    print("\nshow_int_internals\n==================")

    print(f" 1| {GIL_REMOVED=}\n")

    base = 2**30

    n = 3
    print(f" 2| {n=} | {get_long_info(n)}")
    n = 999
    print(f" 3| {n=} | {get_long_info(n)}")
    m = n
    print(f" 4| {m=} | {get_long_info(m)} | {id(n)=}, {id(m)=}\n")

    n = base-1
    print(f" 5| {n=} | {get_long_info(n)}")
    n = base
    print(f" 6| {n=} | {get_long_info(n)}")
    n = base + 123
    print(f" 7| {n=} | {get_long_info(n)}")
    n = 456*base + 123
    print(f" 8| {n=} | {get_long_info(n)}")
    n3 = 789*base**2 + 456*base + 123
    print(f" 9| {n3=} | {get_long_info(n3)}")


if __name__ == "__main__":
    show_int_internals()


###############################################################################


"""
Summary

Topics
  - internal structure of a Python integer
  - GIL = Global Interpreter Lock; it ensures that only one thread is executing 
    Python code at a time
  - GIL removed = Python without GIL; so we need another way to reference counting

PyLongObject for CPython with GIL
  - 'ob_refcnt' is a global reference counter, protected by the GIL
  - 'ob_size' is the number of digits (negative for negative numbers)
  - https://docs.python.org/3/c-api/long.html#c.PyLongObject

PyLongObject for CPython with GIL removed
  - 'ob_base' is a pointer to a PyVarObject
  - 'lv_tag' is a bit field with the sign and the size of the digit array
  - https://docs.python.org/3/c-api/long.html#c.PyLongObject
  - https://docs.python.org/3/c-api/long.html#c.PyVarObject
  - _object, PyVarObject
    https://github.com/python/cpython/blob/main/Include/object.h#L110
  - PyLongValue with lv_tag
    https://github.com/python/cpython/blob/main/Include/cpython/longintrepr.h#L98
  - masks NON_SIZE_BITS
    https://github.com/python/cpython/blob/main/Include/internal/pycore_long.h#L171

'ob_digit'
  - 'ob_digit' is a digit array (stored in base 2^30)

Reference counting and biased reference counting inter-thread queue
  - https://peps.python.org/pep-0703/#how-to-teach-this
  - https://github.com/colesbury/nogil-3.12/blob/nogil-3.12/Include/cpython/longintrepr.h#L79
  - https://github.com/python/cpython/blob/main/Python/brc.c#L4

See also
  - https://tenthousandmeters.com/blog/python-behind-the-scenes-8-how-python-integers-work/
  - https://rushter.com/blog/python-integer-implementation/
"""
