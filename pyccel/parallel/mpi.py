# coding: utf-8

from sympy.core.symbol  import Symbol
from sympy.core.numbers import Integer


from pyccel.types.ast import Variable, IndexedVariable, IndexedElement
from pyccel.types.ast import Assign, Declare
from pyccel.types.ast import NativeBool, NativeFloat, NativeComplex, NativeDouble, NativeInteger
from pyccel.types.ast import DataType
from pyccel.types.ast import DataTypeFactory

from pyccel.parallel.basic        import Basic
from pyccel.parallel.communicator import UniversalCommunicator

def get_shape(expr):
    """Returns the shape of a given variable."""
    if not isinstance(expr, (Variable, IndexedVariable, IndexedElement)):
        raise TypeError('shape is only defined for Variable, IndexedVariable, IndexedElement')

    if isinstance(expr, (Variable, IndexedVariable)):
        shape = expr.shape
        if shape is None:
            return 1
        if isinstance(shape, (list, tuple)):
            n = 1
            for i in shape:
                n *= i
            return n
        else:
            return shape
    elif isinstance(expr, IndexedElement):
        return get_shape(expr.base)

class MPI(Basic):
    """Base class for MPI."""
    pass

##########################################################
#                 Basic Statements
##########################################################
class MPI_Assign(Assign, MPI):
    """MPI statement that can be written as an assignment in pyccel."""
    pass

class MPI_Declare(Declare, MPI):
    """MPI declaration of a variable."""
    pass
##########################################################

##########################################################
#                  Constants
##########################################################
class MPI_status_size(MPI):
    """
    Represents the status size in mpi.

    Examples

    >>> from pyccel.parallel.mpi import MPI_status_size
    >>> MPI_status_size()
    mpi_status_size
    """
    is_integer     = True

    def _sympystr(self, printer):
        sstr = printer.doprint
        return 'mpi_status_size'

class MPI_proc_null(MPI):
    """
    Represents the null process in mpi.

    Examples

    >>> from pyccel.parallel.mpi import MPI_proc_null
    >>> MPI_proc_null()
    mpi_proc_null
    """
    is_integer     = True

    def _sympystr(self, printer):
        sstr = printer.doprint
        return 'mpi_proc_null'

class MPI_comm_world(UniversalCommunicator, MPI):
    """
    Represents the world comm in mpi.

    Examples

    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> MPI_comm_world()
    mpi_comm_world
    """
    is_integer     = True

    def _sympystr(self, printer):
        sstr = printer.doprint
        return 'mpi_comm_world'
##########################################################

##########################################################
#                      Datatypes
##########################################################
# TODO to be removed
class MPI_status_type(DataType):
    """Represents the datatype of MPI status."""
    pass

class MPI_INTEGER(DataType):
    _name = 'MPI_INTEGER'
    pass

class MPI_REAL(DataType):
    _name = 'MPI_REAL'
    pass

class MPI_DOUBLE(DataType):
    _name = 'MPI_DOUBLE'
    pass

class MPI_COMPLEX(DataType):
    _name = 'MPI_COMPLEX'
    pass

class MPI_LOGICAL(DataType):
    _name = 'MPI_LOGICAL'
    pass

class MPI_CHARACTER(DataType):
    _name = 'MPI_CHARACTER'
    pass

def mpi_datatype(dtype):
    """Converts Pyccel datatypes into MPI datatypes."""
    if isinstance(dtype, NativeInteger):
        return 'MPI_INT'
    elif isinstance(dtype, NativeFloat):
        return 'MPI_REAL'
    elif isinstance(dtype, NativeDouble):
        return 'MPI_DOUBLE'
    elif isinstance(dtype, NativeBool):
        return 'MPI_LOGICAL'
    elif isinstance(dtype, NativeComplex):
        return 'MPI_COMPLEX'
    else:
        raise TypeError("Uncovered datatype : ", type(dtype))
##########################################################

