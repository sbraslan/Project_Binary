import sys
import builtins

# Metin2 Python2 compatibility names.
# Keep legacy game scripts functional while runtime is CPython 3.15.
builtins.long = int
builtins.unicode = str
builtins.basestring = (str, bytes)
builtins.xrange = range
builtins.raw_input = input

# Legacy scripts importing __builtin__ can continue working.
sys.modules.setdefault("__builtin__", builtins)
import builtins

# Metin2 Python2 compatibility names.
# Keep legacy game scripts functional while runtime is CPython 3.15.
builtins.long = int
builtins.basestring = str
builtins.basestring = (str, bytes)
builtins.xrange = range
builtins.raw_input = input

# Legacy scripts importing __builtin__ can continue working.
sys.modules.setdefault("__builtin__", builtins)
import app
import dbg

if "lib" not in sys.path:
	sys.path.insert(0, "lib")

class TraceFile:
	def flush(self):
		pass

	def write(self, msg):
		dbg.Trace(msg)

class TraceErrorFile:
	def flush(self):
		pass

	def write(self, msg):
		dbg.TraceError(msg)
		dbg.RegisterExceptionString(msg)

class LogBoxFile:
	def __init__(self):
		self.stderrSave = sys.stderr
		self.msg = ""

	def __del__(self):
		self.restore()

	def restore(self):
		sys.stderr = self.stderrSave

	def write(self, msg):
		self.msg = self.msg + msg

	def show(self):
		dbg.TraceError(self.msg)
		dbg.LogBox(self.msg,"Error")

sys.stdout = TraceFile()
sys.stderr = TraceErrorFile()
#
# pack file support (must move to system.py, systemrelease.pyc)
#
import marshal

# METIN2_PY315_OPEN_CODE_DIAG_V1
#
# Diagnose the exact CPython import/file-open failure before
# importing the first non-frozen stdlib module.

import builtins
import _io

dbg.TraceError(
    "PYDIAG: sys.version=%r" %
    (sys.version,)
)

dbg.TraceError(
    "PYDIAG: sys.executable=%r" %
    (sys.executable,)
)

dbg.TraceError(
    "PYDIAG: sys.prefix=%r" %
    (sys.prefix,)
)

dbg.TraceError(
    "PYDIAG: sys.base_prefix=%r" %
    (sys.base_prefix,)
)

dbg.TraceError(
    "PYDIAG: sys.path=%r" %
    (sys.path,)
)

dbg.TraceError(
    "PYDIAG: builtins.basestring=%r type=%r callable=%r" %
    (
        builtins.str,
        type(builtins.str),
        callable(builtins.str),
    )
)

dbg.TraceError(
    "PYDIAG: builtins.open=%r type=%r callable=%r" %
    (
        builtins.open,
        type(builtins.open),
        callable(builtins.open),
    )
)

dbg.TraceError(
    "PYDIAG: _io.open=%r type=%r callable=%r" %
    (
        _io.open,
        type(_io.open),
        callable(_io.open),
    )
)

dbg.TraceError(
    "PYDIAG: _io.open_code=%r type=%r callable=%r" %
    (
        _io.open_code,
        type(_io.open_code),
        callable(_io.open_code),
    )
)

_type_file = sys.base_prefix + "/Lib/types.py"

dbg.TraceError(
    "PYDIAG: probe file=%r" %
    (_type_file,)
)

try:
    _probe = _io.open(
        _type_file,
        "rb",
    )

    dbg.TraceError(
        "PYDIAG: _io.open DIRECT TEST = OK"
    )

    _probe.close()

except BaseException as _exc:

    dbg.TraceError(
        "PYDIAG: _io.open DIRECT TEST = FAIL | "
        "%s: %s" %
        (
            type(_exc).__name__,
            _exc,
        )
    )


try:
    _probe = _io.open_code(
        _type_file
    )

    dbg.TraceError(
        "PYDIAG: _io.open_code DIRECT TEST = OK"
    )

    _probe.close()

except BaseException as _exc:

    dbg.TraceError(
        "PYDIAG: _io.open_code DIRECT TEST = FAIL | "
        "%s: %s" %
        (
            type(_exc).__name__,
            _exc,
        )
    )


dbg.TraceError(
    "PYDIAG: continuing to import types"
)


# METIN2_PY315_STDLIB_FIRST_V2
#
# Python 3.15 stdlib paths must stay ahead of the old
# Metin2 Python 2.x client "lib" directory.
#
# Otherwise legacy files such as Python 2.7 types.pyc can
# shadow Python 3.15 standard-library modules.

while "lib" in sys.path:
    sys.path.remove("lib")

sys.path.append("lib")

dbg.TraceError(
    "PY315 PATH ORDER: %r" %
    (sys.path,)
)

import types
from importlib.util import MAGIC_NUMBER
import pack
class pack_file_iterator(object):
	def __init__(self, packfile):
		self.pack_file = packfile

	def __next__(self):
		tmp = self.pack_file.readline()
		if tmp:
			return tmp
		raise StopIteration

_chr = builtins.chr

