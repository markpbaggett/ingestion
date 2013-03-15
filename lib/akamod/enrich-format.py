from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json
from dplaingestion.selector import getprop, setprop, exists
import re
import os
from amara.lib.iri import is_absolute

@simple_service('POST', 'http://purl.org/la/dp/enrich-format', 'enrich-format', 'application/json')
def enrichformat(body,ctype,action="enrich-format",prop="isShownAt/format",alternate="aggregatedCHO/physicalMedium",typefield="aggregatedCHO/type"):
    """
    Service that accepts a JSON document and enriches the "format" field of that document
    by: 

    a) setting the format to be all lowercase
    b) running through a set of cleanup regex's (e.g. image/jpg -> image/jpeg)
    c) checking to see if the field is a valid IMT, and moving it to a separatee field if not
       See http://www.iana.org/assignments/media-types for list of valid media-types.
       We require that a subtype is defined.
    d) Remove any extra text after the IMT
    e) Set type field from format field, if it is not set.
       The format field is taken if it is a string, or the first element if it is a list.
       It is then splitted and the first part of IMT is taken.

    By default works on the 'format' field, but can be overridden by passing the name of the field to use
    as the 'prop' parameter. Non-IMT's are moved the field defined by the 'alternate' parameter.
    """

    FORMAT_2_TYPE_MAPPINGS = {
            "audio": "sound",
            "image": "image",
            "video": "moving image",
            "text": "text"
    }

    REGEXPS = ('audio/mp3', 'audio/mpeg'), ('images/jpeg', 'image/jpeg'),\
              ('image/jpg','image/jpeg'),('image/jp$', 'image/jpeg'),\
              ('img/jpg', 'image/jpeg'), ('^jpeg$','image/jpeg'),\
              ('^jpg$', 'image/jpeg'), ('\W$','')
    IMT_TYPES = ['application', 'audio', 'image', 'message', 'model',
                 'multipart', 'text', 'video']

    def get_ext(s):
        return os.path.splitext(s)[1].split('.')[1]
        
    def cleanup(s):
        s = s.lower().strip()
        for pattern, replace in REGEXPS:
            s = re.sub(pattern, replace, s)
            s = re.sub(r"^([a-z0-9/]+)\s.*",r"\1",s)
        return s

    def is_imt(s):
        logger.debug("Checking: " + s)
        imt_regexes = [re.compile('^' + x + '(/)') for x in IMT_TYPES]
        return any(regex.match(s) for regex in imt_regexes)

    try :
        data = json.loads(body)
    except Exception:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    if exists(data,prop):
        v = getprop(data,prop)
        format = []
        physicalFormat = getprop(data,alternate) if exists(data,alternate) else []
        if not isinstance(physicalFormat,list):
            physicalFormat = [physicalFormat]

        for s in (v if not isinstance(v,basestring) else [v]):
            if is_absolute(s):
                s = get_ext(s)
            cleaned = cleanup(s)
            if is_imt(cleaned):
                if cleaned not in format:
                    format.append(cleaned)
            else:
                if s not in physicalFormat:
                    physicalFormat.append(s)

        if format:
            setprop(data,prop,format[0]) if len(format) == 1 else setprop(data,prop,format)
        else:
            setprop(data,prop,None)
        if physicalFormat:
            setprop(data,alternate,physicalFormat[0]) if len(physicalFormat) == 1 else setprop(data,alternate,physicalFormat)

    # Setting the type if it is empty.
    f = getprop(data, typefield, True)
    if not f and exists(data, prop):
        format = getprop(data, prop)
        use_format = None
        if isinstance(format, list) and len(format) > 0:
            use_format = format[0]
        elif isinstance(format, basestring):
            use_format = format

        if use_format:
            use_format = use_format.split("/")[0]

            if use_format in FORMAT_2_TYPE_MAPPINGS:
                setprop(data, typefield, FORMAT_2_TYPE_MAPPINGS[use_format])

    return json.dumps(data)