##########################################################
#           Communicator Accessors
##########################################################
class MPI_comm_size(MPI):
    """
    Represents the size of a given communicator.

    Examples

    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_size
    >>> comm = MPI_comm_world()
    >>> MPI_comm_size(comm)
    mpi_comm_world.size
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_size, cls).__new__(cls, *args, **options)

    @property
    def comm(self):
        return self.args[0]

    def _sympystr(self, printer):
        sstr = printer.doprint
        return '{0}.{1}'.format(sstr(self.comm), 'size')

class MPI_comm_rank(MPI):
    """
    Represents the process rank within a given communicator.

    Examples

    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_rank
    >>> comm = MPI_comm_world()
    >>> MPI_comm_rank(comm)
    mpi_comm_world.rank
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_rank, cls).__new__(cls, *args, **options)

    @property
    def comm(self):
        return self.args[0]
##########################################################

##########################################################
#          Point-to-Point Communication
##########################################################
class MPI_comm_recv(MPI):
    """
    Represents the MPI_recv statement.
    MPI_recv syntax is
    `MPI_RECV (data, count, datatype, source, tag, comm, status)`

    data:
        initial address of receive buffer (choice) [OUT]
    count:
        number of elements in receive buffer (non-negative integer) [IN]
    datatype:
        datatype of each receive buffer element (handle) [IN]
    source:
        rank of source or MPI_ANY_SOURCE (integer) [IN]
    tag:
        message tag or MPI_ANY_TAG (integer) [IN]
    comm:
        communicator (handle) [IN]
    status:
        status object (Status) [OUT]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_recv
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> source = Variable('int', 'source')
    >>> tag  = Variable('int', 'tag')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_recv(x, source, tag, comm)
    MPI_recv (x, 2*n, MPI_DOUBLE, source, tag, mpi_comm_world, i_mpi_status, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_recv, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def source(self):
        return self.args[1]

    @property
    def tag(self):
        return self.args[2]

    @property
    def comm(self):
        return self.args[3]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data    = self.data
        count   = self.count
        dtype   = self.datatype
        source  = self.source
        tag     = self.tag
        comm    = self.comm
        ierr    = MPI_ERROR
        istatus = MPI_STATUS

        args = (data, count, dtype, source, tag, comm, istatus, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_recv ({0})'.format(args)

        return code

class MPI_comm_send(MPI):
    """
    Represents the MPI_send statement.
    MPI_send syntax is
    `MPI_SEND (data, count, datatype, dest, tag, comm)`

    data:
        initial address of send buffer (choice) [IN]
    count:
        number of elements in send buffer (non-negative integer) [IN]
    datatype:
        datatype of each send buffer element (handle) [IN]
    dest:
        rank of destination (integer) [IN]
    tag:
        message tag (integer) [IN]
    comm:
        communicator (handle) [IN]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_send
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> dest = Variable('int', 'dest')
    >>> tag  = Variable('int', 'tag')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_send(x, dest, tag, comm)
    MPI_send (x, 2*n, MPI_DOUBLE, dest, tag, mpi_comm_world, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_send, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def dest(self):
        return self.args[1]

    @property
    def tag(self):
        return self.args[2]

    @property
    def comm(self):
        return self.args[3]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data  = self.data
        count = self.count
        dtype = self.datatype
        dest  = self.dest
        tag   = self.tag
        comm  = self.comm
        ierr  = MPI_ERROR

        args = (data, count, dtype, dest, tag, comm, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_send ({0})'.format(args)
        return code

##########################################################

##########################################################
#
##########################################################
class MPI_comm_irecv(MPI):
    """
    Represents the MPI_irecv statement.
    MPI_irecv syntax is
    `MPI_IRECV (data, count, datatype, source, tag, comm, status)`

    data:
        initial address of receive buffer (choice) [OUT]
    count:
        number of elements in receive buffer (non-negative integer) [IN]
    datatype:
        datatype of each receive buffer element (handle) [IN]
    source:
        rank of source or MPI_ANY_SOURCE (integer) [IN]
    tag:
        message tag or MPI_ANY_TAG (integer) [IN]
    comm:
        communicator (handle) [IN]
    status:
        status object (Status) [OUT]
    request:
        communication request [OUT]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_irecv
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> source = Variable('int', 'source')
    >>> tag  = Variable('int', 'tag')
    >>> requests = Variable('int', 'requests', rank=1, shape=4, allocatable=True)
    >>> comm = MPI_comm_world()
    >>> MPI_comm_irecv(x, source, tag, requests, comm)
    MPI_irecv (x, 2*n, MPI_DOUBLE, source, tag, mpi_comm_world, requests, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_irecv, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def source(self):
        return self.args[1]

    @property
    def tag(self):
        return self.args[2]

    @property
    def request(self):
        return self.args[3]

    @property
    def comm(self):
        return self.args[4]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data    = self.data
        count   = self.count
        dtype   = self.datatype
        source  = self.source
        tag     = self.tag
        comm    = self.comm
        request = self.request
        ierr    = MPI_ERROR

        args = (data, count, dtype, source, tag, comm, request, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_irecv ({0})'.format(args)

        return code

class MPI_comm_isend(MPI):
    """
    Represents the MPI_isend statement.
    MPI_isend syntax is
    `MPI_ISEND (data, count, datatype, dest, tag, comm)`

    data:
        initial address of send buffer (choice) [IN]
    count:
        number of elements in send buffer (non-negative integer) [IN]
    datatype:
        datatype of each send buffer element (handle) [IN]
    dest:
        rank of destination (integer) [IN]
    tag:
        message tag (integer) [IN]
    comm:
        communicator (handle) [IN]
    request:
        communication request [OUT]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_isend
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> dest = Variable('int', 'dest')
    >>> tag  = Variable('int', 'tag')
    >>> requests = Variable('int', 'requests', rank=1, shape=4, allocatable=True)
    >>> comm = MPI_comm_world()
    >>> MPI_comm_isend(x, dest, tag, requests, comm)
    MPI_isend (x, 2*n, MPI_DOUBLE, dest, tag, mpi_comm_world, requests, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_isend, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def dest(self):
        return self.args[1]

    @property
    def tag(self):
        return self.args[2]

    @property
    def request(self):
        return self.args[3]

    @property
    def comm(self):
        return self.args[4]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data    = self.data
        count   = self.count
        dtype   = self.datatype
        dest    = self.dest
        tag     = self.tag
        comm    = self.comm
        request = self.request
        ierr    = MPI_ERROR

        args = (data, count, dtype, dest, tag, comm, request, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_isend ({0})'.format(args)
        return code

class MPI_comm_sendrecv(MPI):
    """
    Represents the MPI_sendrecv statement.
    MPI_sendrecv syntax is
    `MPI_SENDRECV(senddata, sendcount, sendtype, dest, sendtag, recvdata, recvcount, recvtype, source, recvtag, comm, istatus, ierr)`

    senddata:
        initial address of send buffer (choice) [IN]

    sendcount:
        number of elements in send buffer (non-negative integer) [IN]

    senddatatype:
        datatype of each receive buffer element (handle) [IN]

    dest:
        rank of destination (integer) [IN]

    sendtag:
        message tag (integer) [IN]

    recvdata:
        initial address of receive buffer (choice) [OUT]

    recvcount:
        number of elements in receive buffer (non-negative integer) [IN]

    recvdatatype:
        datatype of each send buffer element (handle) [IN]

    source:
        rank of source or MPI_ANY_SOURCE (integer) [IN]

    recvtag:
        message tag or MPI_ANY_TAG (integer) [IN]

    comm:
        communicator (handle) [IN]

    status:
        status object (Status) [OUT]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_sendrecv
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> y = Variable('double', 'y', rank=2, shape=(n,2), allocatable=True)
    >>> source = Variable('int', 'source')
    >>> dest   = Variable('int', 'dest')
    >>> sendtag  = Variable('int', 'sendtag')
    >>> recvtag  = Variable('int', 'recvtag')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_sendrecv(x, dest, sendtag, y, source, recvtag, comm)
    MPI_sendrecv (x, 2*n, MPI_DOUBLE, dest, sendtag, y, 2*n, MPI_DOUBLE, source, recvtag, mpi_comm_world, i_mpi_status, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_sendrecv, cls).__new__(cls, *args, **options)

    @property
    def senddata(self):
        return self.args[0]

    @property
    def dest(self):
        return self.args[1]

    @property
    def sendtag(self):
        return self.args[2]

    @property
    def recvdata(self):
        return self.args[3]

    @property
    def source(self):
        return self.args[4]

    @property
    def recvtag(self):
        return self.args[5]

    @property
    def comm(self):
        return self.args[6]

    @property
    def sendcount(self):
        return get_shape(self.senddata)

    @property
    def recvcount(self):
        return get_shape(self.recvdata)

    @property
    def senddatatype(self):
        return mpi_datatype(self.senddata.dtype)

    @property
    def recvdatatype(self):
        return mpi_datatype(self.recvdata.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        senddata  = self.senddata
        recvdata  = self.recvdata
        sendcount = self.sendcount
        recvcount = self.recvcount
        sendtype  = self.senddatatype
        recvtype  = self.recvdatatype
        dest      = self.dest
        source    = self.source
        sendtag   = self.sendtag
        recvtag   = self.recvtag
        comm      = self.comm
        ierr      = MPI_ERROR
        istatus   = MPI_STATUS

        args = (senddata, sendcount, sendtype, dest,   sendtag, \
                recvdata, recvcount, recvtype, source, recvtag, \
                comm, istatus, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_sendrecv ({0})'.format(args)
        return code

class MPI_comm_sendrecv_replace(MPI):
    """
    Represents the MPI_sendrecv_replace statement.
    MPI_sendrecv_replace syntax is
    `MPI_SENDRECV_REPLACE(senddata, sendcount, sendtype, dest, sendtag, source, recvtag, comm, istatus, ierr)`

    senddata:
        initial address of send buffer (choice) [IN]

    sendcount:
        number of elements in send buffer (non-negative integer) [IN]

    senddatatype:
        datatype of each receive buffer element (handle) [IN]

    dest:
        rank of destination (integer) [IN]

    sendtag:
        message tag (integer) [IN]

    source:
        rank of source or MPI_ANY_SOURCE (integer) [IN]

    recvtag:
        message tag or MPI_ANY_TAG (integer) [IN]

    comm:
        communicator (handle) [IN]

    status:
        status object (Status) [OUT]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_sendrecv_replace
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> source = Variable('int', 'source')
    >>> dest   = Variable('int', 'dest')
    >>> sendtag  = Variable('int', 'sendtag')
    >>> recvtag  = Variable('int', 'recvtag')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_sendrecv_replace(x, dest, sendtag, source, recvtag, comm)
    MPI_sendrecv_replace (x, 2*n, MPI_DOUBLE, dest, sendtag, source, recvtag, mpi_comm_world, i_mpi_status, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_sendrecv_replace, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def dest(self):
        return self.args[1]

    @property
    def sendtag(self):
        return self.args[2]

    @property
    def source(self):
        return self.args[3]

    @property
    def recvtag(self):
        return self.args[4]

    @property
    def comm(self):
        return self.args[5]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data      = self.data
        count     = self.count
        dtype     = self.datatype
        dest      = self.dest
        source    = self.source
        sendtag   = self.sendtag
        recvtag   = self.recvtag
        comm      = self.comm
        ierr      = MPI_ERROR
        istatus   = MPI_STATUS

        args = (data, count, dtype, dest, sendtag, source, recvtag, \
                comm, istatus, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_sendrecv_replace ({0})'.format(args)
        return code

class MPI_waitall(MPI):
    """
    Represents the MPI_waitall statement.
    MPI_waitall syntax is
    `MPI_WAITALL (count, reqs, statuts)`

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_waitall
    >>> from pyccel.parallel.mpi import MPI_status_type
    >>> requests = Variable('int', 'requests', rank=1, shape=4, allocatable=True)
    >>> mpi_status_size = MPI_status_size()
    >>> stats = Variable('int', 'stats', rank=1, shape=(mpi_status_size,4), allocatable=True)
    >>> MPI_waitall(requests, stats)
    MPI_waitall (4, requests, stats, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_waitall, cls).__new__(cls, *args, **options)

    @property
    def requests(self):
        return self.args[0]

    @property
    def status(self):
        return self.args[1]

    @property
    def count(self):
        return get_shape(self.requests)

    def _sympystr(self, printer):
        sstr = printer.doprint

        requests = self.requests
        count    = self.count
        status   = self.status
        ierr    = MPI_ERROR

        args = (count, requests, status, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_waitall ({0})'.format(args)
        return code

##########################################################
#                  Synchronization
##########################################################
class MPI_comm_barrier(MPI):
    """
    Represents the size of a given communicator.

    Examples

    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_barrier
    >>> comm = MPI_comm_world()
    >>> MPI_comm_barrier(comm)
    mpi_comm_world.barrier
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_barrier, cls).__new__(cls, *args, **options)

    @property
    def comm(self):
        return self.args[0]

    def _sympystr(self, printer):
        sstr = printer.doprint
        return '{0}.{1}'.format(sstr(self.comm), 'barrier')

class MPI_comm_bcast(MPI):
    """
    Represents the MPI_bcast statement.
    MPI_bcast syntax is
    `MPI_BCAST(data, count, datatype, root, comm)`

    data:
        initial address of send buffer (choice) [IN]
    count:
        number of elements in send buffer (non-negative integer) [IN]
    datatype:
        datatype of each send buffer element (handle) [IN]
    root:
        rank of broadcast root (integer)
    comm:
        communicator (handle) [IN]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_bcast
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> root = Variable('int', 'root')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_bcast(x, root, comm)
    MPI_bcast (x, 2*n, MPI_DOUBLE, root, mpi_comm_world, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_bcast, cls).__new__(cls, *args, **options)

    @property
    def data(self):
        return self.args[0]

    @property
    def root(self):
        return self.args[1]

    @property
    def comm(self):
        return self.args[2]

    @property
    def count(self):
        return get_shape(self.data)

    @property
    def datatype(self):
        return mpi_datatype(self.data.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        data  = self.data
        count = self.count
        dtype = self.datatype
        root  = self.root
        comm  = self.comm
        ierr  = MPI_ERROR

        args = (data, count, dtype, root, comm, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_bcast ({0})'.format(args)
        return code

class MPI_comm_scatter(MPI):
    """
    Represents the MPI_scatter statement.
    MPI_scatter syntax is
    `MPI_SCATTER(senddata, sendcount, sendtype, recvdata, recvcount, recvtype,
    root, comm, ierr)`

    senddata:
        initial address of send buffer (choice) [IN]

    sendcount:
        number of elements in send buffer (non-negative integer) [IN]

    senddatatype:
        datatype of each receive buffer element (handle) [IN]

    recvdata:
        initial address of receive buffer (choice) [OUT]

    recvcount:
        number of elements in receive buffer (non-negative integer) [IN]

    recvdatatype:
        datatype of each send buffer element (handle) [IN]

    root:
        rank of broadcast root (integer)

    comm:
        communicator (handle) [IN]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_scatter
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> y = Variable('double', 'y', rank=2, shape=(n,2), allocatable=True)
    >>> root   = Variable('int', 'root')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_scatter(x, y, root, comm)
    MPI_scatter (x, 2*n, MPI_DOUBLE, y, 2*n, MPI_DOUBLE, root, mpi_comm_world, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_scatter, cls).__new__(cls, *args, **options)

    @property
    def senddata(self):
        return self.args[0]

    @property
    def recvdata(self):
        return self.args[1]

    @property
    def root(self):
        return self.args[2]

    @property
    def comm(self):
        return self.args[3]

    @property
    def sendcount(self):
        return get_shape(self.senddata)

    @property
    def recvcount(self):
        return get_shape(self.recvdata)

    @property
    def senddatatype(self):
        return mpi_datatype(self.senddata.dtype)

    @property
    def recvdatatype(self):
        return mpi_datatype(self.recvdata.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        senddata  = self.senddata
        recvdata  = self.recvdata
        sendcount = self.sendcount
        recvcount = self.recvcount
        sendtype  = self.senddatatype
        recvtype  = self.recvdatatype
        root      = self.root
        comm      = self.comm
        ierr      = MPI_ERROR

        args = (senddata, sendcount, sendtype, recvdata, recvcount, recvtype, \
                root, comm, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_scatter ({0})'.format(args)
        return code

class MPI_comm_gather(MPI):
    """
    Represents the MPI_gather statement.
    MPI_gather syntax is
    `MPI_GATHER(senddata, sendcount, sendtype, recvdata, recvcount, recvtype, root, comm)`

    senddata:
        initial address of send buffer (choice) [IN]

    sendcount:
        number of elements in send buffer (non-negative integer) [IN]

    senddatatype:
        datatype of each receive buffer element (handle) [IN]

    recvdata:
        initial address of receive buffer (choice) [OUT]

    recvcount:
        number of elements in receive buffer (non-negative integer) [IN]

    recvdatatype:
        datatype of each send buffer element (handle) [IN]

    root:
        rank of broadcast root (integer)

    comm:
        communicator (handle) [IN]

    Examples

    >>> from pyccel.types.ast import Variable
    >>> from pyccel.parallel.mpi import MPI_comm_world
    >>> from pyccel.parallel.mpi import MPI_comm_gather
    >>> n = Variable('int', 'n')
    >>> x = Variable('double', 'x', rank=2, shape=(n,2), allocatable=True)
    >>> y = Variable('double', 'y', rank=2, shape=(n,2), allocatable=True)
    >>> root   = Variable('int', 'root')
    >>> comm = MPI_comm_world()
    >>> MPI_comm_gather(x, y, root, comm)
    MPI_gather (x, 2*n, MPI_DOUBLE, y, 2*n, MPI_DOUBLE, root, mpi_comm_world, i_mpi_error)
    """
    is_integer = True

    def __new__(cls, *args, **options):
        return super(MPI_comm_gather, cls).__new__(cls, *args, **options)

    @property
    def senddata(self):
        return self.args[0]

    @property
    def recvdata(self):
        return self.args[1]

    @property
    def root(self):
        return self.args[2]

    @property
    def comm(self):
        return self.args[3]

    @property
    def sendcount(self):
        return get_shape(self.senddata)

    @property
    def recvcount(self):
        return get_shape(self.recvdata)

    @property
    def senddatatype(self):
        return mpi_datatype(self.senddata.dtype)

    @property
    def recvdatatype(self):
        return mpi_datatype(self.recvdata.dtype)

    def _sympystr(self, printer):
        sstr = printer.doprint

        senddata  = self.senddata
        recvdata  = self.recvdata
        sendcount = self.sendcount
        recvcount = self.recvcount
        sendtype  = self.senddatatype
        recvtype  = self.recvdatatype
        root      = self.root
        comm      = self.comm
        ierr      = MPI_ERROR

        args = (senddata, sendcount, sendtype, recvdata, recvcount, recvtype, \
                root, comm, ierr)
        args  = ', '.join('{0}'.format(sstr(a)) for a in args)
        code = 'MPI_gather ({0})'.format(args)
        return code
##########################################################


MPI_ERROR   = Variable('int', 'i_mpi_error')
MPI_STATUS  = Variable(MPI_status_type(), 'i_mpi_status')

MPI_COMM_WORLD  = MPI_comm_world()
MPI_STATUS_SIZE = MPI_status_size()
MPI_PROC_NULL   = MPI_proc_null()