builtins.NEW_PACK_FILE = True
if NEW_PACK_FILE:
	builtins.old_len = len
# METIN2_PY315_PACK_FILE_V3

def _decode_pack_text(data, filename):

    if isinstance(data, str):
        return data.lstrip("\ufeff")

    if data is None:
        return ""

    if isinstance(data, bytearray):
        data = bytes(data)

    if not isinstance(data, bytes):
        data = bytes(data)

    # UTF-8 BOM
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig")

    # UTF-32 BOM must be tested before UTF-16.
    if (
        data.startswith(b"\xff\xfe\x00\x00")
        or data.startswith(b"\x00\x00\xfe\xff")
    ):
        return data.decode("utf-32")

    # UTF-16 BOM
    if (
        data.startswith(b"\xff\xfe")
        or data.startswith(b"\xfe\xff")
    ):
        return data.decode("utf-16")

    # Our migrated root Python sources are UTF-8.
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        pass

    encodings = []

    try:
        codepage = int(
            app.GetDefaultCodePage()
        )

        if codepage > 0:
            encodings.append(
                "cp%d" % codepage
            )

    except Exception:
        pass

    # Legacy Metin2 locale/data fallbacks.
    encodings.extend(
        [
            "cp1254",
            "cp1252",
            "latin-1",
        ]
    )

    tried = set()

    for encoding in encodings:

        if encoding in tried:
            continue

        tried.add(
            encoding
        )

        try:
            text = data.decode(
                encoding
            )

            dbg.TraceError(
                "PACK TEXT DECODE: %s -> %s"
                % (
                    filename,
                    encoding,
                )
            )

            return text

        except (
            UnicodeDecodeError,
            LookupError,
        ):
            pass

    raise RuntimeError(
        "Unable to decode packed text file: %s"
        % filename
    )


class pack_file(object):

    def __init__(
        self,
        filename,
        mode="rb",
    ):

        if mode not in (
            "r",
            "rb",
        ):
            raise ValueError(
                "pack_file supports only "
                "'r' and 'rb'"
            )

        if not pack.Exist(filename):
            raise IOError(
                "No file or directory: %s"
                % filename
            )

        raw = (
            b""
            if app.ENABLE_PACK_IMPORT_MODULE
            else pack.Get(filename)
        )

        if NEW_PACK_FILE and not raw:

            try:
                tmp = old_open(
                    filename,
                    "rb",
                )

                try:
                    raw = tmp.read()

                finally:
                    tmp.close()

            except (
                IOError,
                OSError,
            ):
                raw = b""

        self.mode = mode
        self.closed = False
        self.tell_size = 0

        if mode == "r":

            self.data = _decode_pack_text(
                raw,
                filename,
            )

            self.data = self.data.replace(
                "\r\n",
                "\n",
            )

        else:

            if isinstance(raw, str):
                raw = raw.encode(
                    "utf-8"
                )

            self.data = (
                raw
                if raw is not None
                else b""
            )


    def __iter__(self):
        return self


    def __next__(self):

        line = self.readline()

        if line:
            return line

        raise StopIteration


    next = __next__


    def read(
        self,
        length=0,
    ):

        empty = (
            ""
            if self.mode == "r"
            else b""
        )

        if not self.data:
            return empty

        if length:

            tmp = self.data[:length]

            self.tell_size += len(
                tmp
            )

            self.data = self.data[
                length:
            ]

            return tmp

        tmp = self.data

        self.tell_size += len(
            tmp
        )

        self.data = empty

        return tmp


    def readline(self):

        separator = (
            "\n"
            if self.mode == "r"
            else b"\n"
        )

        position = self.data.find(
            separator
        )

        if position < 0:
            return self.read()

        return self.read(
            position + 1
        )


    def readlines(self):
        return list(self)


    def tell(self):
        return self.tell_size


    def close(self):

        self.closed = True

        self.data = (
            ""
            if self.mode == "r"
            else b""
        )


    def flush(self):
        pass


    def seek(
        self,
        *args,
    ):
        pass


old_open = open
def open(filename, mode = 'rb'):
	if pack.Exist(filename) and mode in ('r', 'rb'):
		return pack_file(filename, mode)
	else:
		return old_open(filename, mode)

builtins.open = open
builtins.old_open = old_open
builtins.new_open = open

_ModuleType = type(sys)

old_import = __import__
def _process_result(code, fqname):
	# did get_code() return an actual module? (rather than a code object)
	is_module = isinstance(code, _ModuleType)

	# use the returned module, or create a new one to exec code into
	if is_module:
		module = code
	else:
		module = types.ModuleType(fqname)

	# insert additional values into the module (before executing the code)
	#module.__dict__.update(values)

	# the module is almost ready... make it visible
	sys.modules[fqname] = module

	# execute the code within the module's namespace
	if not is_module:
		exec(code, module.__dict__)

	# fetch from sys.modules instead of returning module directly.
	# also make module's __name__ agree with fqname, in case
	# the "exec code in module.__dict__" played games on us.
	module = sys.modules[fqname]
	module.__name__ = fqname
	return module

module_do = lambda x:None

if __USE_CYTHON__:
	import rootlib

