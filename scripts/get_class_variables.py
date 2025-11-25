
import inspect

def class_variables(cls):
    return {
        k: v for k, v in cls.__dict__.items()
        if not k.startswith("__")              # keine dunder-Attribute
        #and not inspect.isroutine(v)           # keine Methoden/Funktionen
        #and not isinstance(v, property)        # keine @property
        #and not inspect.isdatadescriptor(v)    # keine Deskriptoren
    }

def typed_dict_fields(td_cls):
    return td_cls.__annotations__