# METIN2_PY315_RELATIVE_IMPORT_V2

def __hybrid_import(
    name,
    globals=None,
    locals=None,
    fromlist=(),
    level=0,
):

    # Python 3 package-relative imports such as
    #
    #     from . import _compiler
    #
    # must be handled by CPython importlib.
    if level and level > 0:

        return old_import(
            name,
            globals,
            locals,
            fromlist,
            level,
        )

    # Defensive fallback for Python 3 importlib.
    if not name:

        return old_import(
            name,
            globals,
            locals,
            fromlist,
            level,
        )


    if (
        __USE_CYTHON__
        and rootlib.isExist(name)
    ):

        if name in sys.modules:

            dbg.Tracen(
                "importing from sys.modules %s"
                % name
            )

            return sys.modules[name]

        dbg.Tracen(
            "importing from rootlib %s"
            % name
        )

        newmodule = rootlib.moduleImport(
            name
        )

        module_do(
            newmodule
        )

        sys.modules[name] = newmodule

        return newmodule


    filename = name + ".py"

    if pack.Exist(filename):

        if name in sys.modules:

            dbg.Tracen(
                "importing from sys.modules %s"
                % name
            )

            return sys.modules[name]

        dbg.Tracen(
            "importing from pack %s"
            % name
        )

        if app.ENABLE_PACK_IMPORT_MODULE:

            newmodule = _process_result(
                pack.importModule(
                    filename
                ),
                name,
            )

        else:

            source = pack_file(
                filename,
                "r",
            ).read()

            newmodule = _process_result(
                compile(
                    source,
                    filename,
                    "exec",
                ),
                name,
            )

        module_do(
            newmodule
        )

        return newmodule


    dbg.Tracen(
        "importing from stdlib/lib %s"
        % name
    )

    return old_import(
        name,
        globals,
        locals,
        fromlist,
        level,
    )


def splitext(p):
	root, ext = '', ''
	for c in p:
		if c in ['/']:
			root, ext = root + ext + c, ''
		elif c == '.':
			if ext:
				root, ext = root + ext, c
			else:
				ext = c
		elif ext:
			ext = ext + c
		else:
			root = root + c
	return root, ext

def __IsCompiledFile__(sFileName):
	sBase, sExt = splitext(sFileName)
	sExt=sExt.lower()
	if sExt==".pyc" or sExt==".pyo":
		return 1
	else:
		return 0

def __LoadTextFile__(sFileName):
	if app.ENABLE_PACK_IMPORT_MODULE:
		return pack.importModule(sFileName)
	sText=open(sFileName,'r').read()
	return compile(sText, sFileName, "exec")

def __LoadCompiledFile__(sFileName):
	kFile = old_open(sFileName, "rb")

	if kFile.read(4) != MAGIC_NUMBER:
		kFile.close()
		raise RuntimeError("Bad Python 3 bytecode magic: %s" % sFileName)

	# CPython 3.7+ .pyc header after magic:
	# flags (4) + timestamp/hash payload (8)
	kFile.read(12)

	kData = kFile.read()
	kFile.close()

	return marshal.loads(kData)

def execfile(fileName, dict):
	if __IsCompiledFile__(fileName):
		code=__LoadCompiledFile__(fileName)
	else:
		code=__LoadTextFile__(fileName)
		exec(code, dict)

import builtins
builtins.__import__ = __hybrid_import

builtins.old_execfile = getattr(builtins, "execfile", None)
builtins.execfile = execfile

def GetExceptionString(excTitle):
	(excType, excMsg, excTraceBack)=sys.exc_info()
	excText=""
	excText+=_chr(10)

	import traceback
	traceLineList=traceback.extract_tb(excTraceBack)

	for traceLine in traceLineList:
		if traceLine[3]:
			excText+="%s(line:%d) %s - %s" % (traceLine[0], traceLine[1], traceLine[2], traceLine[3])
		else:
			excText+="%s(line:%d) %s"  % (traceLine[0], traceLine[1], traceLine[2])

		excText+=_chr(10)

	excText+=_chr(10)
	excText+="%s - %s:%s" % (excTitle, excType, excMsg)
	excText+=_chr(10)

	return excText

def ShowException(excTitle):
	excText=GetExceptionString(excTitle)
	dbg.TraceError(excText)
	app.Abort()

	return 0

def RunMainScript(name):
	try:
		execfile(name, __main__.__dict__)
	except RuntimeError as msg:
		msg = str(msg)

		import localeInfo
		if localeInfo.error:
			msg = localeInfo.error.get(msg, msg)

		dbg.TraceError(msg)
		dbg.LogBox(msg)
		app.Abort()

	except:
		msg = GetExceptionString("Run")
		dbg.TraceError(msg)
		dbg.LogBox(msg)
		app.Abort()

import debugInfo
debugInfo.SetDebugMode(__DEBUG__)

loginMark = "-cs"

app.__COMMAND_LINE__ = __COMMAND_LINE__

if __USE_CYTHON__:
	import __main__
	__hybrid_import('Prototype', __main__.__dict__)
else:
	RunMainScript("Prototype.py")
